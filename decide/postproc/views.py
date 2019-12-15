from rest_framework.views import APIView
from rest_framework.response import Response


class PostProcView(APIView):

    def ley_de_hondt(self,lista,escañosTotales):

        numEscaños = 0
        numEscañosRepartidos = 0

        #Creamos la lista de partidos con sus escaños y el numero de escaños que ha repartido nuestro metodo
        listaEscaños = []
        
        #inicializamos la lista con el num de escaños por partido a 0
        for x in lista:
            listaEscaños.append({'option':x.get('option'),'votes':x.get('votes'),'cociente':0,'numEscaños':numEscaños})

        #Hacer lo siguiente HASTA que el numero de escaños repartidos y el real sean el mismo
        while(numEscañosRepartidos != escañosTotales):

            #Calculamos en primer lugar los cocientes para cada partido en la iteracion
            for x in listaEscaños:

                cociente = x.get('votes')/(x.get('escaños')+1)
                listaEscaños.append({'option':x.get('option'),'votes':x.get('votes'),'cociente':cociente,'numEscaños':x.get('escaños')})

            mayor_cociente = 0 

            #Una vez hecho esto, sacamos el mayor cociente de todos en esta iteracion
            for x in listaEscaños:
               if(x.get('cociente') > mayor_cociente):
                   mayor_cociente = x.get('cociente')

            #Finalmente, vemos a que partido pertenece dicho cociente mayor y , en caso de ser el suyo,
            #se le otarga como ganador 1 escaño mas y ninguno al resto de partidos
            for x in listaEscaños:
               if(x.get('cociente') == mayor_cociente):
                   listaEscaños.append({'option':x.get('option'),'votes':x.get('votes'),'cociente':x.get('cociente')
                   ,'numEscaños':x.get('numEscaños')+1})
                else:
                    listaEscaños.append({'option':x.get('option'),'votes':x.get('votes'),'cociente':x.get('cociente')
                   ,'numEscaños':x.get('numEscaños')})
                
            numEscañosRepartidos =  numEscañosRepartidos + 1
        
        #Finalmente le damos el formato de la coleccion que recibe el test para hacer la comprobaciones pertinentes
        listaFinal = []

        for x in listaEscaños:
            listaFinal.append({'option':x.get('option'),'numEscaños':x.get('numEscaños')})

        return listaFinal


    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

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


    def metodoHondt(self, data):
        t = data.get('type')
        lista = data.get('options')
        escañosTotales = data.get('escañosTotales')
        if(t == 'HONDT'):
            return self.ley_de_hondt(lista,escañosTotales)
        else:
            return {}