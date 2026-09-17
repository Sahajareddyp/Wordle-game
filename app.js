const board = document.getElementById('board');
const message = document.getElementById('message');
const keyboard = document.getElementById('keyboard');
const newButton = document.getElementById('new-game');
const dialog = document.getElementById('instructions');
let token, current = '', history = [], busy = false, finished = false;
const keys = {}, rank = { absent: 1, present: 2, correct: 3 };
function tell(text, type = '') { message.textContent = text; message.className = type; }
function draw() {
  board.replaceChildren();
  for (let row = 0; row < 5; row++) {
    const line = document.createElement('div');
    line.className = 'row' + (row === history.length && !finished ? ' active' : '');
    const letters = history[row]?.guess || (row === history.length ? current : '');
    for (let col = 0; col < 5; col++) {
      const tile = document.createElement('div'), color = history[row]?.colors[col];
      tile.className = 'tile' + (color ? ' ' + color : letters[col] ? ' filled' : '');
      tile.textContent = (letters[col] || '').toUpperCase();
      tile.setAttribute('aria-label', letters[col] ? `${letters[col]}, ${color || 'not submitted'}` : 'empty');
      line.append(tile);
    }
    board.append(line);
  }
  document.getElementById('counter').textContent = finished ? 'GAME COMPLETE' : `GUESS ${history.length + 1} / 5`;
}
async function request(path, data = {}) {
  const response = await fetch(path, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) });
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || 'Something went wrong. Try again.');
  return result;
}
async function start() {
  if (busy) return;
  busy = true; newButton.disabled = true; tell('Picking a fresh word…');
  try {
    const game = await request('/api/new');
    token = game.token; current = ''; history = []; finished = false;
    Object.values(keys).forEach(key => { key.className = 'key' + (key.dataset.wide ? ' wide' : ''); key.dataset.color = ''; });
    draw(); tell('Plant your first five-letter word.');
  } catch (error) { tell('Could not connect. Start the Python server, then choose New game.', 'error'); }
  finally { busy = false; newButton.disabled = false; }
}
async function input(key) {
  if (busy || finished || !token || dialog.open) return;
  if (key === 'BACKSPACE') { current = current.slice(0, -1); draw(); return; }
  if (/^[A-Z]$/.test(key)) { if (current.length < 5) { current += key; draw(); } return; }
  if (key !== 'ENTER') return;
  if (current.length !== 5) { tell('Enter all five letters first.', 'error'); return; }
  busy = true; newButton.disabled = true;
  try {
    const result = await request('/api/guess', { token, guess: current });
    history.push(result); current = ''; finished = result.done;
    result.guess.split('').forEach((letter, i) => {
      const keyButton = keys[letter.toUpperCase()], color = result.colors[i];
      if ((rank[color] || 0) > (rank[keyButton.dataset.color] || 0)) {
        keyButton.dataset.color = color; keyButton.className = 'key ' + color;
      }
    });
    draw();
    if (result.won) tell(`Beautifully done! You found it in ${result.attempts} ${result.attempts === 1 ? 'guess' : 'guesses'}.`, 'success');
    else if (result.done) tell(`The word was ${result.answer.toUpperCase()}. A fresh start awaits.`);
    else tell(`${5 - result.attempts} ${5 - result.attempts === 1 ? 'chance' : 'chances'} left. Follow the clues.`);
  } catch (error) {
    tell(error instanceof TypeError ? 'Connection lost. Try again or start a new game.' : error.message, 'error');
    const row = board.querySelector('.active');
    if (row) { row.classList.remove('shake'); void row.offsetWidth; row.classList.add('shake'); }
  } finally { busy = false; newButton.disabled = false; }
}
['QWERTYUIOP'.split(''), 'ASDFGHJKL'.split(''), ['ENTER', ...'ZXCVBNM', 'BACKSPACE']].forEach(letters => {
  const row = document.createElement('div'); row.className = 'keyboard-row';
  letters.forEach(letter => {
    const key = document.createElement('button'); key.type = 'button';
    key.className = 'key' + (letter.length > 1 ? ' wide' : '');
    if (letter.length > 1) key.dataset.wide = 'true';
    key.textContent = letter === 'BACKSPACE' ? '⌫' : letter;
    key.setAttribute('aria-label', letter === 'BACKSPACE' ? 'Delete letter' : letter);
    key.addEventListener('click', () => { input(letter); key.blur(); }); keys[letter] = key; row.append(key);
  }); keyboard.append(row);
});
document.addEventListener('keydown', event => {
  if (event.ctrlKey || event.metaKey || event.altKey || dialog.open) return;
  if (event.target instanceof HTMLButtonElement && (event.key === 'Enter' || event.key === ' ')) return;
  const key = event.key.toUpperCase();
  if (/^[A-Z]$/.test(key) || key === 'ENTER' || key === 'BACKSPACE') { event.preventDefault(); input(key); }
});
document.getElementById('help').onclick = () => dialog.showModal();
document.getElementById('close-help').onclick = () => dialog.close();
document.getElementById('lets-play').onclick = () => dialog.close();
newButton.onclick = () => { start(); newButton.blur(); };
draw(); start();
