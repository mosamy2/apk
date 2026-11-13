import sys
KEYS = """@keyframes bfly0{0%{transform:translate(0,0)}25%{transform:translate(10px,-165px)}50%{transform:translate(-8px,-330px)}75%{transform:translate(10px,-495px)}100%{transform:translate(0,-680px)}}
@keyframes bfly1{0%{transform:translate(0,0)}25%{transform:translate(-10px,-165px)}50%{transform:translate(8px,-330px)}75%{transform:translate(-10px,-495px)}100%{transform:translate(0,-680px)}}
@keyframes shrink0{0%{width:100%}100%{width:0%}}
@keyframes shrink1{0%{width:100%}100%{width:0%}}
@keyframes flashUp{0%{transform:scale(.4);opacity:0}30%{transform:scale(1.15);opacity:1}100%{transform:scale(1) translateY(-30px);opacity:0}}
"""
STAR = '<svg width="20" height="20" viewBox="0 0 24 24" fill="#FFC93C" stroke="#E39A00" stroke-width="1.5" aria-hidden="true"><path d="M12 2l3 7 7 .6-5.3 4.7 1.6 7.2L12 17.8 5.7 21.5l1.6-7.2L2 9.6 9 9z"/></svg>'
def win(p):
    return ('<sc-if value="{{' + p + 'Won}}" hint-placeholder-val="{{ false }}"><div style="position:absolute;left:0;right:0;top:0;bottom:0;z-index:3;background:linear-gradient(180deg,#FFF3C4,#FFD6E8 55%,#CFE9FF);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 24px;text-align:center;overflow:hidden">'
     '<div style="position:absolute;left:0;right:0;top:0;height:844px;pointer-events:none"><sc-for list="{{confetti}}" as="c" hint-placeholder-count="3"><i style="{{c.style}}"></i></sc-for></div>'
     '<div style="font-size:100px;line-height:1.1;animation:cheer .9s ease-in-out infinite">{{' + p + 'Emoji}}</div>'
     '<div style="font-size:26px;font-weight:700;margin-top:16px;animation:zoomIn .5s ease-out">{{' + p + 'WinTxt}}</div>'
     '<div style="font-size:15px;font-weight:600;margin-top:8px;color:#44507F">{{' + p + 'WinSub}}</div>'
     '<div style="margin-top:14px;height:44px;padding:0 18px;border-radius:22px;background:#fff;border:3px solid #FFC93C;display:flex;align-items:center;gap:6px;font-size:17px;font-weight:700;animation:zoomIn .6s .2s ease-out both">' + STAR + '{{' + p + 'GainTxt}}</div>'
     '<button onClick="{{' + p + 'Again}}" style="position:absolute;left:20px;right:20px;bottom:114px;height:56px;border-radius:28px;border:0;background:#FF8A3D;box-shadow:0 5px 0 #D86A1F;color:#1F2A5A;font-size:18px;font-weight:700;font-family:inherit">العب مرة أخرى</button>'
     '<button onClick="{{' + p + 'Back}}" style="position:absolute;left:20px;right:20px;bottom:44px;height:56px;border-radius:28px;border:0;background:#20B2A6;box-shadow:0 5px 0 #138A80;color:#1F2A5A;font-size:18px;font-weight:700;font-family:inherit">قائمة الألعاب</button>'
     '</div></sc-if>')
def head(p, title):
    return ('<div style="display:flex;align-items:center;gap:12px"><button onClick="{{' + p + 'Back}}" aria-label="رجوع" style="width:44px;height:44px;border-radius:22px;border:0;background:#fff;box-shadow:0 4px 0 #C9D3F0;font-size:24px;font-weight:700;color:#1F2A5A;font-family:inherit">›</button><div style="flex:1"><div style="font-size:22px;font-weight:700">' + title + '</div><div style="font-size:13px;font-weight:600;color:#44507F">{{' + p + 'Hint}}</div></div><div style="padding:0 14px;height:40px;border-radius:20px;background:#fff;border:3px solid #FFC93C;display:flex;align-items:center;gap:4px;font-size:14px;font-weight:700;white-space:nowrap">{{' + p + 'Prog}}</div></div>')
BALLOONS = ('<sc-if value="{{isBalloons}}" hint-placeholder-val="{{ false }}"><div style="position:absolute;left:0;right:0;top:0;bottom:0;z-index:8;background:linear-gradient(180deg,#8FD3FF 0%,#C6ECFF 50%,#FFF1C9 100%);display:flex;flex-direction:column;padding:56px 20px 0;box-sizing:border-box;overflow:hidden">'
 + head('bl', 'بالونات الذكر 🎈') +
 '<div style="display:flex;align-items:center;justify-content:space-between;margin-top:10px;font-size:20px;font-weight:700"><span aria-label="{{blLivesAria}}">{{blHearts}}</span><span style="{{blComboStyle}}">{{blCombo}}</span><span style="font-size:15px">{{blScore}}</span></div>'
 '<div style="{{blCard}}"><sc-for list="{{blWords}}" as="w" hint-placeholder-count="5"><span style="{{w.style}}">{{w.w}}</span></sc-for></div>'
 '<div style="position:relative;flex:1;margin:10px -20px 0;overflow:hidden">'
 '<sc-for list="{{blBalloons}}" as="b" hint-placeholder-count="4"><button onClick="{{b.go}}" aria-label="{{b.txt}}" style="{{b.style}}"><span style="{{b.txtStyle}}">{{b.txt}}</span></button></sc-for>'
 '<sc-if value="{{blHasFlash}}" hint-placeholder-val="{{ false }}"><div style="{{blFlashStyle}}">{{blFlash}}</div></sc-if>'
 '</div>' + win('bl') + '</div></sc-if>\n')
QUICK = ('<sc-if value="{{isQuick}}" hint-placeholder-val="{{ false }}"><div style="position:absolute;left:0;right:0;top:0;bottom:0;z-index:8;background:linear-gradient(180deg,#E3D9FF 0%,#DFF3FF 55%,#FFE8C2 100%);display:flex;flex-direction:column;padding:56px 20px 24px;box-sizing:border-box;overflow:hidden">'
 + head('qf', 'صح أم خطأ ⚡') +
 '<div style="margin-top:14px;height:18px;border-radius:9px;background:#fff;border:3px solid #C9D3F0;overflow:hidden;direction:ltr"><div style="{{qfBar}}"></div></div>'
 '<div style="height:34px;margin-top:8px;text-align:center;font-size:20px;font-weight:700"><span style="{{qfComboStyle}}">{{qfCombo}}</span></div>'
 '<div style="{{qfCard}}"><div style="font-size:14px;font-weight:700;color:#596392">{{qfAsk}}</div><div style="font-size:30px;font-weight:700;line-height:1.8;margin-top:8px">{{qfLead}} …</div><div style="display:inline-block;margin-top:8px;padding:4px 22px;border-radius:18px;background:#FFE08A;border:3px dashed #FF8A3D;font-size:32px;font-weight:700;line-height:1.7">{{qfCand}}</div></div>'
 '<div style="display:flex;gap:12px;margin-top:22px"><button onClick="{{qfYes}}" style="flex:1;height:96px;border-radius:28px;border:0;font-family:inherit;font-size:26px;font-weight:700;color:#0B4F49;background:radial-gradient(circle at 30% 20%,rgba(255,255,255,.6) 0,rgba(255,255,255,0) 45%),#3FD1A4;box-shadow:0 8px 0 #1E9C77,0 14px 16px rgba(31,42,90,.2)">✓ صح</button><button onClick="{{qfNo}}" style="flex:1;height:96px;border-radius:28px;border:0;font-family:inherit;font-size:26px;font-weight:700;color:#6B1220;background:radial-gradient(circle at 30% 20%,rgba(255,255,255,.6) 0,rgba(255,255,255,0) 45%),#FF8FA3;box-shadow:0 8px 0 #D85C74,0 14px 16px rgba(31,42,90,.2)">✗ خطأ</button></div>'
 + win('qf') + '</div></sc-if>\n')
METHODS = r"""applause(len) { if (this.state.muted) return; const a = this.ctx(); if (!a) return; try { const n = Math.floor(a.sampleRate * 0.05), buf = a.createBuffer(1, n, a.sampleRate), d = buf.getChannelData(0); for (let i = 0; i < n; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / n, 2.2); const dur = len || 3.2, t0 = a.currentTime + 0.05; for (let c = 0; c < dur * 26; c++) { const t = t0 + Math.random() * dur, src = a.createBufferSource(), f = a.createBiquadFilter(), g = a.createGain(), env = Math.sin(Math.PI * Math.min(1, (t - t0) / dur + 0.12)); src.buffer = buf; src.playbackRate.value = 0.8 + Math.random() * 0.6; f.type = 'bandpass'; f.frequency.value = 1100 + Math.random() * 1500; f.Q.value = 0.9; g.gain.value = (0.1 + Math.random() * 0.14) * (0.35 + env); src.connect(f); f.connect(g); g.connect(a.destination); src.start(t); } } catch (e) {} }
gWords(k) { return this.PT[k].t.split(/\s+/).filter(Boolean).map((w) => w.replace(/[،,.؛:]+$/, '')).filter((w) => !/^[ۖ-ۭ]+$/.test(w)); }
gBase(w) { return w.replace(/[ً-ٰٟۖ-ۭ]/g, ''); }
gShuf(a) { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); const x = a[i]; a[i] = a[j]; a[j] = x; } return a; }
gPool() { const pool = [], skip = (w) => /صلى|عليه|وسلم/.test(this.gBase(w)) || this.gBase(w).length < 3; Object.keys(this.PT).forEach((k) => this.gWords(k).forEach((w) => { if (!skip(w) && !pool.some((p) => this.gBase(p) === this.gBase(w))) pool.push(w); })); return pool; }
startBalloons() {
this.clearAll();
const pool = this.gPool(), skip = (w) => /صلى|عليه|وسلم/.test(this.gBase(w)) || this.gBase(w).length < 3;
let keys = this.gShuf(this.seenKeys().slice()); while (keys.length < 8) keys = keys.concat(this.gShuf(this.seenKeys().slice())); keys = keys.slice(0, 8);
const qs = keys.map((k) => { let words = this.gWords(k), off = 0; if (words.length > 9) { off = Math.floor(Math.random() * (words.length - 8)); words = words.slice(off, off + 8); }
const cand = words.map((w, i) => i).filter((i) => !skip(words[i])); const idx = cand.length ? cand[Math.floor(Math.random() * cand.length)] : 0; const ans = words[idx];
const opts = this.gShuf([ans].concat(this.gShuf(pool.filter((p) => this.gBase(p) !== this.gBase(ans))).slice(0, 3)));
return { k, ans, opts, before: words.slice(0, idx), after: words.slice(idx + 1), pre: off > 0, post: off + 8 < this.gWords(k).length && off + words.length < this.gWords(k).length }; });
this.setState({ view: 'balloons', bl: { qs, i: 0, lives: 3, score: 0, combo: 0, best: 0, right: 0, phase: 'fly', bad: [], flash: '', done: false, gain: 0 } });
this.blArm();
}
blDur(i) { return Math.max(4.4, 7.6 - i * 0.4); }
blArm() { clearTimeout(this.blT); const c = this.state.bl; if (!c || c.done) return; this.blT = this.later(() => this.blMiss(), (this.blDur(c.i) + 0.7) * 1000); }
blNext(c) { clearTimeout(this.blT); this.blT = this.later(() => { const c2 = this.state.bl; if (!c2 || this.state.view !== 'balloons') return; if (c2.lives <= 0 || c2.i + 1 >= c2.qs.length) { const gain = this.awardGame(Math.min(8, 1 + Math.floor(c2.score / 3))); this.arp([523, 659, 784, 1047, 1319], 0.1, 'triangle', 0.15); if (c2.lives > 0) this.applause(2); this.setState({ bl: Object.assign({}, c2, { done: true, gain, phase: 'end' }) }); } else { this.setState({ bl: Object.assign({}, c2, { i: c2.i + 1, bad: [], phase: 'fly', flash: '' }) }); this.blArm(); } }, 950); }
blMiss() { const c = this.state.bl; if (!c || c.done || c.phase !== 'fly' || this.state.view !== 'balloons') return; this.tone(196, 0, 0.3, 'sawtooth', 0.06); const n = Object.assign({}, c, { lives: c.lives - 1, combo: 0, phase: 'miss', flash: '💨 ' + c.qs[c.i].ans }); this.setState({ bl: n }); this.blNext(n); }
pickBalloon(oi) { const c = this.state.bl; if (!c || c.done || c.phase !== 'fly' || c.bad.includes(oi)) return; const q = c.qs[c.i];
if (q.opts[oi] === q.ans) { const combo = c.combo + 1, pts = 1 + Math.min(4, combo - 1); this.arp(combo >= 3 ? [784, 988, 1175, 1568] : [784, 1175], 0.07, 'triangle', 0.15); const n = Object.assign({}, c, { combo, best: Math.max(c.best, combo), right: c.right + 1, score: c.score + pts, phase: 'hit', flash: '🎉 +' + this.ar(pts) }); this.setState({ bl: n }); this.blNext(n); }
else { this.tone(220, 0, 0.25, 'sawtooth', 0.06); const lives = c.lives - 1; const n = Object.assign({}, c, { lives, combo: 0, bad: c.bad.concat(oi) }, lives <= 0 ? { phase: 'miss', flash: '💨 ' + q.ans } : {}); this.setState({ bl: n }); if (lives <= 0) this.blNext(n); } }
qfMake() { const keys = this.seenKeys().filter((k) => this.gWords(k).length >= 3), k = keys[Math.floor(Math.random() * keys.length)], w = this.gWords(k), j = Math.floor(Math.random() * (w.length - 2)), yes = Math.random() < 0.5; let cand = w[j + 2];
if (!yes) { const pool = this.gPool().filter((p) => this.gBase(p) !== this.gBase(w[j + 2]) && this.gBase(p) !== this.gBase(w[j + 1])); cand = pool[Math.floor(Math.random() * pool.length)]; }
return { k, lead: w[j] + ' ' + w[j + 1], cand, yes }; }
startQuick() { this.clearAll(); this.qfRun = (this.qfRun || 0) + 1; this.setState({ view: 'quick', qf: { q: this.qfMake(), score: 0, combo: 0, best: 0, n: 0, right: 0, fb: '', done: false, gain: 0, run: this.qfRun } }); clearTimeout(this.qfT); this.qfT = this.later(() => { const c = this.state.qf; if (!c || this.state.view !== 'quick' || c.done) return; const gain = this.awardGame(Math.min(8, 1 + Math.floor(c.score / 4))); this.arp([523, 659, 784, 1047, 1319], 0.1, 'triangle', 0.15); if (c.right >= 8) this.applause(2); this.setState({ qf: Object.assign({}, c, { done: true, gain }) }); }, 40000); }
pickQuick(v) { const c = this.state.qf; if (!c || c.done) return; const ok = v === c.q.yes; if (ok) { const combo = c.combo + 1; this.arp(combo % 3 === 0 ? [784, 988, 1175, 1568] : [880, 1175], 0.06, 'triangle', 0.14); this.setState({ qf: Object.assign({}, c, { q: this.qfMake(), n: c.n + 1, right: c.right + 1, combo, best: Math.max(c.best, combo), score: c.score + 1 + (combo % 3 === 0 ? 2 : 0), fb: 'ok' + c.n }) }); } else { this.tone(200, 0, 0.22, 'sawtooth', 0.06); this.setState({ qf: Object.assign({}, c, { q: this.qfMake(), n: c.n + 1, combo: 0, fb: 'no' + c.n }) }); } }
"""
BPAL = "['#FF6FA5','#FFC93C','#5BC8F5','#8EDB7C']"
VALS = ("isBalloons: s.view === 'balloons', blWon: !!(s.bl && s.bl.done), "
 "blHint: t('فرقع بالونة الكلمة الناقصة قبل أن تطير', 'فرقعي بالونة الكلمة الناقصة قبل أن تطير'), "
 "blProg: s.bl ? 'جولة ' + ar(Math.min(s.bl.i + 1, s.bl.qs.length)) + ' من ' + ar(s.bl.qs.length) : '', "
 "blHearts: s.bl ? '❤️'.repeat(Math.max(0, s.bl.lives)) + '🤍'.repeat(3 - Math.max(0, s.bl.lives)) : '', blLivesAria: s.bl ? 'المحاولات الباقية ' + ar(Math.max(0, s.bl.lives)) : '', "
 "blCombo: s.bl && s.bl.combo >= 2 ? '🔥 ×' + ar(s.bl.combo) : '', blComboStyle: 'display:inline-block;color:#D8480B;animation:' + (s.bl && s.bl.combo >= 2 ? 'pulse .5s ease-in-out infinite' : 'none'), "
 "blScore: s.bl ? ar(s.bl.score) + ' نقطة' : '', "
 "blCard: 'margin-top:10px;background:#fff;border:3px solid #C9D3F0;border-radius:24px;box-shadow:0 5px 0 #C9D3F0;padding:10px 12px;text-align:center;line-height:1.8;font-weight:700;box-sizing:border-box;font-size:' + (s.bl ? (() => { const q = s.bl.qs[Math.min(s.bl.i, s.bl.qs.length - 1)]; return q.before.length + q.after.length > 5 ? 20 : 24; })() : 24) + 'px', "
 "blWords: s.bl ? (() => { const c = s.bl, q = c.qs[Math.min(c.i, c.qs.length - 1)], base = 'display:inline-block;margin:0 4px', shown = c.phase !== 'fly'; return [].concat(q.pre ? [{ w: '…', style: base }] : [], q.before.map((w) => ({ w, style: base })), [{ w: shown ? q.ans : '؟؟؟', style: base + ';padding:0 12px;border-radius:12px;' + (shown ? 'background:#C9F2EC;border:2px solid #20B2A6' : 'background:#FFE08A;border:2px dashed #FF8A3D') }], q.after.map((w) => ({ w, style: base })), q.post ? [{ w: '…', style: base }] : []); })() : [], "
 "blBalloons: s.bl && s.bl.phase === 'fly' && !s.bl.done ? s.bl.qs[s.bl.i].opts.map((o, oi) => { const c = s.bl, bad = c.bad.includes(oi), L = o.replace(/[\\u064B-\\u065F\\u0670]/g, '').length; return { txt: o, go: () => this.pickBalloon(oi), txtStyle: 'display:block;font-size:' + (L > 8 ? 14 : (L > 5 ? 17 : 21)) + 'px;font-weight:700;color:#1F2A5A;line-height:1.5;padding:0 4px', style: 'position:absolute;left:' + (10 + oi * 94) + 'px;bottom:-130px;width:88px;height:108px;border:0;padding:0;font-family:inherit;border-radius:50% 50% 50% 50% / 44% 44% 56% 56%;background:radial-gradient(circle at 30% 26%,rgba(255,255,255,.9) 0,rgba(255,255,255,0) 40%),' + " + BPAL + "[oi % 4] + ';box-shadow:inset -8px -12px 14px rgba(0,0,0,.18),0 10px 12px rgba(31,42,90,.22);animation:bfly' + ((c.i + oi) % 2) + ' ' + (this.blDur(c.i) * [1, 0.9, 0.96, 0.86][oi]).toFixed(2) + 's linear ' + [0, 0.5, 0.25, 0.7][oi] + 's forwards' + (bad ? ';opacity:.25;pointer-events:none' : '') }; }) : [], "
 "blHasFlash: !!(s.bl && s.bl.flash && !s.bl.done), blFlash: s.bl ? s.bl.flash : '', blFlashStyle: 'position:absolute;left:0;right:0;top:120px;text-align:center;font-size:40px;font-weight:700;color:' + (s.bl && s.bl.phase === 'hit' ? '#0B7A6E' : '#B4233A') + ';animation:flashUp .9s ease-out forwards', "
 "blBack: () => { this.clearAll(); this.setState({ view: 'games' }); }, blAgain: () => this.startBalloons(), "
 "blEmoji: s.bl && s.bl.lives > 0 ? '🎈' : '💪', blWinTxt: s.bl && s.bl.lives > 0 ? t('رائع يا بطل!', 'رائعة يا بطلة!') : t('حاول مرة أخرى يا بطل!', 'حاولي مرة أخرى يا بطلة!'), "
 "blWinSub: s.bl ? ar(s.bl.right) + ' بالونات صحيحة · أطول سلسلة ' + ar(s.bl.best) + ' 🔥 · ' + ar(s.bl.score) + ' نقطة' : '', blGainTxt: '+' + ar(s.bl ? s.bl.gain : 0) + ' نجوم', "
 "isQuick: s.view === 'quick', qfWon: !!(s.qf && s.qf.done), "
 "qfHint: t('هل الكلمة التالية صحيحة؟ أجب بسرعة!', 'هل الكلمة التالية صحيحة؟ أجيبي بسرعة!'), qfProg: s.qf ? '⭐ ' + ar(s.qf.score) : '', "
 "qfBar: 'height:100%;border-radius:6px;background:linear-gradient(90deg,#FF6FA5,#FFC93C,#3FD1A4);animation:shrink' + ((s.qf ? s.qf.run : 0) % 2) + ' 40s linear forwards', "
 "qfCombo: s.qf && s.qf.combo >= 2 ? '🔥 سلسلة ' + ar(s.qf.combo) : '', qfComboStyle: 'display:inline-block;color:#D8480B;animation:' + (s.qf && s.qf.combo >= 2 ? 'pulse .5s ease-in-out infinite' : 'none'), "
 "qfCard: 'margin-top:6px;border-radius:28px;padding:22px 14px;text-align:center;box-sizing:border-box;border:4px solid ' + (s.qf && /^ok/.test(s.qf.fb) ? '#20B2A6' : (s.qf && /^no/.test(s.qf.fb) ? '#FF6B6B' : '#C9D3F0')) + ';background:' + (s.qf && /^ok/.test(s.qf.fb) ? '#E4FAF5' : (s.qf && /^no/.test(s.qf.fb) ? '#FFECEC' : '#fff')) + ';box-shadow:0 8px 0 #C9D3F0,0 14px 18px rgba(31,42,90,.15);transition:background .2s,border-color .2s', "
 "qfAsk: s.qf ? 'من ذكر «' + P[s.qf.q.k].s + '» · هل تأتي هذه الكلمة بعدها؟' : '', qfLead: s.qf ? s.qf.q.lead : '', qfCand: s.qf ? s.qf.q.cand : '', "
 "qfYes: () => this.pickQuick(true), qfNo: () => this.pickQuick(false), qfBack: () => { this.clearAll(); this.setState({ view: 'games' }); }, qfAgain: () => this.startQuick(), "
 "qfEmoji: '⚡', qfWinTxt: t('انتهى الوقت يا بطل!', 'انتهى الوقت يا بطلة!'), qfWinSub: s.qf ? ar(s.qf.right) + ' إجابات صحيحة من ' + ar(s.qf.n) + ' · أطول سلسلة ' + ar(s.qf.best) + ' 🔥' : '', qfGainTxt: '+' + ar(s.qf ? s.qf.gain : 0) + ' نجوم', ")
GLOSS = "radial-gradient(circle at 32% 24%,rgba(255,255,255,.8) 0,rgba(255,255,255,0) 46%),"
DARK = "['#D95C86','#D99A00','#3FA57C','#4A86D1','#D0641C','#7F5AD1','#D14545']"
def rep(s, a, b, n=1):
    assert s.count(a) >= 1, a[:70]
    return s.replace(a, b, n)
for f in sys.argv[1:]:
    s = open(f, encoding='utf8').read()
    s = rep(s, "@keyframes glow{", KEYS + "@keyframes glow{")
    s = rep(s, '<sc-if value="{{isCloze}}"', BALLOONS + QUICK + '<sc-if value="{{isCloze}}"')
    s = rep(s, "arp(list, gap, type, vol) {", METHODS + "arp(list, gap, type, vol) {")
    s = rep(s, "isWird: s.view === 'wird',", VALS + "isWird: s.view === 'wird',")
    # games list
    s = rep(s, "['🚂', 'سباق القطار', 'أجب عن الأسئلة ليسبق قطارك', 4]]", "['🚂', 'سباق القطار', 'أجب عن الأسئلة ليسبق قطارك', 4], ['🎈', 'بالونات الذكر', 'فرقع بالونة الكلمة الصحيحة قبل أن تطير', 1], ['⚡', 'صح أم خطأ', 'أجب بسرعة قبل انتهاء الوقت', 2]]")
    s = rep(s, "go: () => ok && gi === 0 ? this.startCloze()", "go: () => ok && gi === 5 ? this.startBalloons() : ok && gi === 6 ? this.startQuick() : ok && gi === 0 ? this.startCloze()")
    s = rep(s, "border:3px solid ' + (ok ? '#20B2A6' : '#C9D3F0'),", "border:3px solid ' + (ok ? '#20B2A6' : '#C9D3F0') + ';box-shadow:0 5px 0 ' + (ok ? '#138A80' : '#C9D3F0'),")
    # applause on celebration
    s = rep(s, "this.setState({ view: 'wird' }); } }, 3200);", "this.applause(3.6); this.setState({ view: 'wird' }); } }, 3200);")
    s = rep(s, "tC: () => open ? this.setState({ view: 'wird' })", "tC: () => open ? (this.applause(3), this.setState({ view: 'wird' }))")
    # 3D stations
    old = "';border:4px solid #fff;box-shadow:0 3px 0 rgba(31,42,90,.25);color:#1F2A5A' : (st === 'cur' ? 'background:#7B5CFF;border:6px solid #FFC93C;color:#fff' : 'background:#fff;border:4px solid #C9D3F0;color:#596392');"
    new = ("';border:3px solid #fff;box-shadow:0 6px 0 ' + " + DARK + "[(k - 1) % 7] + ',0 12px 12px rgba(31,42,90,.28),inset 0 -6px 8px rgba(0,0,0,.12);color:#1F2A5A' : (st === 'cur' ? 'background:" + GLOSS + "#7B5CFF;border:5px solid #FFC93C;box-shadow:0 7px 0 #4A34B8,0 14px 16px rgba(31,42,90,.32),inset 0 -6px 10px rgba(0,0,0,.18);color:#fff' : 'background:radial-gradient(circle at 32% 24%,#fff 0,#E3EAF9 75%);border:4px solid #C9D3F0;box-shadow:0 5px 0 #AEB9DA,0 10px 10px rgba(31,42,90,.18);color:#596392');")
    s = rep(s, old, new)
    s = rep(s, "const col = st === 'done' ? 'background:' + ['#FF8FB1'", "const col = st === 'done' ? 'background:" + GLOSS + "' + ['#FF8FB1'")
    # 3D scenery
    s = s.replace(';animation:drift ', ';filter:drop-shadow(0 7px 5px rgba(70,100,160,.25));animation:drift ')
    s = s.replace('<ellipse cx="60" cy="34" rx="52" ry="14" fill="#fff"/>', '<ellipse cx="60" cy="38" rx="50" ry="11" fill="#D5E3F6"/><ellipse cx="60" cy="34" rx="52" ry="14" fill="#fff"/>')
    s = rep(s, 'style="position:absolute;left:0;top:544px" aria-hidden="true">', 'style="position:absolute;left:0;top:544px" aria-hidden="true"><defs><linearGradient id="hg1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#CDF5C0"/><stop offset="1" stop-color="#8AD38F"/></linearGradient><linearGradient id="hg2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A6E6A8"/><stop offset="1" stop-color="#5DB877"/></linearGradient><linearGradient id="hg3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#83DB93"/><stop offset="1" stop-color="#3FA865"/></linearGradient><radialGradient id="tg" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#9BEBA6"/><stop offset="1" stop-color="#379A5C"/></radialGradient><linearGradient id="mg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#D9CFFF"/><stop offset="1" stop-color="#9483E0"/></linearGradient><radialGradient id="dg" cx=".35" cy=".3" r=".9"><stop offset="0" stop-color="#C9BCFF"/><stop offset="1" stop-color="#7D6AD6"/></radialGradient></defs>')
    for a, b in (('fill="#A8E6A1"', 'fill="url(#hg1)"'), ('fill="#7DD08B"', 'fill="url(#hg2)"'), ('fill="#5FC27A"', 'fill="url(#hg3)"'), ('fill="#4FB872"', 'fill="url(#tg)"'), ('fill="#5CC67E"', 'fill="url(#tg)"'), ('fill="#B7A8F0"', 'fill="url(#mg)"'), ('fill="#9A89E6"', 'fill="url(#dg)"')):
        assert a in s, a; s = s.replace(a, b)
    s = rep(s, '<svg width="350" height="560" viewBox="0 0 350 560" style="position:absolute;left:0;top:0"', '<svg width="350" height="560" viewBox="0 0 350 560" style="position:absolute;left:0;top:0;filter:drop-shadow(0 3px 0 rgba(31,42,90,.22))"')
    s = rep(s, "transition:left .06s linear, top .06s linear;animation:trainIn .5s ease-out'", "transition:left .06s linear, top .06s linear;animation:trainIn .5s ease-out;filter:drop-shadow(0 8px 5px rgba(31,42,90,.35))'")
    # 3D medal
    s = rep(s, 'role="img" aria-label="ميدالية الورد" style="animation:zoomIn .7s ease-out">', 'role="img" aria-label="ميدالية الورد" style="animation:zoomIn .7s ease-out;filter:drop-shadow(0 10px 8px rgba(120,70,0,.35))"><defs><radialGradient id="md1" cx=".35" cy=".28" r=".9"><stop offset="0" stop-color="#FFF6C2"/><stop offset=".55" stop-color="#FFC93C"/><stop offset="1" stop-color="#D98A00"/></radialGradient><radialGradient id="md2" cx=".35" cy=".28" r=".9"><stop offset="0" stop-color="#FFFBE0"/><stop offset="1" stop-color="#FFD45A"/></radialGradient><linearGradient id="md3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFB25E"/><stop offset="1" stop-color="#E8641A"/></linearGradient></defs>')
    s = rep(s, '<circle cx="95" cy="82" r="60" fill="#FFC93C"/><circle cx="95" cy="82" r="48" fill="#FFE08A" stroke="#E39A00" stroke-width="3"/>', '<circle cx="95" cy="82" r="60" fill="url(#md1)"/><circle cx="95" cy="82" r="48" fill="url(#md2)" stroke="#E39A00" stroke-width="3"/>')
    s = rep(s, 'fill="#FF8A3D" stroke="#E39A00" stroke-width="3" stroke-linejoin="round"/>', 'fill="url(#md3)" stroke="#C25A10" stroke-width="3" stroke-linejoin="round"/>')
    s = rep(s, "border:2px solid #fff;background:' + ['#FF8FB1'", "border:2px solid #fff;box-shadow:0 4px 0 rgba(31,42,90,.2);background:" + GLOSS + "' + ['#FF8FB1'")
    open(f, 'w', encoding='utf8').write(s); print('patched', f)
