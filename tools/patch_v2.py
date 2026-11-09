import re,sys
for f in ['src/Main.dc.html','src/MainGirl.dc.html']:
    s=open(f).read()
    def rep(a,b,cnt=1):
        global s
        assert s.count(a)==cnt,(f,a[:60],s.count(a))
        s=s.replace(a,b)
    # state fields
    rep("passed: false };\n", "passed: false, dayDate: null, shift: 0, hist: [] };\n") if "passed: false };\n" in s else rep("lvStars: 0, passed: false };","lvStars: 0, passed: false, dayDate: null, shift: 0, hist: [] };")
    # load db + helpers after this.g line
    m=re.search(r"this\.g = '(boy|girl)'; try \{ this\.nm = [^\n]*\n",s); assert m
    load = m.group(0) + """this.dbKey = 'tk_db_' + this.g;
try { const db = JSON.parse(window.localStorage.getItem(this.dbKey)); if (db && db.v === 1 && db.s) { Object.assign(this.state, db.s, { view: 'map', count: 0, gain: 0, riding: false, ringing: false, popping: false, lock: false, burst: false, toast: '', vstat: '' }); if (this.state.tab === 'pm') Object.assign(this.state, { tab: 'am', progress: this.state.alt, alt: this.state.progress }); } } catch (e) {}
{ const p0 = this.rollDay(); if (p0) Object.assign(this.state, p0, { view: p0.passed ? 'levelend' : 'map' }); }
try { const chk = () => { const p = this.rollDay(); if (p && !this.state.riding && this.state.view !== 'play') { this.clearAll(); this.setState(Object.assign({}, p, { view: p.passed ? 'levelend' : 'map', count: 0, gain: 0, lock: false })); this.say(p.passed ? 'أحسنت! أنهيت المستوى' : 'يوم جديد! اليوم ' + this.ar(p.day) + (p.day > 4 ? '' : ' من ٤'), ''); } }; document.addEventListener('visibilitychange', () => { if (!document.hidden) chk(); }); setInterval(chk, 60000); } catch (e) {}
"""
    s=s.replace(m.group(0),load)
    # helper methods after ar()
    rep("ar(n) { return String(n).replace(/\\d/g, (d) => '٠١٢٣٤٥٦٧٨٩'[d]); }\n","""ar(n) { return String(n).replace(/\\d/g, (d) => '٠١٢٣٤٥٦٧٨٩'[d]); }
today() { const d = new Date(Date.now() + (this.state.shift || 0) * 864e5); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
pmMin() { let m = 900; try { const t = JSON.parse(window.localStorage.getItem('tk_times_' + this.g)); if (t && t.pmT) m = t.pmT; } catch (e) {} return m; }
pmOpen() { const n = new Date(); return n.getHours() * 60 + n.getMinutes() >= this.pmMin(); }
rollDay() {
const s = this.state, t = this.today();
if (!s.dayDate) { s.dayDate = t; return null; }
if (t <= s.dayDate) return null;
const amP = s.tab === 'am' ? s.progress : s.alt;
if (s.passed || amP === 0) return { dayDate: t, gameStars: 0, alt: s.tab === 'am' ? 0 : s.alt, passed: s.passed, day: s.day };
const e = this.evalLevel(s.lvStars, s.lvSt, s.day);
const hist = (s.hist || []).concat([{ d: s.dayDate, level: s.level, day: s.day, stars: s.stars, st: amP }]).slice(-400);
if (e.pass) return { dayDate: t, passed: true, maxDone: Math.max(s.maxDone || 0, s.level), hist, day: s.day };
return { dayDate: t, day: s.day + 1, progress: 0, alt: 0, gameStars: 0, tab: 'am', hist, passed: false };
}
""")
    # level end button: wait for the next real day
    rep("lendGo: () => { if (s.passed) { if (s.level < 5) this.startLevel(nl); else this.setState({ view: 'rewards' }); } else this.nextDay(); },",
        "lendGo: () => { if (s.passed) { if (s.level < 5) this.startLevel(nl); else this.setState({ view: 'rewards' }); } else { const p = this.rollDay(); if (p) { this.clearAll(); this.setState(Object.assign({}, p, { view: p.passed ? 'levelend' : 'map', count: 0, gain: 0, lock: false })); this.say('يوم جديد! اليوم ' + this.ar(p.day) + (p.day > 4 ? '' : ' من ٤'), ''); } else { this.setState({ view: 'map' }); this.say(this.g === 'girl' ? 'أحسنتِ! ارجعي غدًا لليوم ' + this.ar(Math.min(s.day + 1, 99)) + ' بإذن الله' : 'أحسنت! ارجع غدًا لليوم ' + this.ar(Math.min(s.day + 1, 99)) + ' بإذن الله', ''); } } },")
    rep("lendBtn: s.passed ? (s.level < 5 ? 'ابدأ المستوى ' + ar(nl) : 'مكافآتي') : 'يوم جديد (تجربة الغد)',","lendBtn: s.passed ? (s.level < 5 ? 'ابدأ المستوى ' + ar(nl) : 'مكافآتي') : 'حسنًا، إلى الخريطة',")
    # test button tomorrow: move date one day and roll
    rep("nextDayBtn: () => this.nextDay(),","nextDayBtn: () => { if (s.riding || s.view === 'cheer') return; this.setState({ shift: (s.shift || 0) + 1 }); const p = this.rollDay(); if (p) { this.clearAll(); this.setState(Object.assign({}, p, { view: p.passed ? 'levelend' : 'map', count: 0, gain: 0, lock: false })); this.say(p.passed ? 'أنهيت المستوى!' : 'يوم جديد (تجربة الغد)', ''); } else this.say('انتقلنا ليوم تالٍ', ''); },")
    # evening gate
    rep("if (!TEST_UNLOCK_ALL) { this.say('تفتح أذكار المساء بعد العصر', ''); return; }","if (!TEST_UNLOCK_ALL && !this.pmOpen()) { const m = this.pmMin(); this.say('تفتح أذكار المساء بعد العصر (الساعة ' + this.ar(String(Math.floor(m / 60)).padStart(2, '0') + ':' + String(m % 60).padStart(2, '0')) + ')', ''); return; }")
    # reset also resets date and history
    rep("saves: {}, alt: 0, gameStars: 0 }); },","saves: {}, alt: 0, gameStars: 0, shift: 0, dayDate: this.today(), hist: [] }); },")
    # long text fit
    rep('<div style="font-size:{{dFont}}px;font-weight:700;line-height:1.7;max-height:150px;overflow-y:auto">','<div style="{{dBox}}">')
    rep("dText: d.t, dHelp: d.h, dFont: d.f,","dText: d.t, dHelp: d.h, dFont: d.f, dBox: 'font-size:' + (d.t.length <= 35 ? 34 : d.t.length <= 70 ? 26 : d.t.length <= 110 ? 22 : d.t.length <= 170 ? 19 : d.t.length <= 300 ? 16 : 14) + 'px;font-weight:700;line-height:1.6;overflow-y:auto;max-height:' + (d.t.length > 200 ? 270 : 170) + 'px',")
    # db write
    rep("try { const lv = JSON.stringify(","try { const o = {}; ['level','tab','progress','alt','stars','saves','gameStars','maxDone','day','lvSt','lvStars','passed','muted','dayDate','shift','hist'].forEach((k) => { o[k] = s[k]; }); const js = JSON.stringify({ v: 1, t: Date.now(), s: o }); if (js !== this.lastDb) { this.lastDb = js; window.localStorage.setItem(this.dbKey, js); } } catch (e) {}\ntry { const lv = JSON.stringify(")
    open(f,'w').write(s)
print('ok')
