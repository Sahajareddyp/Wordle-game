"""Local: python server.py. Hosted: gunicorn --workers 1 server:app."""
import secrets
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
from werkzeug.exceptions import HTTPException
from word_garden import clean_guesses, clean_words, compare, random_word

ROOT = Path(__file__).resolve().parent
ALLOWED = set(clean_guesses) | set(clean_words)
GAMES = {}
COLORS = {"🟩": "correct", "🟨": "present", "⬜": "absent"}
app = Flask(__name__, static_folder=None)
app.config['MAX_CONTENT_LENGTH'] = 1024

@app.after_request
def headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    if request.path.startswith('/api/'):
        response.headers['Cache-Control'] = 'no-store'
    return response

@app.errorhandler(HTTPException)
def http_error(error):
    return jsonify(error=error.description), error.code

@app.get('/')
def index():
    return send_from_directory(ROOT, 'index.html')

@app.get('/style.css')
def css():
    return send_from_directory(ROOT, 'style.css')

@app.get('/app.js')
def javascript():
    return send_from_directory(ROOT, 'app.js')

@app.get('/health')
def health():
    return jsonify(status='ok')

@app.post('/api/new')
def new_game():
    if len(GAMES) >= 1000:
        del GAMES[next(iter(GAMES))]
    token = secrets.token_urlsafe(24)
    GAMES[token] = {'answer': random_word(clean_words), 'guesses': [], 'done': False}
    return jsonify(token=token)

@app.post('/api/guess')
def guess_word():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error='Invalid request'), 400
    token = data.get('token')
    game = GAMES.get(token) if isinstance(token, str) else None
    if not game:
        return jsonify(error='Game expired. Choose New game to begin.'), 410
    guess = data.get('guess', '')
    if not isinstance(guess, str):
        return jsonify(error='Enter a five-letter word.'), 400
    guess = guess.lower().strip()
    if game['done']:
        return jsonify(error='This game is finished. Start a new one.'), 409
    if len(guess) != 5 or not guess.isascii() or not guess.isalpha():
        return jsonify(error='Enter all five letters first.'), 400
    if guess not in ALLOWED:
        return jsonify(error='Not in the word list. Try another word.'), 400
    game['guesses'].append(guess)
    won = guess == game['answer']
    game['done'] = won or len(game['guesses']) == 5
    return jsonify(guess=guess, colors=[COLORS[c] for c in compare(guess, game['answer']).split()],
                   attempts=len(game['guesses']), won=won, done=game['done'],
                   answer=game['answer'] if game['done'] else None)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=False, threaded=False)
