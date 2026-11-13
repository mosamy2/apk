import sys, re, json
CT = json.dumps(json.load(open('tools/counts.json')))
def rep(s, a, b, n=1):
    assert a in s, a[:90]
    return s.replace(a, b, n)
def rx(s, pat, b, flags=re.S):
    r, n = re.subn(pat, lambda m: b, s, count=1, flags=flags); assert n == 1, pat[:80]; return r
KEYS = "@keyframes flipA{0%{transform:rotateY(90deg) scale(.9)}100%{transform:rotateY(0) scale(1)}}\n@keyframes flipB{0%{transform:rotateY(-90deg) scale(.9)}100%{transform:rotateY(0) scale(1)}}\n"
MEM = r"""startMemory() {
this.clearAll();
const P = this.PT;
const qs = this.gShuf(this.seenKeys().slice()).slice(0, 6).map((k) => {
const words = this.gWords(k), n = words.length, tl = Math.min(8, Math.max(1, Math.ceil(n / 2)));
const head = words.slice(0, n - tl), tail = words.slice(n - tl).join(' ');
const others = this.gShuf(Object.keys(P).filter((x) => x !== k)).map((x) => { const w = this.gWords(x); return w.slice(Math.max(0, w.length - tl)).join(' '); }).filter((x, i, a) => x !== tail && a.indexOf(x) === i).slice(0, 3);
const cards = this.gShuf([tail].concat(others));
return { k, head, tail, cards, ai: cards.indexOf(tail) };
});
this.setState({ view: 'memory', mg: { qs, i: 0, phase: 'show', cd: 5, open: -1, wrong: -1, lock: false, solved: false, score: 0, done: false, gain: 0 } });
this.mgShow();
}
mgShow() { clearTimeout(this.mgT); const tick = () => { const m = this.state.mg; if (!m || m.done || this.state.view !== 'memory') return; if (m.cd <= 1) { this.setState({ mg: Object.assign({}, m, { phase: 'pick', cd: 0 }) }); return; } this.setState({ mg: Object.assign({}, m, { cd: m.cd - 1 }) }); this.mgT = this.later(tick, 1000); }; this.mgT = this.later(tick, 1000); }
mgNext(ms) { this.later(() => { const m2 = this.state.mg; if (!m2 || this.state.view !== 'memory') return; if (m2.i + 1 >= m2.qs.length) { const gain = this.awardGame(Math.min(8, m2.score)); this.arp([523, 659, 784, 1047, 1319], 0.1, 'triangle', 0.15); this.setState({ mg: Object.assign({}, m2, { done: true, gain }) }); } else { this.setState({ mg: Object.assign({}, m2, { i: m2.i + 1, phase: 'show', cd: 5, open: -1, wrong: -1, solved: false, lock: false }) }); this.mgShow(); } }, ms); }
flip(ci) {
const m = this.state.mg; if (!m || m.done || m.phase !== 'pick' || m.solved || m.lock) return;
const q = m.qs[m.i];
if (ci === q.ai) {
this.arp([784, 988, 1175], 0.1, 'triangle', 0.14);
this.setState({ mg: Object.assign({}, m, { open: ci, solved: true, lock: true, score: m.score + 1 }) });
this.mgNext(1500);
} else {
this.tone(220, 0, 0.25, 'sawtooth', 0.06);
this.setState({ mg: Object.assign({}, m, { open: ci, wrong: ci, lock: true }) });
this.later(() => { const m2 = this.state.mg; if (!m2 || this.state.view !== 'memory') return; this.setState({ mg: Object.assign({}, m2, { open: q.ai, solved: true }) }); this.arp([523, 659], 0.12, 'triangle', 0.08); }, 900);
this.mgNext(2900);
}
}
"""
QF_MAKE = r"""qfMake() { const keys = this.seenKeys(), k = keys[Math.floor(Math.random() * keys.length)], w = this.gWords(k).slice(), yes = Math.random() < 0.5;
if (!yes) { const skip = (x) => /صلى|عليه|وسلم/.test(this.gBase(x)) || this.gBase(x).length < 3; const cand = w.map((x, i) => i).filter((i) => !skip(w[i])); const bad = cand[Math.floor(Math.random() * cand.length)]; const orig = this.gBase(w[bad]); const pool = this.gPool().filter((p) => this.gBase(p) !== orig && !w.some((x) => this.gBase(x) === this.gBase(p))); w[bad] = pool[Math.floor(Math.random() * pool.length)]; }
return { k, text: w.join(' '), n: w.length, yes }; }
"""
GL = "const GL = { 1: ['أكمل الكلمة', 'رتّب الذكر'], 2: ['ذاكرة الأذكار', 'بالونات الذكر'], 3: ['صيد النجوم'], 4: ['صح أم خطأ'], 5: ['سباق القطار'] };"
for f in sys.argv[1:]:
    s = open(f, encoding='utf8').read()
    # 1 repetition counts
    s = rx(s, r"this\.CT = \{.*?\};", "this.CT = " + CT + ";")
    # 2 kid id
    g = "boy" if f.endswith('Main.dc.html') else "girl"
    a = "this.g = '%s'; try { this.nm = window.localStorage.getItem('tk_name_%s'); } catch (e) { this.nm = null; }\nthis.dbKey = 'tk_db_' + this.g;" % (g, g)
    b = ("this.g = '%s'; this.kid = '%s'; this.nm = null; try { const T = window.TK, q = new URLSearchParams(window.location.search).get('k'); if (T && q) { const kd = T.kid(q); if (kd) { this.kid = kd.id; this.nm = kd.name; } } } catch (e) {} if (!this.nm) { try { this.nm = window.localStorage.getItem('tk_name_' + this.kid); } catch (e) {} }\nthis.dbKey = 'tk_db_' + this.kid;" % (g, g))
    s = rep(s, a, b)
    s = rep(s, "getItem('tk_times_' + this.g)", "getItem('tk_times_' + this.kid)")
    s = rep(s, "setItem('tk_live_' + this.g, lv)", "setItem('tk_live_' + this.kid, lv)")
    # 3 applause: real-ish recording rendered offline, falls back to synthesis
    s = rep(s, "applause(len) { if (this.state.muted) return;", "applause(len) { if (this.state.muted) return; try { const u = ((window.TK_AUDIO || {}).fx || {}).applause; if (u) { if (this.fxA) { try { this.fxA.pause(); } catch (e) {} } const a = new Audio(u); this.fxA = a; a.volume = 0.95; const p = a.play(); if (p && p.catch) p.catch(() => {}); return; } } catch (e) {}")
    s = rep(s, "clearAll() { try { if (this.curAudio) this.curAudio.pause(); } catch (e) {}", "clearAll() { try { if (this.curAudio) this.curAudio.pause(); } catch (e) {} try { if (this.fxA) this.fxA.pause(); } catch (e) {}")
    # 4 quick: whole dhikr
    s = rx(s, r"qfMake\(\) \{.*?\n return \{ k, lead.*?\}; \}\n" if False else r"qfMake\(\) \{.*?return \{ k, lead: w\[j\] \+ ' ' \+ w\[j \+ 1\], cand, yes \}; \}\n", QF_MAKE)
    s = rep(s, '<div style="font-size:30px;font-weight:700;line-height:1.8;margin-top:8px">{{qfLead}} …</div><div style="display:inline-block;margin-top:8px;padding:4px 22px;border-radius:18px;background:#FFE08A;border:3px dashed #FF8A3D;font-size:32px;font-weight:700;line-height:1.7">{{qfCand}}</div>', '<div style="{{qfTextStyle}}">{{qfText}}</div>')
    s = rep(s, "qfAsk: s.qf ? 'من ذكر «' + P[s.qf.q.k].s + '» · هل تأتي هذه الكلمة بعدها؟' : '', qfLead: s.qf ? s.qf.q.lead : '', qfCand: s.qf ? s.qf.q.cand : '',",
        "qfAsk: s.qf ? 'هل هذا الذكر مكتوب صحيحًا؟ (' + P[s.qf.q.k].s + ')' : '', qfText: s.qf ? s.qf.q.text : '', qfTextStyle: 'margin-top:8px;font-weight:700;line-height:1.9;max-height:300px;overflow:auto;font-size:' + (s.qf ? (s.qf.q.n <= 6 ? 34 : (s.qf.q.n <= 12 ? 28 : (s.qf.q.n <= 25 ? 22 : 18))) : 28) + 'px',")
    s = rep(s, "s linear forwards' + (bad", "s linear forwards' + (bad") if False else s
    s = rep(s, "animation:shrink' + ((s.qf ? s.qf.run : 0) % 2) + ' 40s linear forwards", "animation:shrink' + ((s.qf ? s.qf.run : 0) % 2) + ' 60s linear forwards")
    s = rep(s, "}, 40000); }", "}, 60000); }")
    # 5 memory game
    s = rep(s, "@keyframes glow{", KEYS + "@keyframes glow{")
    s = rx(s, r"startMemory\(\) \{.*?\nflip\(ci\) \{.*?\n\}\n\}\n", MEM)
    s = rx(s, r"memHint: t\([^\n]*?\),\n", "memHint: mg ? (mg.phase === 'show' ? t('احفظ أماكن البطاقات! ', 'احفظي أماكن البطاقات! ') + '⏳ ' + ar(mg.cd) : (mg.wrong >= 0 ? 'ليست هذه، انظر البطاقة الصحيحة' : t('أين باقي الذكر؟ اختر البطاقة', 'أين باقي الذكر؟ اختاري البطاقة'))) : '',\n")
    s = rx(s, r"memCards: mg \?.*?: \[\],\n", r"""memCards: mg ? mg.qs[Math.min(mg.i, mg.qs.length - 1)].cards.map((txt, ci) => { const q = mg.qs[Math.min(mg.i, mg.qs.length - 1)], face = mg.phase === 'show' || mg.open === ci, good = mg.solved && ci === q.ai, bad = mg.wrong === ci; return { txt: face ? txt : '❓', go: () => this.flip(ci), style: 'min-height:120px;border-radius:20px;box-sizing:border-box;padding:10px;font-family:inherit;font-weight:700;display:flex;align-items:center;justify-content:center;text-align:center;line-height:1.7;font-size:' + (face ? 17 : 38) + 'px;animation:flip' + (face ? 'A' : 'B') + ' .4s ease-out;' + (face ? (good ? 'color:#1F2A5A;background:#C9F2EC;border:3px solid #20B2A6;box-shadow:0 5px 0 #138A80' : (bad ? 'color:#1F2A5A;background:#FFE0E0;border:3px solid #FF6B6B;box-shadow:0 5px 0 #D85C5C' : 'color:#1F2A5A;background:#FFF6D6;border:3px solid #FFC93C;box-shadow:0 5px 0 #E39A00')) : 'background:radial-gradient(circle at 30% 24%,rgba(255,255,255,.45) 0,rgba(255,255,255,0) 45%),#7B5CFF;border:3px solid #5A3FD1;color:#fff;box-shadow:0 6px 0 #5A3FD1,0 12px 12px rgba(31,42,90,.22)') }; }) : [],
""")
    # 6 balloons twice as slow
    s = rep(s, "blDur(i) { return Math.max(4.4, 7.6 - i * 0.4); }", "blDur(i) { return Math.max(8.8, 15.2 - i * 0.8); }")
    # 7 games list: levels 1,1,2,2,3,4,5
    s = rx(s, r"gameItems: \[\[.*?\]\]\.map\(\(g, gi\)", "gameItems: [['✍️', 'أكمل الكلمة', 'اختر الكلمة الناقصة في الذكر', 1, 'startCloze'], ['🧩', 'رتّب الذكر', 'رتّب كلمات الذكر بالترتيب الصحيح', 1, 'startOrder'], ['🃏', 'ذاكرة الأذكار', 'احفظ أماكن البطاقات ثم اختر الصحيحة', 2, 'startMemory'], ['🎈', 'بالونات الذكر', 'فرقع بالونة الكلمة الصحيحة قبل أن تطير', 2, 'startBalloons'], ['⭐', 'صيد النجوم', 'التقط النجوم الساقطة بسرعة', 3, 'startStars'], ['⚡', 'صح أم خطأ', 'هل الذكر مكتوب صحيحًا؟ أجب بسرعة', 4, 'startQuick'], ['🚂', 'سباق القطار', 'أجب عن الأسئلة ليسبق قطارك', 5, 'startRace']].map((g, gi)")
    s = rx(s, r"go: \(\) => ok && gi === 5 \? this\.startBalloons\(\).*?: this\.say\(", "go: () => ok ? this[g[4]]() : this.say(")
    # 8 badge + game per level
    s = rep(s, "const LBE = { 1: '⭐', 2: '🌙', 3: '☀️', 4: '🌟', 5: '🏆' };", "const LBE = { 1: '⭐', 2: '🌙', 3: '☀️', 4: '🌟', 5: '🏆' };\n" + GL)
    s = rep(s, "sub: this.dayList(n, 1).map((c) => P[c[0]].s).slice(0, 3).join('، ') + '…',", "sub: 'الشارة ' + LBE[n] + ' · 🎮 ' + GL[n].join(' + '),")
    s = rep(s, " + ar(nl) + '!')", " + ar(nl) + '! 🎮 ' + t('فتحتَ', 'فتحتِ') + ' لعبة: ' + GL[nl].join(' + '))")
    open(f, 'w', encoding='utf8').write(s); print('patched', f)
