# 🌿 Word Garden

A small, Wordle-inspired game built with Python and Flask. Find a hidden five-letter word in five guesses, using colored clues to guide your next move.

**[Play Word Garden →](https://word-garden-1jdj.onrender.com)**

No account or installation needed to play. The demo runs on Render's free tier, so the first visit after a period of inactivity may take about a minute to load.

## How to play

1. Type a five-letter word or use the on-screen keyboard.
2. Press **Enter** to submit your guess. Use **Backspace** to delete a letter.
3. Use the feedback to find the answer within five valid guesses.

| Tile | Meaning |
| --- | --- |
| 🟩 Green | Correct letter in the correct position |
| 🟨 Yellow | The letter appears in the answer, but in another position |
| ⬜ Gray on the website | No unused occurrence of that letter remains in the answer |

Green matches take priority over yellow matches. Repeated letters receive credit only as many times as they appear in the answer.

Invalid words do not use an attempt. Select **New game** to start again with a randomly selected answer. This is free play, rather than a shared daily puzzle; answers can repeat.

## Features

- Responsive layout for desktop and mobile
- Physical and on-screen keyboard support
- Colored keyboard clues that preserve each letter's strongest match
- Server-side word validation and duplicate-letter scoring
- Win and loss messages, instructions, and replay
- Original Python terminal version included

## About the project

Word Garden started as a terminal game for learning Python: loops, functions, lists, input validation, and algorithm design. The web version uses the same comparison function behind a browser interface.

The scoring algorithm makes two passes: first reserve exact matches, then check the remaining letters for misplaced matches. This prevents a single answer letter from being counted twice.

## How it works

```text
Browser: HTML + CSS + JavaScript
                ↓ sends a guess and game token
Flask: validates the guess and calls the Python scoring function
                ↓ returns colors and game status
Browser: updates the board and keyboard
```

The server selects and stores the secret answer. Each game has its own randomly generated token, and the answer is returned to the browser only when that game ends.

## Run locally

Use Python 3.12 to match the included Render configuration.

Clone the repository and enter its folder:

```bash
git clone https://github.com/Sahajareddyp/Wordle-game.git
cd Wordle-game
```

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe server.py
```

### macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python server.py
```

Open **http://127.0.0.1:8000** in your browser. Keep the terminal running while you play; press **Ctrl+C** to stop the server. Open the server address rather than double-clicking `index.html`.

To play the original terminal version from the project folder:

```bash
python wordle.py
```

On macOS/Linux, use `python3` if your system does not provide a `python` command. The terminal version uses only Python's standard library.

## Project files

| File | Purpose |
| --- | --- |
| `wordle.py` | Word loading, shared scoring logic, and terminal game |
| `server.py` | Flask routes, validation, and in-memory game sessions |
| `index.html` | Page structure and instructions |
| `style.css` | Responsive layout, colors, and tile styling |
| `app.js` | Keyboard input, API requests, and display updates |
| `words.txt` | Small, curated pool of possible secret answers |
| `allowed_guesses.txt` | Larger dictionary of accepted guesses |
| `requirements.txt` | Python web dependencies |
| `render.yaml` | Render deployment configuration |
| `test_game.py` | Automated scoring and API tests |

## Word lists and attribution

Secret answers come from `words.txt`. Accepted guesses come from `allowed_guesses.txt`; the web version also accepts every word in the answer pool.

The guess list was downloaded from [Tab Atkins's community Wordle word list](https://github.com/tabatkins/wordle-list), whose author describes it as extracted from the game's source. It is not verified as the current New York Times dictionary. See the source repository for its licensing information.

To expand the answer pool, add familiar five-letter English words to `words.txt`, one lowercase word per line, then restart or redeploy the server.

Word Garden is an independent learning project, not affiliated with or endorsed by The New York Times.

## Tests

After installing the dependencies, run:

```powershell
# Windows
.\.venv\Scripts\python.exe -m unittest test_game.py
```

```bash
# macOS / Linux
.venv/bin/python -m unittest test_game.py
```

The tests cover duplicate letters, invalid guesses not consuming turns, uppercase input, winning, the five-attempt limit, answer disclosure, separate game sessions, static routes, and malformed requests.

## Deploy on Render

The repository includes a Blueprint configuration in `render.yaml`:

1. Push the project to your GitHub repository.
2. In the [Render Dashboard](https://dashboard.render.com/), choose **New → Blueprint**.
3. Connect your repository and select its branch.
4. Keep the Blueprint path as `render.yaml`.
5. Review the service and its **Free** plan, then deploy.
6. Open the HTTPS address assigned to the web service.

The configuration installs dependencies with:

```bash
pip install -r requirements.txt
```

It starts the Flask application with Gunicorn on Render's Linux environment:

```bash
gunicorn --workers 1 --threads 1 --bind 0.0.0.0:$PORT server:app
```

For platform details, see [Render's Blueprint guide](https://render.com/docs/infrastructure-as-code) and [free service limitations](https://render.com/docs/free).

### Current limitations

- Game sessions live in memory. A server restart, redeploy, or free-service shutdown clears unfinished games; choose **New game** to continue.
- Refreshing the page starts a new game. There are no saved statistics or accounts.
- The server retains up to 1,000 game sessions, removing the oldest when the limit is reached.
- Keep the configured **one worker and one thread** while using in-memory sessions. Multiple workers or instances would need shared game storage.
- The answer pool is intentionally small and separate from the much larger guess dictionary.

## Feedback

Found a bug or have an idea? [Open an issue](https://github.com/Sahajareddyp/Wordle-game/issues) with what happened, what you expected, and steps to reproduce it.
