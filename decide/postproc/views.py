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


