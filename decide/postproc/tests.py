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

    ## Tests realizados modificando la variable (temporal) 'numSeats' con los valores: 2,3,5,12,21

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
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 245034, 'seats': 4 },
            { 'option': 'Option 2', 'number': 2, 'votes': 98562, 'seats': 2 },
            { 'option': 'Option 3', 'number': 3, 'votes': 391000, 'seats': 7 },
            { 'option': 'Option 4', 'number': 4, 'votes': 200001, 'seats': 3 },
            { 'option': 'Option 5', 'number': 5, 'votes': 312000, 'seats': 5 },
            { 'option': 'Option 6', 'number': 6, 'votes': 20145, 'seats': 0 },
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
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 2510, 'seats': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 300, 'seats': 0 },
            { 'option': 'Option 3', 'number': 3, 'votes': 245034, 'seats': 11 },
            { 'option': 'Option 4', 'number': 4, 'votes': 200001, 'seats': 9 },
            { 'option': 'Option 5', 'number': 5, 'votes': 14, 'seats': 0 },
            { 'option': 'Option 6', 'number': 6, 'votes': 20145, 'seats': 1 },
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
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 2510, 'seats': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 6540, 'seats': 4 },
            { 'option': 'Option 3', 'number': 3, 'votes': 0, 'seats': 0 },
            { 'option': 'Option 4', 'number': 4, 'votes': 12046, 'seats': 6 },
            { 'option': 'Option 5', 'number': 5, 'votes': 14, 'seats': 0 },
            { 'option': 'Option 6', 'number': 6, 'votes': 20145, 'seats': 10 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
