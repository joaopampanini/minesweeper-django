import json

from django.test import Client, TestCase
from django.urls import reverse


class testsGame(TestCase):

    fixtures = ['Game']

    def setUp(self):
        self.client = Client()

        self.get_valid_safe = {
            'id': 1, 'x': 1, 'y': 4}
        self.get_valid_bomb = {
            'id': 1, 'x': 4, 'y': 0}
        self.get_valid_win = {
            'id': 2, 'x': 5, 'y': 0}
        self.get_invalid_coord = {
            'id': 1, 'x': 9, 'y': 9}
        self.get_invalid_game = {
            'id': 0, 'x': 0, 'y': 0}
        self.post_create_game = {
            'x': 9, 'y': 9, 'mines': 10}
        self.delete_valid_game = {
            'id': 1}
        self.delete_invalid_game = {
            'id': 0}

    def test_get_valid_safe(self):
        url = reverse('game-click', kwargs=self.get_valid_safe)
        ret = self.client.get(url)
        ret = json.loads(ret.content)

        self.assertEqual(ret['result'], 'continue')
        self.assertEqual(
            ret['opened'],
            [[1, 4, 0], [2, 4, 1], [0, 4, 0], [0, 5, 1], [0, 3, 1],
             [1, 5, 1], [1, 3, 1], [2, 5, 1], [2, 3, 2]])

    def test_get_valid_bomb(self):
        url = reverse('game-click', kwargs=self.get_valid_bomb)
        ret = self.client.get(url)
        ret = json.loads(ret.content)

        self.assertEqual(ret['result'], 'game-over')
        self.assertEqual(
            ret['mines'],
            [[4, 7], [3, 3], [7, 7], [1, 2], [2, 0],
             [4, 3], [6, 3], [6, 7], [4, 0], [1, 6]])

    def test_get_valid_win(self):
        url = reverse('game-click', kwargs=self.get_valid_win)
        ret = self.client.get(url)
        ret = json.loads(ret.content)

        self.assertEqual(ret['result'], 'won')
        self.assertEqual(ret['opened'], [[5, 0, 1]])

    def test_get_invalid_coord(self):
        url = reverse('game-click', kwargs=self.get_invalid_coord)
        ret = self.client.get(url)
        ret = json.loads(ret.content)

        self.assertEqual(ret['result'], 'game-over')
        self.assertEqual(
            ret['mines'],
            [[4, 7], [3, 3], [7, 7], [1, 2], [2, 0],
             [4, 3], [6, 3], [6, 7], [4, 0], [1, 6]])

    def test_get_invalid_game(self):
        url = reverse('game-click', kwargs=self.get_invalid_game)
        ret = self.client.get(url)
        ret = json.loads(ret.content)

        self.assertEqual(ret['result'], 'game-over')
        self.assertEqual(ret['mines'], [])

    def test_post_create_game(self):
        url = reverse('new-game')
        ret = self.client.post(
            url, self.post_create_game, "application/json; charset=utf-8")
        ret = json.loads(ret.content)

        self.assertEqual(ret['game_id'], 3)

    def test_delete_valid_game(self):
        url = reverse('delete-game', kwargs=self.delete_valid_game)
        ret = self.client.delete(url)
        ret = json.loads(ret.content)

        self.assertEqual(ret['result'], 'ok')

    def test_delete_invalid_game(self):
        url = reverse('delete-game', kwargs=self.delete_invalid_game)
        ret = self.client.delete(url)
        ret = json.loads(ret.content)

        self.assertEqual(ret['result'], 'Invalid Game')
