from rest_framework.views import APIView
from rest_framework.response import Response

import math
import copy

class PostProcView(APIView):

    def identity(self, options):
        out = []
        inputData = {}
        results = {}  
        numEscaños = 21

        for opt in options:
            i = opt['number']
            v = opt['votes']
            inputData[i] = v

        def hareQuotient(votes):
            q = math.floor(votes/numEscaños)
            return q

        def votesSum(allVotes):
            sum = 0
            for x in allVotes.values():
                sum += x
            return sum

        def seatsAndResidues(data):
            res = {}
            quotient = hareQuotient(votesSum(data))
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

        results = residueDistribution(seatsAndResidues(inputData))

        for index, opt in enumerate(options, start = 1):
            out.append({
                **opt,
                'seats': results.get(index)[0],
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

    
