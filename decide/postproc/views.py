from rest_framework.views import APIView
from rest_framework.response import Response
import math


import math
import copy

class PostProcView(APIView):


    def ley_de_hondt(self,listaEscaños,escañosTotales):

        numEscañosRepartidos = 0
        
        #inicializamos la lista con el num de escaños y cociente por partido a 0
        for x in listaEscaños:
             x.update({ 
                        'cociente' : 0,
                        'numEscaños' : 0 })


        #Hacer lo siguiente HASTA que el numero de escaños repartidos y el real sean el mismo
        while(numEscañosRepartidos != escañosTotales):

            #Calculamos en primer lugar los cocientes para cada partido en la iteracion
            for x in listaEscaños:

                    esc = int(x.get('numEscaños'))
                    ci = x.get('votes')/(esc+1)
                    print(ci)
                    x.update({ 'cociente' : ci})

                
            mayor_cociente = 0 

            #Una vez hecho esto, sacamos el mayor cociente de todos en esta iteracion
            for x in listaEscaños:
               if(x.get('cociente') > mayor_cociente):
                   mayor_cociente = x.get('cociente')

            #Finalmente, vemos a que partido pertenece dicho cociente mayor y , en caso de ser el suyo,
            #se le otarga como ganador 1 escaño mas y ninguno al resto de partidos
            for x in listaEscaños:
               if(x.get('cociente') == mayor_cociente):
                   x.update({'numEscaños':x.get('numEscaños')+1})
                
               else:
                   x.update({'numEscaños':x.get('numEscaños')})
                
            numEscañosRepartidos =  numEscañosRepartidos + 1
        
        #Finalmente le damos el formato de la coleccion que recibe el test para hacer la comprobaciones pertinentes
        #y eliminamos el campo cociente
        for x in listaEscaños:
            x.pop('cociente')

        return listaEscaños


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

    # Método de reparto de escaños mediante el Cociente Hare
    # type: 'HARE'
    def hare(self, options):

        out = []
        inputData = {}
        results = {}
        quotient = 0

        # Variable necesaria que debe ser parte del parametro 'options'  
        numSeats = 21

        # Formateo de la entrada
        for opt in options:
            i = opt['number']
            v = opt['votes']
            inputData[i] = v

        totalVotes = self.votesSum(inputData)
        quotient = math.floor(totalVotes/numSeats)

        results = self.residueDistribution(self.seatsAndResidues(inputData, quotient), numSeats)

        # Formateo de la salida
        for index, opt in enumerate(options, start = 1):
            out.append({
                **opt,
                'seats': results.get(index)[0],
            })

        return Response(out)

    # Sumatorio de los votos totales
    def votesSum(self, allVotes):
        sum = 0
        for x in allVotes.values():
            sum += x
        return sum       

    # Primera repartición de escaños y cálculo de los votos 
    # residuo para cada partido
    def seatsAndResidues(self, data, quotient):
        res = {}
        for x in data.values():
            a = []
            seats = math.floor(x/quotient)
            residue = x - quotient*seats

            a.append(seats)
            a.append(residue)

            key_list = list(data.keys()) 
            val_list = list(data.values()) 
            n = key_list[val_list.index(x)]

            res[n] = a

        return res

    # Segunda repatición teniendo en cuenta el nº de escaños 
    # aún sin repartir y los votos residuos
    def residueDistribution(self, initalDist, numSeats):
        distSeats = 0
        n = 0
        residues = []
        finalDist = copy.deepcopy(initalDist)
        values = finalDist.values()

        for x in values:
            distSeats += x[0]
            residues.append(x[1])

        notDistributed = numSeats - distSeats
        sortedResidues = residues.copy()
        sortedResidues.sort(reverse = True)

        while notDistributed > 0:
            selected = sortedResidues[n]
            pos = residues.index(selected)

            notDistributed -= 1

            list(values)[pos][0] += 1

            n += 1

        return finalDist

    def identity(self, options):
        out = [] 

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


    #Recuento borda. Realizado por Raúl.
    def borda(self, options):
        salida = {}

        for opcion in options:
            if len(opcion['positions']) != 0:
                suma_total_opcion = 0
                for posicion in opcion['positions']:
                    valor = len(options) - posicion + 1
                    suma_total_opcion += valor
                salida[opcion['option']] = suma_total_opcion
            else:
                salida = {}
                break

        return Response(salida)


    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT | BORDA
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
        numEscanyos = request.data.get('numEscanyos', 0)
        
        if t == 'IDENTITY':
            return self.identity(opts)
        elif t == 'COCIENTE_IMPERIALI1':
            return self.cocienteImperiali(numEscanyos, opts)
        elif t == 'COCIENTE_IMPERIALI2':
            return self.cocienteImperiali(numEscanyos, opts)
        elif t == 'COCIENTE_IMPERIALI3':
            return self.cocienteImperiali(numEscanyos, opts)
        elif t == 'COCIENTE_IMPERIALI4':
            return self.cocienteImperiali(numEscanyos, opts)
        elif t == 'COCIENTE_IMPERIALI5':
            return self.cocienteImperiali(numEscanyos, opts)
        elif t == 'COCIENTE_IMPERIALI6':
            return self.cocienteImperiali(numEscanyos, opts)
        elif t == 'BORDA':
            return self.borda(opts)
        elif t == 'HARE':
            return self.hare(opts)

        return Response({})

          
        return Response({})


    def metodoHondt(self, data):
        t = data.get('type')
        lista = data.get('options')
        escañosTotales = data.get('escañosTotales')
        if(t == 'HONDT'):
            return self.ley_de_hondt(lista,escañosTotales)
        else:
            return {}


    def metodoHondt(self, data):
        t = data.get('type')
        lista = data.get('options')
        escañosTotales = data.get('escañosTotales')
        if(t == 'HONDT'):
            return self.ley_de_hondt(lista,escañosTotales)
        else:
            return {}

        return Response({})

