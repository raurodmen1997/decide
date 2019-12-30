from rest_framework.views import APIView
from rest_framework.response import Response
import math



class PostProcView(APIView):

    def metodoHuntington_Hill_aux(self,lista,escaños):

        #Calculamos el numero de votos totales
        totalVotes = 0
        for x in lista:
            totalVotes += x.get('votes')

        #Calculamos el divisor
        d = totalVotes/escaños

        #Creamos divisores un 0.1% inferior y superior por si necesitamos otro divisor
        dpercent = d*0.001
        dinf = d-dpercent
        dsup = d+dpercent

        #Creamos la lista de partidos con sus escaños y el numero de escaños que ha repartido nuestro metodo
        listaEscaños = []
        numEscañosRepartidos = 0

        #Hacer lo siguiente HASTA que el numero de escaños repartidos y el real concuerden
        while(numEscañosRepartidos != escaños):

            #Reseteamos la lista y el numero de escaños repartidos por si nos hemos equivocado de divisor
            listaEscaños = []
            numEscañosRepartidos = 0

            #Por cada partido...
            for x in lista:

                #Si sus votos no superan el divisor pues no tendran escaños
                if(x.get('votes')<d):
                    listaEscaños.append({'option':x.get('option'),'numEscaños':0})
                
                #Si sus votos superan el divisor...
                else:
                    
                    #Creamos la cuota de cada partido, en base al divisor actual
                    quota = x.get('votes')/d
                    
                    #Si la cuota es un entero el numero de escaños es, directamente, la cuota
                    if(int(quota) == quota):
                        listaEscaños.append({'option':x.get('option'),'numEscaños':int(quota)})
                    
                    #Si la cuota no es un entero...
                    else:
                        
                        #Calculamos las cotas superior e inferior de la cuota y despues la media geometrica
                        lQ = int(quota)
                        hQ = lQ+1
                        gM = math.sqrt(lQ*hQ)

                        #Si la cuota es superior a la media geometrica el numero de escaños es la cota sup.
                        if(quota > gM):
                            listaEscaños.append({'option':x.get('option'),'numEscaños':hQ})

                        #Si la cuota es inferior a la media geometrica el numero de escaños es la cota inf.
                        else:
                            listaEscaños.append({'option':x.get('option'),'numEscaños':lQ})
            
            #Una vez rellenada la lista calculamos cuantos escaños hemos utilizados en nuestro reparto
            for e in listaEscaños:
                numEscañosRepartidos += e.get('numEscaños')
            
            #Si el numero de escaños utilizados es menor que el real disminuimos el divisor
            if(numEscañosRepartidos < escaños):
                d = dinf
                dinf = d-dpercent
                dsup = d+dpercent

            #Si el numero de escaños utilizados es mayor que el real aumentamos el divisor
            else:
                d = dsup
                dinf = d-dpercent
                dsup = d+dpercent
            
            #Como cuanto mayor menor divisor mayor cuota (quota=numVotos/divisor) es mas facil para un partido
            # que su cuota supere la media geometrica, por lo que, el proximo intento, es muy posible que
            # aumenten los escaños, solucionando el problema. Para el caso de demasiados escaños se aplicaria
            # el metodo inverso, mayor divisor > menor cuota > menos posibilidad de obtener escaños
            #
            #Si el divisor da problemas lo mejor sera cambiar el 'dpercent' ya que este determina la variacion
            # de divisor que se produce con cada intento, cuanto menor porciento de d menos posiblidad de
            # saltarse el divisor correcto pero mayor cantidad de vueltas se darian al bucle (Eficiencia = 1/Precision)
        
        return listaEscaños

    def metodoHuntington_Hill(self, data):
        t = data.get('type')
        lista = data.get('options')
        escaños = data.get('escaños')
        if(t == 'HUNTINGTON_HILL'):
            return self.metodoHuntington_Hill_aux(lista,escaños)
        else:
            return {}


    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],

            })


        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def cocienteImperiali(self, numEscanyos, datos):
        #Obtenemos los votos totales de la votacion
        totalVotos = self.sumaVotos(datos)

        if totalVotos > 0 and numEscanyos > 0:

            #Calculamos el cociente y lo redondeamos
            q = round(totalVotos / (numEscanyos + 2), 0)
  
            #Realizamos la primera asignación de los escaños
            #y lo añadimos a la lista de datos
            for x in datos:
                ei = math.trunc(x['votes']/q)
                x.update({'escanyos' : ei})
  
            #Calculamos el número de escaños asignados
            escanyosAsignados = self.sumaEscanyos(datos)

            #Si quedan escaños por asignar....
            if(escanyosAsignados < numEscanyos):
                #Calculamos los votos de residuo para añadirlo a la lista según al partido que corresponda
                for x in datos:
                    x.update({ 
                        'escanyosResiduo' : x['votes'] - (q * x['escanyos'])})

                #Ordenamos la lista por los votos de residuo
                datos.sort(key=lambda x : -x['escanyosResiduo'])

                #Mientras quedan escaños por asignar, recorremos la lista de votos de residuo y le sumamos +1 al numero de escaños del partido correspondiente
                for x in datos:
                    while(escanyosAsignados < numEscanyos):
                        x.update({
                        'escanyos' : x['escanyos'] + 1})
                        escanyosAsignados = escanyosAsignados + 1
      
                    #Eliminamos el campo de votos de residuo de la lista
                    x.pop('escanyosResiduo')

                #Ordenamos la lista por escaños antes de devolverla
            datos.sort(key=lambda x : -x['escanyos'])
            
            return Response(datos)
        else:
            for x in datos:
                x.update({'escanyos' : 0})
            return Response(datos)
    

    #Método que calcula el número de votos en la votación
    def sumaVotos(self, datos):
        suma = 0
        for x in datos:
            suma = suma + x['votes']
  
        return suma

    #Método que calcula el número de escaños asignados
    def sumaEscanyos(self, datos):
        suma = 0
        for x in datos:
            suma = suma + x['escanyos']
  
        return suma


    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])
        
        if t == 'IDENTITY':
            return self.identity(opts)
        elif t == 'COCIENTE_IMPERIALI1':
            return self.cocienteImperiali(21, opts)
        elif t == 'COCIENTE_IMPERIALI2':
            return self.cocienteImperiali(6, opts)
        elif t == 'COCIENTE_IMPERIALI3':
            return self.cocienteImperiali(0, opts)
        elif t == 'COCIENTE_IMPERIALI4':
            return self.cocienteImperiali(10, opts)
        elif t == 'COCIENTE_IMPERIALI5':
            return self.cocienteImperiali(0, opts)
        elif t == 'COCIENTE_IMPERIALI6':
            return self.cocienteImperiali(20, opts)
        return Response({})


