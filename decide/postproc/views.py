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

        return Response({})
