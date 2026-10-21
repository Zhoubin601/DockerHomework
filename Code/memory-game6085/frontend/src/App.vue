<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref } from 'vue'
import { ArrowDown, ArrowRight, Check, CheckCheck, ChevronRight, CircleHelp, Clock3, Flower2, Leaf, LoaderCircle, Maximize2, MousePointer2, Pause, Play, RefreshCw, RotateCcw, Sparkles, Sprout, Trophy, Volume2, VolumeX, X } from 'lucide-vue-next'
import PlantArt from './components/PlantArt.vue'
import { api, post } from './api'

const modes = [
  { id: 'easy', label: '轻松', pairs: 6, size: '3 × 4', description: '先从一小片花园开始' },
  { id: 'normal', label: '标准', pairs: 8, size: '4 × 4', description: '刚刚好的记忆小挑战' },
  { id: 'hard', label: '挑战', pairs: 12, size: '4 × 6', description: '探索更大一片花园' },
]
const names = { sprout: '嫩芽', tulip: '郁金香', daisy: '雏菊', cactus: '仙人掌', leaf: '叶子', cherry: '樱桃', mushroom: '蘑菇', orange: '橘子', clover: '四叶草', sunflower: '向日葵', acorn: '橡果', lavender: '薰衣草' }
const mode = ref('normal')
const currentMode = computed(() => modes.find(item => item.id === mode.value))
const game = ref(null)
const busy = ref(false)
const error = ref('')
const notice = ref('')
const ranking = ref({ scores: [], total: 0, bestDurationMs: null })
const rankMode = ref('normal')
const rankState = ref('loading')
const rankError = ref('')
const displayElapsed = ref(0)
const sound = ref(false)
const rulesDialog = ref(null)
const confirmDialog = ref(null)
const winDialog = ref(null)
const nicknameInput = ref(null)
const nickname = ref('')
const saveBusy = ref(false)
const saved = ref(false)
const saveError = ref('')
const highlightScore = ref(null)
const boardElement = ref(null)
const gameSection = ref(null)
let pendingAction = null
let clockTick
let closeMismatch
let syncPoint = 0
let audio
let rankRequest = 0
let mounted = true

const ready = computed(() => !game.value)
const paused = computed(() => game.value?.status === 'paused')
const completed = computed(() => game.value?.status === 'completed')
const matched = computed(() => game.value?.matchedPairs || 0)
const totalPairs = computed(() => game.value?.totalPairs || currentMode.value.pairs)
const cards = computed(() => game.value?.cards || Array.from({ length: currentMode.value.pairs * 2 }, (_, index) => ({ index, symbol: null, matched: false })))
const progress = computed(() => `${Math.round(matched.value / totalPairs.value * 100)}%`)
const accuracy = computed(() => game.value?.moves ? `${Math.round(matched.value / game.value.moves * 100)}%` : '—')

function formatTime(ms, decimal = false) {
  if (ms == null) return '—'
  const seconds = Math.floor(ms / 1000)
  const time = `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`
  return decimal ? `${time}.${Math.floor(ms % 1000 / 100)}` : time
}

function setGame(value) {
  game.value = value
  displayElapsed.value = value.elapsedMs
  syncPoint = performance.now()
}

function playTone(success = false) {
  if (!sound.value) return
  try {
    audio ||= new AudioContext()
    void audio.resume()
    const oscillator = audio.createOscillator()
    const gain = audio.createGain()
    oscillator.type = 'sine'
    oscillator.frequency.setValueAtTime(success ? 660 : 440, audio.currentTime)
    if (success) oscillator.frequency.exponentialRampToValueAtTime(880, audio.currentTime + .13)
    gain.gain.setValueAtTime(.055, audio.currentTime)
    gain.gain.exponentialRampToValueAtTime(.001, audio.currentTime + .2)
    oscillator.connect(gain).connect(audio.destination)
    oscillator.start()
    oscillator.stop(audio.currentTime + .22)
  } catch { /* 浏览器不支持音频时保持静音，不影响游戏。 */ }
}

async function fetchRanking(difficulty = rankMode.value) {
  rankMode.value = difficulty
  const request = ++rankRequest
  rankState.value = 'loading'
  rankError.value = ''
  try {
    const result = await api(`/leaderboard?difficulty=${difficulty}`)
    if (!mounted || request !== rankRequest) return
    ranking.value = result
    rankState.value = 'loaded'
  } catch (failure) {
    if (!mounted || request !== rankRequest) return
    rankState.value = 'error'
    rankError.value = failure.message
  }
}

async function startGame(difficulty = mode.value) {
  if (busy.value) return
  busy.value = true
  error.value = ''
  try {
    const previousId = game.value?.id
    const result = await post('/games', { difficulty })
    clearTimeout(closeMismatch)
    mode.value = difficulty
    setGame(result)
    saved.value = false
    saveError.value = ''
    notice.value = '花园已准备好。翻开第一张卡牌开始计时。'
    if (previousId) void api(`/games/${previousId}`, { method: 'DELETE' }).catch(() => {})
    await nextTick()
    boardElement.value?.querySelector('button')?.focus({ preventScroll: true })
  } catch (failure) { error.value = failure.message }
  finally { busy.value = false }
}

function askRestart(difficulty = mode.value) {
  if (busy.value) return
  if (!game.value || completed.value) {
    mode.value = difficulty
    if (game.value) void startGame(difficulty)
    return
  }
  pendingAction = () => startGame(difficulty)
  confirmDialog.value?.showModal()
}

function confirmRestart() {
  confirmDialog.value.close()
  pendingAction?.()
  pendingAction = null
}

async function syncGame() {
  const id = game.value?.id
  if (!id || busy.value) return
  try {
    const state = await api(`/games/${id}`)
    if (game.value?.id === id) {
      setGame(state)
      error.value = ''
    }
  } catch (failure) { error.value = failure.message }
}

async function flip(index) {
  if (ready.value || paused.value || completed.value || busy.value || game.value.lockedForMs > 0) return
  const card = game.value.cards[index]
  if (card.matched || card.symbol) return
  busy.value = true
  error.value = ''
  try {
    const before = matched.value
    const state = await post(`/games/${game.value.id}/flip`, { index })
    setGame(state)
    playTone(matched.value > before)
    if (state.lockedForMs > 0) {
      notice.value = '这两张不一样，再记一下它们的位置。'
      clearTimeout(closeMismatch)
      closeMismatch = setTimeout(syncGame, state.lockedForMs + 80)
    } else if (matched.value > before) {
      notice.value = `配对成功！已经找到 ${matched.value} 对植物。`
    } else { notice.value = '再翻一张，寻找相同的植物。' }
    if (completed.value) {
      notice.value = '花园收集完成！可以保存本局成绩。'
      await nextTick()
      winDialog.value?.showModal()
      nicknameInput.value?.focus()
    }
  } catch (failure) {
    error.value = failure.message
    if (failure.status === 409) setTimeout(syncGame, 950)
  } finally { busy.value = false }
}

async function togglePause() {
  if (!game.value || busy.value || completed.value) return
  busy.value = true
  error.value = ''
  try {
    const state = await post(`/games/${game.value.id}/pause`, { paused: !paused.value })
    clearTimeout(closeMismatch)
    setGame(state)
    if (state.lockedForMs > 0) closeMismatch = setTimeout(syncGame, state.lockedForMs + 80)
    notice.value = paused.value ? '休息一下，花园会等你回来。' : '欢迎回来，继续寻找植物吧。'
    if (!paused.value) {
      await nextTick()
      boardElement.value?.querySelector('button:not(:disabled)')?.focus({ preventScroll: true })
    }
  } catch (failure) { error.value = failure.message }
  finally { busy.value = false }
}

async function saveScore() {
  if (saveBusy.value || saved.value) return
  saveError.value = ''
  const clean = nickname.value.trim()
  if (!clean || [...clean].length > 16) {
    saveError.value = '给自己起个 1–16 字的昵称吧。'
    nicknameInput.value?.focus()
    return
  }
  saveBusy.value = true
  try {
    const result = await post(`/games/${game.value.id}/score`, { nickname: clean })
    saved.value = true
    highlightScore.value = result.id
    try { localStorage.setItem('garden-nickname', clean) } catch { /* 隐私模式不影响提交。 */ }
    await fetchRanking(mode.value)
    notice.value = '成绩已保存，排行榜里也有你的足迹了。'
  } catch (failure) { saveError.value = failure.message }
  finally { saveBusy.value = false }
}

function playAgain() {
  if (saveBusy.value) return
  winDialog.value.close()
  void startGame()
}

function scrollToGame() { gameSection.value?.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' }) }

function handleVisibility() { if (document.visibilityState === 'visible') void syncGame() }

onMounted(() => {
  try { nickname.value = localStorage.getItem('garden-nickname') || '' } catch { /* 本地存储可选。 */ }
  void fetchRanking()
  clockTick = setInterval(() => {
    if (game.value?.status === 'playing' && game.value.timerRunning) {
      displayElapsed.value = game.value.elapsedMs + performance.now() - syncPoint
    }
  }, 100)
  document.addEventListener('visibilitychange', handleVisibility)
})

onUnmounted(() => {
  mounted = false
  clearInterval(clockTick)
  clearTimeout(closeMismatch)
  document.removeEventListener('visibilitychange', handleVisibility)
  void audio?.close()
})
</script>

<template>
  <a class="skip-link" href="#game">跳到游戏</a>
  <header class="site-header">
    <a href="#" class="brand" aria-label="记忆花园首页">
      <span class="brand-icon"><PlantArt name="mark"/></span>
      <span class="brand-text">记忆花园<small>MEMORY GARDEN</small></span>
    </a>
    <nav class="navigation" aria-label="主导航">
      <a href="#game" class="nav-active">开始游戏<span/></a>
      <a href="#leaderboard">花园榜单</a>
      <button class="nav-help" @click="rulesDialog.showModal()"><CircleHelp :size="17"/>玩法指南</button>
    </nav>
    <span class="header-note"><span class="status-dot"/>给专注一点生长的时间</span>
  </header>

  <main class="page-shell">
    <section class="hero" aria-labelledby="hero-title">
      <div class="hero-copy">
        <div class="eyebrow"><span class="eyebrow-line"/> A LITTLE PLAY, A LITTLE PEACE</div>
        <h1 id="hero-title">翻开一张，<br/>遇见<span class="heading-flower">好心情<svg viewBox="0 0 220 14" aria-hidden="true"><path d="M3 10Q106-3 215 7"/></svg></span>。</h1>
        <p>把忙碌放一边，让记忆散个步。<br class="mobile-br"/>找到相同的植物，收集属于你的片刻专注。</p>
        <button class="hero-link" @click="scrollToGame">来一场记忆漫游 <ArrowDown :size="15"/></button>
      </div>
      <div class="hero-art" aria-hidden="true">
        <div class="art-orbit orbit-one"/><div class="art-orbit orbit-two"/>
        <span class="art-spark spark-one">✦</span><span class="art-spark spark-two">✧</span>
        <div class="floating-card float-left"><PlantArt name="tulip"/><span>一点小幸运</span></div>
        <div class="floating-card float-right"><PlantArt name="sprout"/><span>一点新生长</span></div>
        <div class="floating-card float-center"><PlantArt name="daisy"/><span>记得开心</span></div>
        <span class="art-caption">good things grow here.</span>
        <div class="art-leaf leaf-one"><Leaf :size="28"/></div><div class="art-leaf leaf-two"><Sprout :size="30"/></div>
      </div>
    </section>

    <div class="workspace">
      <section id="game" ref="gameSection" class="game-panel" aria-labelledby="game-title">
        <div class="panel-topline">
          <div><span class="section-kicker">YOUR LITTLE GARDEN</span><h2 id="game-title">今天，也要好好玩。<Flower2 :size="20"/></h2></div>
          <button class="icon-button sound-button" :aria-pressed="sound" :aria-label="sound ? '关闭音效' : '开启音效'" :title="sound ? '关闭音效' : '开启音效'" @click="sound = !sound"><Volume2 v-if="sound" :size="19"/><VolumeX v-else :size="19"/></button>
        </div>

        <div class="game-toolbar">
          <div class="mode-tabs" role="group" aria-label="游戏难度">
            <button v-for="item in modes" :key="item.id" :class="{ selected: mode === item.id }" :aria-pressed="mode === item.id" :disabled="busy" @click="askRestart(item.id)">{{ item.label }}<span>{{ item.pairs }} 对</span></button>
          </div>
          <div class="game-actions">
            <button class="icon-button" :disabled="ready || completed || busy" :aria-label="paused ? '继续游戏' : '暂停游戏'" :title="paused ? '继续游戏' : '暂停游戏'" @click="togglePause"><Play v-if="paused" :size="18"/><Pause v-else :size="18"/></button>
            <button class="icon-button" :disabled="ready || busy" aria-label="重新开始" title="重新开始" @click="askRestart()"><RotateCcw :size="18"/></button>
          </div>
        </div>

        <div class="game-stats">
          <div class="stat"><span class="stat-label"><Clock3 :size="15"/>已用时间</span><strong>{{ formatTime(displayElapsed) }}</strong></div>
          <div class="stat"><span class="stat-label"><MousePointer2 :size="15"/>翻牌步数</span><strong>{{ String(game?.moves || 0).padStart(2, '0') }}<small>步</small></strong></div>
          <div class="stat"><span class="stat-label"><Sprout :size="16"/>已找到</span><strong>{{ matched }}<small>/ {{ totalPairs }} 对</small></strong></div>
          <div class="mini-progress" :style="{ '--progress': progress }" aria-hidden="true"><Leaf :size="19"/></div>
        </div>

        <div v-if="error" class="inline-error" role="alert"><span>{{ error }}</span><button v-if="game" class="text-button" :disabled="busy" @click="syncGame()">重新同步</button><button class="text-button" @click="error = ''">关闭</button></div>

        <div class="board-wrap" :class="{ 'is-ready': ready, 'is-paused': paused, 'is-completed': completed }">
          <div ref="boardElement" class="card-grid" :class="{ 'hard-grid': mode === 'hard' }" :aria-label="`${currentMode.label}难度，${totalPairs} 对卡牌`" :aria-busy="busy">
            <button v-for="card in cards" :key="`${game?.id || 'preview'}-${card.index}`" class="game-card" :class="{ revealed: !!card.symbol, matched: card.matched }" :disabled="ready || paused || completed || card.matched" :aria-label="card.symbol ? `第 ${card.index + 1} 张：${names[card.symbol]}${card.matched ? '，已配对' : ''}` : `翻开第 ${card.index + 1} 张卡牌`" :aria-pressed="!!card.symbol" @click="flip(card.index)">
              <span class="card-inner"><span class="card-back"><PlantArt name="mark"/><span>GROW A LITTLE</span></span><span class="card-front"><PlantArt :name="card.symbol || 'sprout'"/><span>{{ card.symbol ? names[card.symbol] : '' }}</span><span v-if="card.matched" class="match-check"><Check :size="12"/></span></span></span>
            </button>
          </div>
          <div v-if="ready || paused" class="board-overlay">
            <div class="start-note">
              <span class="start-note-icon"><Sprout :size="28"/></span>
              <span class="section-kicker">{{ paused ? 'TAKE YOUR TIME' : 'LET YOUR MIND BLOOM' }}</span>
              <h3>{{ paused ? '休息一下，也很好。' : '种下一点专注。' }}</h3>
              <p>{{ paused ? '计时已暂停，准备好了再继续。' : `${totalPairs} 对植物，等你发现彼此。` }}</p>
              <button class="primary-button" :disabled="busy" @click="paused ? togglePause() : startGame()"><LoaderCircle v-if="busy" class="spin" :size="17"/><Play v-else :size="16" fill="currentColor"/>{{ paused ? '继续漫游' : busy ? '花园准备中' : '开始翻牌' }}<ArrowRight :size="17"/></button>
              <small v-if="!paused">第一张卡牌翻开后开始计时</small>
            </div>
          </div>
        </div>

        <div class="board-footer"><span><span class="status-dot" :class="{ amber: paused }"/>{{ ready ? currentMode.description : completed ? '这片小花园，被你点亮了' : paused ? '花园正在休息' : `已收集 ${matched} / ${totalPairs} 对植物` }}</span><button v-if="completed" class="text-button" @click="winDialog.showModal()">{{ saved ? '查看本局成绩' : '保存本局成绩' }}<ChevronRight :size="15"/></button><span v-else class="board-hint">两张相同，即可配对</span></div>
        <p class="sr-only" role="status" aria-live="polite">{{ notice }}</p>
      </section>

      <aside class="sidebar">
        <section id="leaderboard" class="leaderboard panel" aria-labelledby="rank-title">
          <div class="sidebar-title"><span class="trophy-badge"><Trophy :size="20"/></span><div><span class="section-kicker">LITTLE ACHIEVEMENTS</span><h2 id="rank-title">花园榜单</h2></div><button class="icon-button" aria-label="刷新排行榜" :disabled="rankState === 'loading'" @click="fetchRanking()"><RefreshCw :size="15" :class="{ spin: rankState === 'loading' }"/></button></div>
          <p class="sidebar-intro">每一份专注，都值得被记住。</p>
          <div class="rank-tabs" role="group" aria-label="排行榜难度"><button v-for="item in modes" :key="item.id" :class="{ active: rankMode === item.id }" :aria-pressed="rankMode === item.id" @click="fetchRanking(item.id)">{{ item.label }}</button></div>
          <div class="ranking-head"><span>玩家</span><span>步数 / 用时</span></div>
          <div v-if="rankState === 'loading'" class="rank-empty" role="status"><LoaderCircle class="spin" :size="25"/><p>正在整理花园足迹…</p></div>
          <div v-else-if="rankState === 'error'" class="rank-empty rank-error" role="alert"><Leaf :size="29"/><p>{{ rankError }}</p><button class="text-button" @click="fetchRanking()">重新加载 <RefreshCw :size="13"/></button></div>
          <ol v-else-if="ranking.scores.length" class="ranking-list">
            <li v-for="(score, index) in ranking.scores" :key="score.id" :class="{ 'my-score': highlightScore === score.id }"><span class="rank-number" :class="{ 'top-rank': index < 3 }">{{ String(index + 1).padStart(2, '0') }}</span><span class="rank-player"><span class="player-avatar"><Leaf :size="16"/></span><span>{{ score.nickname }}</span></span><span class="rank-result"><strong>{{ score.moves }} 步</strong><small>{{ formatTime(score.durationMs, true) }}</small></span></li>
          </ol>
          <div v-else class="rank-empty"><span class="empty-plant"><PlantArt name="sprout"/></span><h3>第一片叶子，等你种下</h3><p>完成一局并保存成绩，<br/>让你的名字在这里发芽。</p></div>
          <div class="ranking-bottom"><Leaf :size="14"/><span>先比步数，再比用时 · 前 10 名</span></div>
        </section>

        <section class="gentle-note" aria-labelledby="note-title"><span class="note-kicker"><Sparkles :size="14"/>给你的小提示</span><h3 id="note-title">不用很快，<br/>记住一点就好。</h3><p>试着记住植物的位置，<br/>下一次相遇就会更容易。</p><PlantArt name="leaf"/><span class="note-number">01 / A MOMENT FOR YOU</span></section>
        <div class="tiny-facts"><span><CheckCheck :size="15"/>成绩自动持久保存<span class="fact-note">提交后</span></span><span><Leaf :size="15"/>没有倒计时，按你的节奏来</span></div>
      </aside>
    </div>

    <section class="how-to" aria-labelledby="how-title"><div class="how-intro"><span class="section-kicker">SIMPLE JOYS</span><h2 id="how-title">快乐，只需要三小步。</h2></div><div class="how-step"><span>01</span><div><h3>翻开卡牌</h3><p>点一下，认识一株小植物</p></div></div><div class="how-step"><span>02</span><div><h3>找到同伴</h3><p>记住位置，配对相同图案</p></div></div><div class="how-step"><span>03</span><div><h3>收集好心情</h3><p>完成花园，留下你的成绩</p></div></div></section>
    <footer class="site-footer"><span><Flower2 :size="15"/>记忆花园 <span class="footer-dot">·</span> 给日常一点小小的绿意</span><span>MADE FOR A LITTLE PEACE <span class="footer-dot">/</span> 6085</span></footer>
  </main>

  <dialog ref="rulesDialog" class="modal rules-modal" aria-labelledby="rules-title" @click="event => { if (event.target === rulesDialog) rulesDialog.close() }"><div class="modal-content"><button class="icon-button modal-close" aria-label="关闭玩法指南" @click="rulesDialog.close()"><X :size="20"/></button><span class="modal-symbol"><Sprout :size="30"/></span><span class="section-kicker">WELCOME TO YOUR GARDEN</span><h2 id="rules-title">一起来种点好心情。</h2><ol class="rules-list"><li><strong>选择一片花园</strong><p>轻松 6 对、标准 8 对、挑战 12 对。没有时间限制。</p></li><li><strong>翻开并记住位置</strong><p>每翻开两张计一步。图案相同则保留，不同则稍后翻回。</p></li><li><strong>保存你的专注时刻</strong><p>全部配对后填写昵称，将成绩保存到排行榜。步数越少排名越高，步数相同时比较用时。</p></li></ol><p class="rules-footnote">可以用 Tab 选择卡牌，按 Enter 或空格翻开。暂停不计时；页面刷新或服务重启后需重新开局，已提交的成绩会保留。</p><button class="primary-button full-width" @click="rulesDialog.close()">知道啦，去花园看看 <ArrowRight :size="17"/></button></div></dialog>

  <dialog ref="confirmDialog" class="modal confirm-modal" aria-labelledby="confirm-title"><div class="modal-content"><span class="modal-symbol"><RotateCcw :size="26"/></span><h2 id="confirm-title">要重新种一片花园吗？</h2><p>当前这局的进度将清空，已经保存的成绩会保留。</p><div class="modal-buttons"><button class="secondary-button" autofocus @click="confirmDialog.close()">再想想</button><button class="primary-button" @click="confirmRestart">开始新的一局</button></div></div></dialog>

  <dialog ref="winDialog" class="modal win-modal" aria-labelledby="win-title" @cancel="event => { if (saveBusy) event.preventDefault() }"><div class="modal-content"><button class="icon-button modal-close" aria-label="关闭成绩窗口" :disabled="saveBusy" @click="winDialog.close()"><X :size="20"/></button><div class="win-art"><PlantArt name="daisy"/></div><span class="section-kicker">A GARDEN WELL GROWN</span><h2 id="win-title">你的花园，开花了。</h2><p>又收集了一段小小的专注时光。</p><div class="win-stats"><span><small>完成用时</small><strong>{{ formatTime(game?.elapsedMs, true) }}</strong></span><span><small>翻牌步数</small><strong>{{ game?.moves }}<small>步</small></strong></span><span><small>配对成功率</small><strong>{{ accuracy }}</strong></span></div><form v-if="!saved" @submit.prevent="saveScore" novalidate><label for="nickname">给这份好心情留个名字<span>1–16 字</span></label><input id="nickname" ref="nicknameInput" v-model="nickname" type="text" maxlength="32" autocomplete="nickname" placeholder="你的花园昵称" :aria-invalid="!!saveError" :aria-describedby="saveError ? 'save-error' : undefined" :disabled="saveBusy"/><p v-if="saveError" id="save-error" class="form-error" role="alert">{{ saveError }}</p><button class="primary-button full-width" :disabled="saveBusy"><LoaderCircle v-if="saveBusy" class="spin" :size="17"/><Trophy v-else :size="17"/>{{ saveBusy ? '正在保存…' : '保存到花园榜单' }}</button></form><div v-else class="saved-message" role="status"><CheckCheck :size="20"/>成绩已保存，花园记住了你的名字。</div><button class="text-button again-button" :disabled="saveBusy" @click="playAgain">再漫游一次 <ArrowRight :size="16"/></button></div></dialog>
</template>
