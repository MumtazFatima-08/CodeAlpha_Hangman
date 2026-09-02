const WORD_DATA = {
  EASY: [
    { word: 'PYTHON', category: 'Popular Programming Language', fact: "Named after Monty Python's Flying Circus, not the snake!" },
    { word: 'NETWORK', category: 'Interconnected Computer Systems', fact: 'A collection of nodes sharing data and resources securely.' }
  ],
  MEDIUM: [
    { word: 'DATABASE', category: 'Organized Collection of Data', fact: 'Structured digital storehouse for records, tables, and files.' },
    { word: 'SECURITY', category: 'Protection of Systems & Networks', fact: 'Safeguards digital infrastructure from cyber threats.' }
  ],
  HARD: [
    { word: 'ALGORITHM', category: 'Step-by-Step Logic Blueprint', fact: 'The foundational algorithm recipe guiding software execution.' }
  ]
};

const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
let difficulty = localStorage.getItem('hangmanDifficulty') || 'EASY';
let current = null;
let guessed = new Set();
let mistakes = 0;
let score = 100;
let gameOver = false;
let hints = { h1: false, h2: false, h3: false };
let stats = JSON.parse(localStorage.getItem('hangmanStats') || '{"games":0,"wins":0,"best":0}');

const $ = id => document.getElementById(id);

function saveStats(){ localStorage.setItem('hangmanStats', JSON.stringify(stats)); }

function updateHomeStats(){
  const rate = stats.games ? Math.round(stats.wins / stats.games * 100) : 0;
  $('homeStats').textContent = `Games: ${stats.games} • Wins: ${stats.wins} • Win Rate: ${rate}% • Best Score: ${stats.best}`;
}

function setDifficulty(value){
  difficulty = value;
  localStorage.setItem('hangmanDifficulty', value);

  document.querySelectorAll('.difficulty').forEach(btn => {
    const active = btn.dataset.difficulty === value;
    btn.classList.toggle('active', active);
    const label = btn.dataset.difficulty;
    btn.querySelector('strong').textContent = active ? `✓ ${label}` : label;
  });
}

function showGame(){
  $('homeScreen').classList.add('hidden');
  $('gameScreen').classList.remove('hidden');
  $('resultModal').classList.add('hidden');
}

function showHome(){
  $('resultModal').classList.add('hidden');
  $('gameScreen').classList.add('hidden');
  $('homeScreen').classList.remove('hidden');
  updateHomeStats();
}

function startGame(){
  current = WORD_DATA[difficulty][Math.floor(Math.random() * WORD_DATA[difficulty].length)];
  guessed = new Set();
  mistakes = 0;
  score = 100;
  gameOver = false;
  hints = {h1:false,h2:false,h3:false};

  $('score').textContent = score;
  $('mistakes').textContent = mistakes;
  $('difficultyBadge').textContent = difficulty;
  $('category').textContent = current.category;
  $('fact').textContent = 'Need a clue? Tap a boost below!';

  $('hint1').disabled = false;
  $('hint2').disabled = false;
  $('hint3').disabled = false;

  resetHangman();
  renderWord();
  renderKeyboard();
  showGame();
}

function resetHangman(){
  ['head','body','armL','armR','legL','legR'].forEach(id => $(id).style.visibility='hidden');
}

function drawMistake(){
  const parts=['head','body','armL','armR','legL','legR'];
  if(parts[mistakes-1]) $(parts[mistakes-1]).style.visibility='visible';
}

function renderWord(){
  $('word').innerHTML = current.word.split('').map(ch =>
    `<span class="letter">${guessed.has(ch) ? ch : '&nbsp;'}</span>`
  ).join('');
}

function renderKeyboard(){
  $('keyboard').innerHTML = '';

  letters.forEach(letter => {
    const b = document.createElement('button');
    b.className='key';
    b.textContent=letter;

    if(guessed.has(letter)){
      b.disabled=true;
      b.classList.add(current.word.includes(letter)?'correct':'wrong');
    }

    b.addEventListener('click',()=>guess(letter));
    $('keyboard').appendChild(b);
  });
}

function guess(letter){
  if(gameOver || guessed.has(letter)) return;

  guessed.add(letter);

  if(current.word.includes(letter)){
    score += 10;
    $('fact').textContent = 'Nice guess! Keep going. 🎯';
    $('word').classList.add('pop');
    setTimeout(()=>$('word').classList.remove('pop'),300);
  } else {
    score = Math.max(0, score - 10);
    mistakes++;
    $('mistakes').textContent=mistakes;
    $('gameScreen').classList.remove('shake');
    void $('gameScreen').offsetWidth;
    $('gameScreen').classList.add('shake');
    drawMistake();
  }

  $('score').textContent=score;
  renderWord();
  renderKeyboard();
  checkGame();
}

function checkGame(){
  const won = current.word.split('').every(ch => guessed.has(ch));
  if(won) finish(true);
  else if(mistakes >= 6) finish(false);
}

function finish(won){
  gameOver=true;
  stats.games++;

  if(won){
    score += 50;
    stats.wins++;
    stats.best=Math.max(stats.best,score);
    $('resultEmoji').textContent='🎉';
    $('resultTitle').textContent='YOU WIN!';
    $('resultTitle').style.color='var(--green)';
    $('resultText').textContent=`You uncovered ${current.word} and finished with ${score} points. Victory bonus +50!`;
  } else {
    stats.best=Math.max(stats.best,score);
    $('resultEmoji').textContent='💭';
    $('resultTitle').textContent='GAME OVER';
    $('resultTitle').style.color='var(--rust)';
    $('resultText').textContent=`The mystery word was ${current.word}. Your final score was ${score}. Give it another shot!`;
  }

  $('score').textContent=score;
  saveStats();
  $('resultModal').classList.remove('hidden');
}

function useHint(type){
  if(gameOver || hints[type]) return;

  if(type==='h1'){
    hints.h1=true;
    $('fact').textContent=current.fact;
    $('hint1').disabled=true;
  } else if(type==='h2'){
    if(score<10) return;
    hints.h2=true;
    score-=10;
    const first=current.word[0];
    guessed.add(first);
    $('fact').textContent=`First letter revealed: ${first}`;
    $('hint2').disabled=true;
    renderWord();
    renderKeyboard();
    checkGame();
  } else {
    if(score<20) return;
    const hidden=current.word.split('').filter(ch=>!guessed.has(ch));
    if(!hidden.length) return;

    hints.h3=true;
    score-=20;
    const reveal=hidden[Math.floor(Math.random()*hidden.length)];
    guessed.add(reveal);
    $('fact').textContent=`A mystery letter revealed: ${reveal}`;
    $('hint3').disabled=true;
    renderWord();
    renderKeyboard();
    checkGame();
  }

  $('score').textContent=score;
}

document.querySelectorAll('.difficulty').forEach(btn =>
  btn.addEventListener('click',()=>setDifficulty(btn.dataset.difficulty))
);

$('playBtn').addEventListener('click',startGame);
$('backBtn').addEventListener('click',showHome);
$('againBtn').addEventListener('click',startGame);
$('menuBtn').addEventListener('click',showHome);
$('hint1').addEventListener('click',()=>useHint('h1'));
$('hint2').addEventListener('click',()=>useHint('h2'));
$('hint3').addEventListener('click',()=>useHint('h3'));

document.addEventListener('keydown',e=>{
  if(/^[a-zA-Z]$/.test(e.key)) guess(e.key.toUpperCase());
});

setDifficulty(difficulty);
updateHomeStats();
