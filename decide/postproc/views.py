from rest_framework.views import APIView
from rest_framework.response import Response
import math


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

    def cocienteImperiali(numEscanyos, datos):
        #Obtenemos los votos totales de la votacion
        totalVotos = sumaVotos(datos);

        #Calculamos el cociente y lo redondeamos
        q = round(totalVotos / (numEscanyos + 2), 0);
  
        #Realizamos la primera asignación de los escaños
        #y lo añadimos a la lista de datos
        for x in datos:
            ei = math.trunc(x['postproc']/q);
            x.update({'encanyos' : ei});
  
        #Calculamos el número de escaños asignados
        escanyosAsignados = sumaEscanyos(datos);

        #Si quedan escaños por asignar....
        if(escanyosAsignados < numEscanyos):
            #Calculamos los votos de residuo para añadirlo a la lista según al partido que corresponda
            for x in datos:
                x.update({ 
                    'escanyosResiduo' : x['postproc'] - (q * x['encanyos'])
                });

            #Ordenamos la lista por los votos de residuo
            datos.sort(key=lambda x : -x['escanyosResiduo']);

            #Mientras quedan escaños por asignar, recorremos la lista de votos de residuo y le sumamos +1 al numero de escaños del partido correspondiente
            for x in datos:
                while(escanyosAsignados < numEscanyos):
                    x.update({
                    'encanyos' : x['encanyos'] + 1
                    })
                    escanyosAsignados = escanyosAsignados + 1;
      
                #Eliminamos el campo de votos de residuo de la lista
                x.pop('escanyosResiduo');

            #Ordenamos la lista por escaños antes de devolverla
            datos.sort(key=lambda x : -x['encanyos']);
        return datos;
    

    #Método que calcula el número de votos en la votación
    def sumaVotos(datos):
        suma = 0;
        for x in datos:
            suma = suma + x['postproc']
  
        return suma;

    #Método que calcula el número de escaños asignados
    def sumaEscanyos(datos):
        suma = 0;
        for x in datos:
            suma = suma + x['encanyos']
  
        return suma;

