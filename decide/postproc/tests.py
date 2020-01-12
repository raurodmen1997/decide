from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods
from postproc import views

class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.views = views.PostProcView()
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None

    ##### Tests Hare ########

    # Testeo de un caso sencillo con las opciones no ordenadas segun votos
    def test_hare_01(self):
        data = {
            'type': 'HARE',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 245034 },
                { 'option': 'Option 2', 'number': 2, 'votes': 98562 },
                { 'option': 'Option 3', 'number': 3, 'votes': 391000 },
                { 'option': 'Option 4', 'number': 4, 'votes': 200001 },
                { 'option': 'Option 5', 'number': 5, 'votes': 312000 },
                { 'option': 'Option 6', 'number': 6, 'votes': 20145 },
            ],
            'numEscanyos': 21,
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 245034, 'escanyos': 4 },
            { 'option': 'Option 2', 'number': 2, 'votes': 98562, 'escanyos': 2 },
            { 'option': 'Option 3', 'number': 3, 'votes': 391000, 'escanyos': 7 },
            { 'option': 'Option 4', 'number': 4, 'votes': 200001, 'escanyos': 3 },
            { 'option': 'Option 5', 'number': 5, 'votes': 312000, 'escanyos': 5 },
            { 'option': 'Option 6', 'number': 6, 'votes': 20145, 'escanyos': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    # Caso en el que existe gran disparidad en los votos de las opciones
    def test_hare_02(self):
        data = {
            'type': 'HARE',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 2510 },
                { 'option': 'Option 2', 'number': 2, 'votes': 300 },
                { 'option': 'Option 3', 'number': 3, 'votes': 245034 },
                { 'option': 'Option 4', 'number': 4, 'votes': 200001 },
                { 'option': 'Option 5', 'number': 5, 'votes': 14 },
                { 'option': 'Option 6', 'number': 6, 'votes': 20145 },
            ],
            'numEscanyos': 21,
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 2510, 'escanyos': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 300, 'escanyos': 0 },
            { 'option': 'Option 3', 'number': 3, 'votes': 245034, 'escanyos': 11 },
            { 'option': 'Option 4', 'number': 4, 'votes': 200001, 'escanyos': 9 },
            { 'option': 'Option 5', 'number': 5, 'votes': 14, 'escanyos': 0 },
            { 'option': 'Option 6', 'number': 6, 'votes': 20145, 'escanyos': 1 },
        ]
        

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    # Testeo del comportamiento del código con una opción con 0 votos
    def test_hare_03(self):
        data = {
            'type': 'HARE',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 2510 },
                { 'option': 'Option 2', 'number': 2, 'votes': 6540 },
                { 'option': 'Option 3', 'number': 3, 'votes': 0 },
                { 'option': 'Option 4', 'number': 4, 'votes': 12046 },
                { 'option': 'Option 5', 'number': 5, 'votes': 14 },
                { 'option': 'Option 6', 'number': 6, 'votes': 20145 },
            ],
            'numEscanyos': 21,
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 2510, 'escanyos': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 6540, 'escanyos': 4 },
            { 'option': 'Option 3', 'number': 3, 'votes': 0, 'escanyos': 0 },
            { 'option': 'Option 4', 'number': 4, 'votes': 12046, 'escanyos': 6 },
            { 'option': 'Option 5', 'number': 5, 'votes': 14, 'escanyos': 0 },
            { 'option': 'Option 6', 'number': 6, 'votes': 20145, 'escanyos': 10 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    # Testeo del comportamiento del código con sólo 2 opciones
    def test_hare_04(self):
        data = {
            'type': 'HARE',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 264793 },
                { 'option': 'Option 2', 'number': 2, 'votes': 654046 },
            ],
            'numEscanyos': 14,
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 264793, 'escanyos': 4 },
            { 'option': 'Option 2', 'number': 2, 'votes': 654046, 'escanyos': 10 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    # Testeo del comportamiento del código con una votación con 0 votos totales
    def test_hare_05(self):
        data = {
            'type': 'HARE',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 0 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 0 },
                { 'option': 'Option 4', 'number': 4, 'votes': 0 },
                { 'option': 'Option 5', 'number': 5, 'votes': 0 },
                { 'option': 'Option 6', 'number': 6, 'votes': 0 },
            ],
            'numEscanyos': 27,
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 0, 'escanyos': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'escanyos': 0 },
            { 'option': 'Option 3', 'number': 3, 'votes': 0, 'escanyos': 0 },
            { 'option': 'Option 4', 'number': 4, 'votes': 0, 'escanyos': 0 },
            { 'option': 'Option 5', 'number': 5, 'votes': 0, 'escanyos': 0 },
            { 'option': 'Option 6', 'number': 6, 'votes': 0, 'escanyos': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    # Mismo caso que el anterior pero solo una opcion ha recibido votos
    def test_hare_06(self):
        data = {
            'type': 'HARE',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 1678 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 0 },
                { 'option': 'Option 4', 'number': 4, 'votes': 0 },
                { 'option': 'Option 5', 'number': 5, 'votes': 0 },
                { 'option': 'Option 6', 'number': 6, 'votes': 0 },
            ],
            'numEscanyos': 34,
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 1678, 'escanyos': 34 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'escanyos': 0 },
            { 'option': 'Option 3', 'number': 3, 'votes': 0, 'escanyos': 0 },
            { 'option': 'Option 4', 'number': 4, 'votes': 0, 'escanyos': 0 },
            { 'option': 'Option 5', 'number': 5, 'votes': 0, 'escanyos': 0 },
            { 'option': 'Option 6', 'number': 6, 'votes': 0, 'escanyos': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    # Sólo 2 opciones reciben votos y reciben el mismo numero
    def test_hare_07(self):
        data = {
            'type': 'HARE',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 1678 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 0 },
                { 'option': 'Option 4', 'number': 4, 'votes': 1678 },
                { 'option': 'Option 5', 'number': 5, 'votes': 0 },
                { 'option': 'Option 6', 'number': 6, 'votes': 0 },
            ],
            'numEscanyos': 34,
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 1678, 'escanyos': 17 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'escanyos': 0 },
            { 'option': 'Option 3', 'number': 3, 'votes': 0, 'escanyos': 0 },
            { 'option': 'Option 4', 'number': 4, 'votes': 1678, 'escanyos': 17 },
            { 'option': 'Option 5', 'number': 5, 'votes': 0, 'escanyos': 0 },
            { 'option': 'Option 6', 'number': 6, 'votes': 0, 'escanyos': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #TESTs HUNTINGTON_HILL
    def test_huntington_hill1(self):
        data = {
            'type': 'HUNTINGTON_HILL',
            'options': [
                {'option':'PP','number':1,'votes': 100000},
                {'option':'PSOE', 'number':2,'votes': 80000},
                {'option':'Podemos', 'number':3,'votes': 30000},
                {'option':'Cs', 'number':4,'votes': 20000}
            ],
            'numEscanyos': 8
        }

        expected_result = [
            {'option':'PP','number':1,'votes': 100000,'escanyos':4},
            {'option':'PSOE', 'number':2,'votes': 80000,'escanyos':3},
            {'option':'Podemos', 'number':3,'votes': 30000,'escanyos':1},
            {'option':'Cs', 'number':4,'votes': 20000,'escanyos':0}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_huntington_hill2(self):
        data = {
            'type': 'HUNTINGTON_HILL',
            'options': [
                {'option':'PP','number':1,'votes': 126837},
                {'option':'PSOE', 'number':2,'votes': 71804},
                {'option':'Podemos', 'number':3,'votes': 25880}
            ],
            'numEscanyos': 4
        }

        expected_result = [
            {'option':'PP','number':1,'votes': 126837,'escanyos':3},
            {'option':'PSOE', 'number':2,'votes': 71804,'escanyos':1},
            {'option':'Podemos', 'number':3,'votes': 25880,'escanyos':0}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_huntington_hill3(self):
        data = {
            'type': 'HUNTINGTON_HILL',
            'options': [
                {'option':'Marta','number':1,'votes': 380},
                {'option':'Jose','number':2, 'votes': 240},
                {'option':'Pedro','number':3, 'votes': 105},
                {'option':'Ana', 'number':4,'votes': 55}
            ],
            'numEscanyos': 22
        }

        expected_result = [
            {'option':'Marta','number':1,'votes': 380,'escanyos':10},
            {'option':'Jose','number':2, 'votes': 240,'escanyos':7},
            {'option':'Pedro','number':3, 'votes': 105,'escanyos':3},
            {'option':'Ana', 'number':4,'votes': 55,'escanyos':2}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_huntington_hill4(self):
        data = {
            'type': 'HUNTINGTON_HILL',
            'options': [
                {'option':'PP','number':1,'votes': 162310},
                {'option':'PSOE','number':2, 'votes': 538479},
                {'option':'Podemos','number':3, 'votes': 197145}
            ],
            'numEscanyos': 41
        }

        expected_result = [
            {'option':'PP','number':1,'votes': 162310,'escanyos':7},
            {'option':'PSOE','number':2, 'votes': 538479,'escanyos':25},
            {'option':'Podemos','number':3, 'votes': 197145,'escanyos':9}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_hondt_01(self):
        data = {
            'type': 'HONDT',
            'options': [
                {'option':'A','number':1,'votes': 340000},
                {'option':'B','number':2, 'votes': 280000},
                {'option':'C','number':3, 'votes': 160000},
                {'option':'D','number':4, 'votes': 60000},
                {'option':'E','number':5, 'votes': 15000}
            ],
            'numEscanyos': 7
        }

        expected_result = [
            {'option':'A','number':1,'votes': 340000,'escanyos': 3},
            {'option':'B','number':2, 'votes': 280000,'escanyos': 3},
            {'option':'C','number':3, 'votes': 160000,'escanyos': 1},
            {'option':'D','number':4, 'votes': 60000,'escanyos': 0},
            {'option':'E','number':5, 'votes': 15000,'escanyos': 0}
        ]

        result = self.views.metodoHondt(data)

        print('test 1')
        print(result)

        self.assertEqual(result, expected_result)

    def test_hondt_02(self):
        data = {
            'type': 'HONDT',
            'options': [
                {'option':'ROSA','number':1,'votes': 100},
                {'option':'VERDE','number':2, 'votes': 80},
                {'option':'ROJO','number':3, 'votes': 70},
                {'option':'AMARILLO','number':4, 'votes': 5},
                {'option':'AZUL', 'number':5, 'votes': 3}
            ],
            'numEscanyos': 5
        }

        expected_result = [
            {'option':'ROSA','number':1,'votes': 100,'escanyos': 2},
            {'option':'VERDE','number':2, 'votes': 80,'escanyos': 2},
            {'option':'ROJO','number':3, 'votes': 70,'escanyos': 1},
            {'option':'AMARILLO','number':4, 'votes': 5,'escanyos': 0},
            {'option':'AZUL','number':5, 'votes': 3,'escanyos': 0}
        ]

        result = self.views.metodoHondt(data)

        self.assertEqual(result, expected_result)

    def test_hondt_03(self):
        data = {
            'type': 'HONDT',
            'options': [
                {'option':'A','number':1,'votes': 168000},
                {'option':'B','number':2, 'votes': 104000},
                {'option':'C','number':3, 'votes': 72000},
                {'option':'D','number':4, 'votes': 64000},
                {'option':'E','number':5, 'votes': 40000},
                {'option':'F','number':6, 'votes': 32000}
            ],
            'numEscanyos': 8
        }

        expected_result = [
            {'option':'A','number':1,'votes': 168000,'escanyos': 4},
            {'option':'B','number':2, 'votes': 104000,'escanyos': 2},
            {'option':'C','number':3, 'votes': 72000,'escanyos': 1},
            {'option':'D','number':4, 'votes': 64000,'escanyos': 1},
            {'option':'E','number':5, 'votes': 40000,'escanyos': 0},
            {'option':'F','number':6, 'votes': 32000,'escanyos': 0}
        ]

        result = self.views.metodoHondt(data)

        self.assertEqual(result, expected_result)
 

    #TEST IMPERIALI

    def test_imperiali_1(self):
        data = {
            'type': 'COCIENTE_IMPERIALI',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 391000 },
                { 'option': 'B', 'number': 2, 'votes': 311000 },
                { 'option': 'C', 'number': 3, 'votes': 184000 },
                { 'option': 'D', 'number': 4, 'votes': 73000 },
                { 'option': 'E', 'number': 5, 'votes': 27000 },
                { 'option': 'F', 'number': 6, 'votes': 12000 },
                { 'option': 'G', 'number': 7, 'votes': 2000 },
            ],
            'numEscanyos': 21,
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 391000, 'escanyos': 9},
            { 'option': 'B', 'number': 2, 'votes': 311000, 'escanyos': 7},
            { 'option': 'C', 'number': 3, 'votes': 184000, 'escanyos': 4},
            { 'option': 'D', 'number': 4, 'votes': 73000, 'escanyos': 1},
            { 'option': 'E', 'number': 5, 'votes': 27000, 'escanyos': 0},
            { 'option': 'F', 'number': 6, 'votes': 12000, 'escanyos': 0},
            { 'option': 'G', 'number': 7, 'votes': 2000, 'escanyos': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_imperiali_2(self):
        #Test 2: Más partidos que escaños a repartir
        data = {
            'type': 'COCIENTE_IMPERIALI',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 391000 },
                { 'option': 'B', 'number': 2, 'votes': 311000 },
                { 'option': 'C', 'number': 3, 'votes': 184000 },
                { 'option': 'D', 'number': 4, 'votes': 73000 },
                { 'option': 'E', 'number': 5, 'votes': 27000 },
                { 'option': 'F', 'number': 6, 'votes': 12000 },
                { 'option': 'G', 'number': 7, 'votes': 2000 },
            ],
            'numEscanyos': 6,
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 391000, 'escanyos': 3},
            { 'option': 'B', 'number': 2, 'votes': 311000, 'escanyos': 2},
            { 'option': 'C', 'number': 3, 'votes': 184000, 'escanyos': 1},
            { 'option': 'D', 'number': 4, 'votes': 73000, 'escanyos': 0},
            { 'option': 'E', 'number': 5, 'votes': 27000, 'escanyos': 0},
            { 'option': 'F', 'number': 6, 'votes': 12000, 'escanyos': 0},
            { 'option': 'G', 'number': 7, 'votes': 2000, 'escanyos': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_imperiali_3(self):
        #Test 3: Repartir 0 escaños entre todos los partidos
        data = {
            'type': 'COCIENTE_IMPERIALI',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 391000 },
                { 'option': 'B', 'number': 2, 'votes': 311000 },
                { 'option': 'C', 'number': 3, 'votes': 184000 },
                { 'option': 'D', 'number': 4, 'votes': 73000 },
                { 'option': 'E', 'number': 5, 'votes': 27000 },
                { 'option': 'F', 'number': 6, 'votes': 12000 },
                { 'option': 'G', 'number': 7, 'votes': 2000 },
            ],
            'numEscanyos': 0,
            
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 391000, 'escanyos': 0},
            { 'option': 'B', 'number': 2, 'votes': 311000, 'escanyos': 0},
            { 'option': 'C', 'number': 3, 'votes': 184000, 'escanyos': 0},
            { 'option': 'D', 'number': 4, 'votes': 73000, 'escanyos': 0},
            { 'option': 'E', 'number': 5, 'votes': 27000, 'escanyos': 0},
            { 'option': 'F', 'number': 6, 'votes': 12000, 'escanyos': 0},
            { 'option': 'G', 'number': 7, 'votes': 2000, 'escanyos': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_imperiali_4(self):
        #Test 4: Repartir escaños para partidos con 0 votos
        data = {
            'type': 'COCIENTE_IMPERIALI',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 0 },
                { 'option': 'B', 'number': 2, 'votes': 0 },
                { 'option': 'C', 'number': 3, 'votes': 0 },
                { 'option': 'D', 'number': 4, 'votes': 0 },
                { 'option': 'E', 'number': 5, 'votes': 0 },
                { 'option': 'F', 'number': 6, 'votes': 0 },
                { 'option': 'G', 'number': 7, 'votes': 0 },
            ],
            'numEscanyos': 10,
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 0, 'escanyos': 0},
            { 'option': 'B', 'number': 2, 'votes': 0, 'escanyos': 0},
            { 'option': 'C', 'number': 3, 'votes': 0, 'escanyos': 0},
            { 'option': 'D', 'number': 4, 'votes': 0, 'escanyos': 0},
            { 'option': 'E', 'number': 5, 'votes': 0, 'escanyos': 0},
            { 'option': 'F', 'number': 6, 'votes': 0, 'escanyos': 0},
            { 'option': 'G', 'number': 7, 'votes': 0, 'escanyos': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_imperiali_5(self):
        #Test 5: Repartir 0 escaños para partidos con 0 votos
        data = {
            'type': 'COCIENTE_IMPERIALI',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 0 },
                { 'option': 'B', 'number': 2, 'votes': 0 },
                { 'option': 'C', 'number': 3, 'votes': 0 },
                { 'option': 'D', 'number': 4, 'votes': 0 },
                { 'option': 'E', 'number': 5, 'votes': 0 },
                { 'option': 'F', 'number': 6, 'votes': 0 },
                { 'option': 'G', 'number': 7, 'votes': 0 },
            ],
            'numEscanyos': 0,
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 0, 'escanyos': 0},
            { 'option': 'B', 'number': 2, 'votes': 0, 'escanyos': 0},
            { 'option': 'C', 'number': 3, 'votes': 0, 'escanyos': 0},
            { 'option': 'D', 'number': 4, 'votes': 0, 'escanyos': 0},
            { 'option': 'E', 'number': 5, 'votes': 0, 'escanyos': 0},
            { 'option': 'F', 'number': 6, 'votes': 0, 'escanyos': 0},
            { 'option': 'G', 'number': 7, 'votes': 0, 'escanyos': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_imperiali_6(self):
        #Test 6: Partidos con el mismo numero de votos y con 20 escaños a repartir
        data = {
            'type': 'COCIENTE_IMPERIALI',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 10 },
                { 'option': 'B', 'number': 2, 'votes': 20 },
                { 'option': 'C', 'number': 3, 'votes': 60 },
                { 'option': 'D', 'number': 4, 'votes': 20 },
                { 'option': 'E', 'number': 5, 'votes': 1 },
                { 'option': 'F', 'number': 6, 'votes': 20 },
                { 'option': 'G', 'number': 7, 'votes': 0 },
            ],
            'numEscanyos': 20,
        }

        expected_result = [
            { 'option': 'C', 'number': 3, 'votes': 60, 'escanyos': 10},
            { 'option': 'B', 'number': 2, 'votes': 20, 'escanyos': 3},
            { 'option': 'D', 'number': 4, 'votes': 20, 'escanyos': 3},
            { 'option': 'F', 'number': 6, 'votes': 20, 'escanyos': 3},
            { 'option': 'A', 'number': 1, 'votes': 10, 'escanyos': 1},
            { 'option': 'E', 'number': 5, 'votes': 1, 'escanyos': 0},
            { 'option': 'G', 'number': 7, 'votes': 0, 'escanyos': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)



    def test_borda(self):
        data = {
            'type': 'BORDA',
            'options': [
                {'option': 'Popular','number':1, 'positions': [1,1,3,2],'votes': 0},
                {'option': 'Psoe','number':2, 'positions': [2,3,4,3],'votes': 0},
                {'option': 'Podemos','number':3, 'positions': [3,4,1,4],'votes': 0},
                {'option': 'Ciudadanos','number':4, 'positions': [4,2,2,1],'votes': 0},
            ]
        }

        expected_result = [
            {'option': 'Popular','number':1,'positions': [1,1,3,2], 'votes': 13},
            {'option': 'Psoe','number':2,'positions': [2,3,4,3], 'votes': 8},
            {'option': 'Podemos','number':3,'positions': [3,4,1,4], 'votes': 8},
            {'option': 'Ciudadanos','number':4,'positions': [4,2,2,1], 'votes': 11},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_borda2(self):
        data = {
            'type': 'BORDA',
            'options': [
                {'option': 'Popular','number':1, 'positions': [1],'votes': 0},
                {'option': 'Psoe','number':2, 'positions': [2],'votes': 0},
                {'option': 'Podemos','number':3, 'positions': [3],'votes': 0},
                {'option': 'Ciudadanos','number':4, 'positions': [4],'votes': 0},
            ]
        }

        expected_result = [
            {'option': 'Popular','number':1,'positions': [1], 'votes': 4},
            {'option': 'Psoe','number':2,'positions': [2], 'votes': 3},
            {'option': 'Podemos','number':3,'positions': [3], 'votes': 2},
            {'option': 'Ciudadanos','number':4,'positions': [4], 'votes': 1},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_borda3(self):
        data = {
            'type': 'BORDA',
            'options': [
                {'option': 'Popular','number':1,'positions': [],'votes': 0},
                {'option': 'Psoe','number':2,'positions': [],'votes': 0},
                {'option': 'Podemos','number':3,'positions': [],'votes': 0},
                {'option': 'Ciudadanos','number':4,'positions': [],'votes': 0},
            ]
        }

        expected_result = [
            {'option': 'Popular','number':1,'positions': [], 'votes': 0},
            {'option': 'Psoe','number':2,'positions': [], 'votes': 0},
            {'option': 'Podemos','number':3,'positions': [], 'votes': 0},
            {'option': 'Ciudadanos','number':4,'positions': [], 'votes': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)



    def test_borda4(self):
        data = {
            'type': 'BORDA',
            'options': [
                {'option': 'Popular','number':1, 'positions': [1,3,3,4],'votes': 0},
                {'option': 'Psoe','number':2, 'positions': [2,2,1,1],'votes': 0},
                {'option': 'Podemos','number':3, 'positions': [],'votes': 0},
                {'option': 'Ciudadanos','number':4, 'positions': [3,4,2,2],'votes': 0},
            ]
        }

        expected_result = [
            {'option': 'Popular','number':1,'positions': [1,3,3,4], 'votes': 0},
            {'option': 'Psoe','number':2,'positions': [2,2,1,1], 'votes': 0},
            {'option': 'Podemos','number':3,'positions': [], 'votes': 0},
            {'option': 'Ciudadanos','number':4,'positions': [3,4,2,2], 'votes': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)



