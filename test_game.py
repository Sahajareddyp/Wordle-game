import unittest
import server
from wordle import compare

class GameTests(unittest.TestCase):
    def setUp(self):
        self.client = server.app.test_client()

    def post(self, path, data):
        response = self.client.post(path, json=data)
        return response.status_code, response.get_json()

    def new(self, answer='plant'):
        _, result = self.post('/api/new', {})
        token = result['token']
        server.GAMES[token]['answer'] = answer
        return token

    def test_duplicates(self):
        self.assertEqual(compare('apple', 'plant'), '🟨 🟨 ⬜ 🟨 ⬜')
        self.assertEqual(compare('prope', 'plant'), '🟩 ⬜ ⬜ ⬜ ⬜')
        self.assertEqual(compare('llama', 'aloud'), '⬜ 🟩 🟨 ⬜ ⬜')

    def test_invalid_guesses_dont_consume_turn_and_uppercase_win(self):
        token = self.new()
        for guess in ['zzzzz', 'cat', 'abc12', 42]:
            self.assertEqual(self.post('/api/guess', {'token': token, 'guess': guess})[0], 400)
        self.assertEqual(server.GAMES[token]['guesses'], [])
        status, result = self.post('/api/guess', {'token': token, 'guess': 'PLANT'})
        self.assertEqual(status, 200)
        self.assertTrue(result['won'])
        self.assertEqual(result['attempts'], 1)
        self.assertEqual(self.post('/api/guess', {'token': token, 'guess': 'plant'})[0], 409)

    def test_five_attempt_loss_and_answer_secrecy(self):
        token = self.new()
        for attempt in range(5):
            _, result = self.post('/api/guess', {'token': token, 'guess': 'apple'})
            self.assertEqual(result['attempts'], attempt + 1)
            self.assertEqual(result['answer'], 'plant' if attempt == 4 else None)
        self.assertTrue(result['done'])
        self.assertFalse(result['won'])

    def test_separate_games_and_static_files(self):
        first, second = self.new(), self.new()
        self.post('/api/guess', {'token': first, 'guess': 'apple'})
        self.assertEqual(server.GAMES[second]['guesses'], [])
        for path in ['/', '/style.css', '/app.js', '/health']:
            with self.client.get(path) as response:
                self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post('/api/guess', {'token': 'missing', 'guess': 'apple'})[0], 410)
        self.assertEqual(self.client.get('/words.txt').status_code, 404)

    def test_malformed_and_large_requests(self):
        self.assertEqual(self.client.post('/api/guess', json=[]).status_code, 400)
        self.assertEqual(self.client.post('/api/guess', data='x' * 2048, content_type='application/json').status_code, 413)

if __name__ == '__main__':
    unittest.main()
