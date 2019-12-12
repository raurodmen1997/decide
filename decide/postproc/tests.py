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





    #Test recuento BORDA. Realizado por Raúl. VARIOS VOTANTES, EN ESTE CASO, 4 VOTANTES
    def test_borda(self):
        data = {
            'type': 'BORDA',
            'options': [
                {'option': 'Popular', 'positions': [1,1,3,2]},
                {'option': 'Psoe', 'positions': [2,3,4,3]},
                {'option': 'Podemos', 'positions': [3,4,1,4]},
                {'option': 'Ciudadanos', 'positions': [4,2,2,1]},
            ]
        }

        expected_result = {
            'Popular': 13,
            'Psoe': 8,
            'Podemos': 8,
            'Ciudadanos': 11
            }
        

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    #Test recuento BORDA. Realizado por Raúl. SOLO UN VOTANTE
    def test_borda2(self):
        data = {
            'type': 'BORDA',
            'options': [
                {'option': 'Popular', 'positions': [1]},
                {'option': 'Psoe', 'positions': [2]},
                {'option': 'Podemos', 'positions': [3]},
                {'option': 'Ciudadanos', 'positions': [4]},
            ]
        }

        expected_result = {
            'Popular': 4,
            'Psoe': 3,
            'Podemos': 2,
            'Ciudadanos': 1
            }
        

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    #Test recuento BORDA. Realizado por Raúl. SI NADIE HA VOTADO A NINGÚN REPRESENTANTE
    def test_borda3(self):
        data = {
            'type': 'BORDA',
            'options': [
                {'option': 'Popular', 'positions': []},
                {'option': 'Psoe', 'positions': []},
                {'option': 'Podemos', 'positions': []},
                {'option': 'Ciudadanos', 'positions': []},
            ]
        }

        expected_result = {}
        

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    #Test recuento BORDA. Realizado por Raúl. TODOS LOS VOTANTES NO HAN VOTADO A UN REPRESENTANTE,
    #EN ESTE CASO, AL REPRESENTANTE 'Podemos'
    def test_borda4(self):
        data = {
            'type': 'BORDA',
            'options': [
                {'option': 'Popular', 'positions': [1,3,3,4]},
                {'option': 'Psoe', 'positions': [2,2,1,1]},
                {'option': 'Podemos', 'positions': []},
                {'option': 'Ciudadanos', 'positions': [3,4,2,2]},
            ]
        }

        expected_result = {}
        

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)