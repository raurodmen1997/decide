from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods


class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None

    def test_identity(self):
        data = {
            'type': 'IDENTITY',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 2 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_imperiali_1(self):
        data = {
            'type': 'COCIENTE_IMPERIALI1',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 391000 },
                { 'option': 'B', 'number': 2, 'votes': 311000 },
                { 'option': 'C', 'number': 3, 'votes': 184000 },
                { 'option': 'D', 'number': 4, 'votes': 73000 },
                { 'option': 'E', 'number': 5, 'votes': 27000 },
                { 'option': 'F', 'number': 6, 'votes': 12000 },
                { 'option': 'G', 'number': 7, 'votes': 2000 },
            ]
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
            'type': 'COCIENTE_IMPERIALI2',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 391000 },
                { 'option': 'B', 'number': 2, 'votes': 311000 },
                { 'option': 'C', 'number': 3, 'votes': 184000 },
                { 'option': 'D', 'number': 4, 'votes': 73000 },
                { 'option': 'E', 'number': 5, 'votes': 27000 },
                { 'option': 'F', 'number': 6, 'votes': 12000 },
                { 'option': 'G', 'number': 7, 'votes': 2000 },
            ]
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
            'type': 'COCIENTE_IMPERIALI3',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 391000 },
                { 'option': 'B', 'number': 2, 'votes': 311000 },
                { 'option': 'C', 'number': 3, 'votes': 184000 },
                { 'option': 'D', 'number': 4, 'votes': 73000 },
                { 'option': 'E', 'number': 5, 'votes': 27000 },
                { 'option': 'F', 'number': 6, 'votes': 12000 },
                { 'option': 'G', 'number': 7, 'votes': 2000 },
            ]
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
            'type': 'COCIENTE_IMPERIALI4',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 0 },
                { 'option': 'B', 'number': 2, 'votes': 0 },
                { 'option': 'C', 'number': 3, 'votes': 0 },
                { 'option': 'D', 'number': 4, 'votes': 0 },
                { 'option': 'E', 'number': 5, 'votes': 0 },
                { 'option': 'F', 'number': 6, 'votes': 0 },
                { 'option': 'G', 'number': 7, 'votes': 0 },
            ]
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

    def test_imperiali_4(self):
        #Test 4: Repartir escaños para partidos con 0 votos
        data = {
            'type': 'COCIENTE_IMPERIALI4',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 0 },
                { 'option': 'B', 'number': 2, 'votes': 0 },
                { 'option': 'C', 'number': 3, 'votes': 0 },
                { 'option': 'D', 'number': 4, 'votes': 0 },
                { 'option': 'E', 'number': 5, 'votes': 0 },
                { 'option': 'F', 'number': 6, 'votes': 0 },
                { 'option': 'G', 'number': 7, 'votes': 0 },
            ]
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
            'type': 'COCIENTE_IMPERIALI5',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 0 },
                { 'option': 'B', 'number': 2, 'votes': 0 },
                { 'option': 'C', 'number': 3, 'votes': 0 },
                { 'option': 'D', 'number': 4, 'votes': 0 },
                { 'option': 'E', 'number': 5, 'votes': 0 },
                { 'option': 'F', 'number': 6, 'votes': 0 },
                { 'option': 'G', 'number': 7, 'votes': 0 },
            ]
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
            'type': 'COCIENTE_IMPERIALI6',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 10 },
                { 'option': 'B', 'number': 2, 'votes': 20 },
                { 'option': 'C', 'number': 3, 'votes': 60 },
                { 'option': 'D', 'number': 4, 'votes': 20 },
                { 'option': 'E', 'number': 5, 'votes': 1 },
                { 'option': 'F', 'number': 6, 'votes': 20 },
                { 'option': 'G', 'number': 7, 'votes': 0 },
            ]
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

