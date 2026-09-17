# Word Garden

A responsive word game with a Python/Flask backend.

## Run locally on Windows

    python -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    .\.venv\Scripts\python.exe server.py

Open http://127.0.0.1:8000. Stop with Ctrl+C. Open that address rather than double-clicking index.html. The original terminal game still runs with `python wordle.py`.

## Deploy on Render

1. Upload the project files to a GitHub repository. Exclude `.venv`, `__pycache__`, and private configuration. The included `.gitignore` handles these when using Git.
2. In Render choose New > Web Service and connect that repository.
3. Choose Python 3 and the Free instance type.
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn --workers 1 --threads 1 --bind 0.0.0.0:$PORT server:app`
6. Deploy and use the resulting HTTPS address.

Alternatively use New > Blueprint with the included render.yaml, which defines these settings.

Keep one worker and one thread: game sessions live in memory. Restarting, redeploying, or free-service sleep clears ongoing games; players can choose New game. Refreshing the page starts a new game. This is suitable for a small friends-and-family project; scaling needs shared storage.

## Game and word lists

Five valid guesses per game. Type or tap letters, Enter submits, Backspace deletes. Invalid guesses cost no turns.

`words.txt` holds secret answers. `allowed_guesses.txt` holds accepted guesses; the web server also accepts every answer word. Your existing answer pool is preserved. The community guess list is not verified as the current NYT list. This is an independent game.

## Tests

    .\.venv\Scripts\python.exe -m unittest test_game.py
