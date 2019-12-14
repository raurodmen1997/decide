from rest_framework.views import APIView
from rest_framework.response import Response

import math
import copy

class PostProcView(APIView):

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

        t = request.data.get('type', 'HARE')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts)

        if t == 'HARE':
            return self.hare(opts)

        return Response({})

    
