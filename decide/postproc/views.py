from rest_framework.views import APIView
from rest_framework.response import Response

import math
import copy

class PostProcView(APIView):

    def identity(self, options):
        out = []
        numEscaños = 21

        lista = {"A":391000, "B":312000, "C":245034, "D":200001, "E":98562, "F":20145}

        def hareQuotient(votes):
            q = math.floor(votes/numEscaños)
            return q

        def votesSum(lista):
            sum = 0
            for x in lista.values():
                sum += x
            return sum

        def seatsAndResidues(lista):
            res = {}
            quotient = hareQuotient(votesSum(lista))
            for x in lista.values():
                a = []
                seats = math.floor(x/quotient)
                residue = x - quotient*seats

                a.append(seats)
                a.append(residue)

                key_list = list(lista.keys()) 
                val_list = list(lista.values()) 
                n = key_list[val_list.index(x)]

                res[n] = a

            return res

        def residueDistribution(initalDist):
            distSeats = 0
            n = 0
            residues = []
            finalDist = copy.deepcopy(initalDist)
            values = finalDist.values()

            for x in values:
                distSeats += x[0]
                residues.append(x[1])

            notDistributed = numEscaños - distSeats
            sortedResidues = residues.copy()
            sortedResidues.sort(reverse = True)

            while notDistributed > 0:
                selected = sortedResidues[n]
                pos = residues.index(selected)
            
                residues.pop(pos)
                notDistributed -= 1

                list(values)[pos][0] += 1

                n += 1

            return finalDist


        results = residueDistribution(seatsAndResidues(lista))

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

    
