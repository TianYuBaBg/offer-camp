/* 求职自习室 · Offer Camp
   三件小事的状态存在 localStorage 里，按天分开存。
   日志直接写在这个文件里，改完 push，Cloudflare Pages 会自动重新发布。 */

const START = new Date('2026-10-29T00:00:00+08:00');

const LOGS = [
  { day: 'D0', date: '2026.10.29', text: '把这个站搭起来：只放四样东西——词、题、项目、课。以后每天在这里留一行。' },
  { day: 'D-1', date: '2026.10.28', text: '简历改到 v2：删掉求职地点和南京涵华那段，补上作品链接与学信网报告。' },
  { day: 'D-2', date: '2026.10.27', text: '题库 179 道，挑出 47 道保命题，每题配了一段能直接照念的口播稿。' },
  { day: 'D-3', date: '2026.10.26', text: '谐音表补到 326 个词，给每个词挂上真人发音链接——读得出，才听得懂别人问什么。' },
  { day: 'D-4', date: '2026.10.25', text: '秒杀项目骨架跑通：建库、Redis 预扣、RabbitMQ 落单。先能跑，再谈漂亮。' }
];

const pad = n => String(n).padStart(2, '0');
const dateKey = d => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;

function renderHeader() {
  const now = new Date();
  const today = document.getElementById('today');
  today.textContent = `${now.getFullYear()}.${pad(now.getMonth() + 1)}.${pad(now.getDate())}`;

  const dayNo = document.getElementById('dayNo');
  const diff = Math.floor((new Date(dateKey(now)) - new Date(dateKey(START))) / 86400000) + 1;
  dayNo.textContent = diff >= 1 && diff <= 14 ? diff : (diff < 1 ? '未开始' : '已过 14 天');
}

function loadState() {
  try { return JSON.parse(localStorage.getItem('oc:' + dateKey(new Date())) || '{}'); }
  catch (e) { return {}; }
}

function saveState(state) {
  try { localStorage.setItem('oc:' + dateKey(new Date()), JSON.stringify(state)); } catch (e) {}
}

function bindTasks() {
  const boxes = [...document.querySelectorAll('.tri input[data-task]')];
  const line = document.getElementById('stampLine');
  const state = loadState();

  const refresh = () => {
    const done = boxes.filter(b => b.checked).length;
    if (done === boxes.length) {
      line.textContent = '今天三件事都做完了。翻篇，明天见。';
      line.classList.add('done');
    } else {
      line.textContent = done ? `还差 ${boxes.length - done} 件，别急，从最短的那件开始。` : '三件事都勾上，今天就翻篇。';
      line.classList.remove('done');
    }
  };

  boxes.forEach(b => {
    b.checked = !!state[b.dataset.task];
    b.addEventListener('change', () => {
      state[b.dataset.task] = b.checked ? 1 : 0;
      saveState(state);
      refresh();
    });
  });
  refresh();
}

function renderLogs() {
  const list = document.getElementById('logList');
  if (!list) return;
  list.innerHTML = LOGS.map(l => `
    <li>
      <div>
        <span class="l-meta">${l.day} · ${l.date}</span>
        <p class="l-text">${l.text}</p>
      </div>
    </li>`).join('');
}

function revealBlocks() {
  const blocks = document.querySelectorAll('.block');
  if (!('IntersectionObserver' in window)) {
    blocks.forEach(b => b.classList.add('in'));
    return;
  }
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.12 });
  blocks.forEach(b => io.observe(b));
}

renderHeader();
renderLogs();
bindTasks();
revealBlocks();
