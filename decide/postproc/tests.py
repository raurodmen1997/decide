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


    def test_hondt_01(self):
        data = {
            'type': 'HONDT',
            'options': [
                {'option':'A','votes': 340000},
                {'option':'B', 'votes': 280000},
                {'option':'C', 'votes': 160000},
                {'option':'D', 'votes': 60000},
                {'option':'E', 'votes': 15000}
            ],
            'escañosTotales': 7
        }

        expected_result = [
            {'option':'A','numEscaños': 3},
            {'option':'B','numEscaños': 3},
            {'option':'C','numEscaños': 1},
            {'option':'D','numEscaños': 0},
            {'option':'E','numEscaños': 0}
        ]

        result = self.views.metodoHondt(data)

        self.assertEqual(result, expected_result)


    def test_hondt_02(self):
        data = {
            'type': 'HONDT',
            'options': [
                {'option':'ROSA','votes': 100},
                {'option':'VERDE', 'votes': 80},
                {'option':'ROJO', 'votes': 70},
                {'option':'AMARILLO', 'votes': 5},
                {'option':'AZUL', 'votes': 3}
            ],
            'escañosTotales': 5
        }

        expected_result = [
            {'option':'ROSA','numEscaños': 2},
            {'option':'VERDE','numEscaños': 2},
            {'option':'ROJO','numEscaños': 1},
            {'option':'AMARILLO','numEscaños': 0},
            {'option':'AZUL','numEscaños': 0}
        ]

        result = self.views.metodoHondt(data)

        self.assertEqual(result, expected_result)


    def test_hondt_03(self):
        data = {
            'type': 'HONDT',
            'options': [
                {'option':'A','votes': 168000},
                {'option':'B', 'votes': 104000},
                {'option':'C', 'votes': 72000},
                {'option':'D', 'votes': 64000},
                {'option':'E', 'votes': 40000},
                {'option':'F', 'votes': 32000}
            ],
            'escañosTotales': 8
        }

        expected_result = [
            {'option':'A','numEscaños': 4},
            {'option':'B','numEscaños': 2},
            {'option':'C','numEscaños': 1},
            {'option':'D','numEscaños': 1},
            {'option':'E','numEscaños': 0},
            {'option':'F','numEscaños': 0}
        ]

        result = self.views.metodoHondt(data)

        self.assertEqual(result, expected_result)