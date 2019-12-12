from rest_framework.views import APIView
from rest_framework.response import Response


class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)


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

        if t == 'IDENTITY':
            return self.identity(opts)
        elif t == 'BORDA':
            return self.borda(opts)
        return Response({})
