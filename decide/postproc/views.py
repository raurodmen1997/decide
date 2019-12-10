from rest_framework.views import APIView
from rest_framework.response import Response


class PostProcView(APIView):

    #atributo de candidato GENERO puede ser "F"=female o "M"=male
    def seCumpleLeyParidad(lista):
	    sumFemales = 0
	    for x in lista:
		    for y in x.values():
			    if y == "F":
				    sumFemales += 1
	    return 0.4*len(lista) <= sumFemales <= 0.6*len(lista)


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
