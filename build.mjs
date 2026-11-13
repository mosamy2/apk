// Converts src/*.dc.html (design pages) into standalone pages in www/
import fs from 'fs';
import path from 'path';
const SRC = 'src', OUT = 'www';
fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(OUT, { recursive: true });
fs.copyFileSync('tools/runtime.js', path.join(OUT, 'runtime.js'));
const CAPJS = 'node_modules/@capacitor/core/dist/capacitor.js';
if (fs.existsSync(CAPJS)) fs.copyFileSync(CAPJS, path.join(OUT, 'capacitor.js')); // gives window.Capacitor.registerPlugin on the phone
for (const f of ['manifest.webmanifest', 'icon-192.png', 'icon-512.png', 'tkstore.js']) if (fs.existsSync('tools/' + f)) fs.copyFileSync('tools/' + f, path.join(OUT, f));
const TKA = { boy: {}, girl: {}, husary: {}, fx: {} };
if (fs.existsSync('audio')) {
  fs.mkdirSync(path.join(OUT, 'audio'), { recursive: true });
  for (const f of fs.readdirSync('audio')) {
    const m = /^(boy|girl|husary|fx)_([a-z]+)\.(mp3|m4a|ogg|wav)$/.exec(f);
    if (!m) continue;
    fs.copyFileSync(path.join('audio', f), path.join(OUT, 'audio', f));
    TKA[m[1]][m[2]] = 'audio/' + f;
  }
}
let TKT = {};
if (fs.existsSync('audio/timings.json')) { const t = JSON.parse(fs.readFileSync('audio/timings.json', 'utf8')); for (const k in t) TKT[k] = t[k].words.map((w) => w.s); }
const FX3D_CSS = `button,a[href]{transition:transform .15s ease,box-shadow .15s ease,filter .15s}
button:active,a[href]:active{transform:translateY(4px) scale(.97)!important;filter:brightness(.96)}
input:focus{outline:0;transform:translateY(-2px);box-shadow:0 6px 0 rgba(255,138,61,.35),0 10px 14px rgba(31,42,90,.15)}
@keyframes pageIn3d{0%{opacity:0;transform:perspective(900px) translateY(26px) rotateX(10deg)}100%{opacity:1;transform:perspective(900px) translateY(0) rotateX(0)}}
@keyframes fx3dFloat{0%,100%{transform:translate3d(0,0,0) rotateY(0) rotateZ(-6deg)}50%{transform:translate3d(0,-16px,0) rotateY(180deg) rotateZ(6deg)}}
#root>*{animation:pageIn3d .7s cubic-bezier(.2,.8,.3,1) backwards}
.fx3d{position:absolute;left:0;top:0;right:0;bottom:0;pointer-events:none;z-index:2;overflow:hidden;perspective:600px}
.fx3d i{position:absolute;font-style:normal;filter:drop-shadow(0 6px 4px rgba(0,0,0,.25));animation:fx3dFloat 5s ease-in-out infinite}
@media (prefers-reduced-motion: reduce){#root>*,.fx3d i{animation:none!important}}`;
const FX3D_JS = `(function(){try{var st=document.getElementById('stage');if(!st)return;var d=document.createElement('div');d.className='fx3d';var E=['⭐','🌙','🎈','☁️','🌟','🦋'],P=[[8,8],[88,6],[4,92],[90,90],[92,48],[3,50]];E.forEach(function(e,i){var x=document.createElement('i');x.textContent=e;x.style.cssText='left:'+P[i][0]+'%;top:'+P[i][1]+'%;font-size:'+(22+(i%3)*6)+'px;animation-delay:'+(i*0.7)+'s;opacity:.85';d.appendChild(x)});st.appendChild(d)}catch(e){}})();`;
/* soft 'pop' on every button press (WebAudio, no files). Skips buttons that already make their own sound. */
const SFX_JS = `(function(){var ac=null,last=0;function ctx(){try{if(!ac){var C=window.AudioContext||window.webkitAudioContext;if(C)ac=new C();}if(ac&&ac.state==='suspended')ac.resume();}catch(e){}return ac;}
function muted(){try{var d=window.__dc;return !!(d&&d.state&&d.state.muted);}catch(e){return false;}}
function pop(kind){var a=ctx();if(!a)return;try{var t=a.currentTime+0.005,o=a.createOscillator(),g=a.createGain(),f=kind==='sw'?520:(kind==='nav'?660:760);o.type='sine';o.frequency.setValueAtTime(f,t);o.frequency.exponentialRampToValueAtTime(f*1.9,t+0.07);g.gain.setValueAtTime(0.0001,t);g.gain.exponentialRampToValueAtTime(0.16,t+0.012);g.gain.exponentialRampToValueAtTime(0.0001,t+0.11);o.connect(g);g.connect(a.destination);o.start(t);o.stop(t+0.13);
var o2=a.createOscillator(),g2=a.createGain();o2.type='triangle';o2.frequency.setValueAtTime(f*2.5,t+0.035);g2.gain.setValueAtTime(0.0001,t+0.035);g2.gain.exponentialRampToValueAtTime(0.05,t+0.045);g2.gain.exponentialRampToValueAtTime(0.0001,t+0.12);o2.connect(g2);g2.connect(a.destination);o2.start(t+0.035);o2.stop(t+0.14);}catch(e){}}
var SKIP=/^(سبّح|اضغط الجرس)/;
document.addEventListener('pointerdown',function(e){var b=e.target&&e.target.closest&&e.target.closest('button,a[href],[role=switch]');if(!b||b.disabled||b.hasAttribute('data-nosfx'))return;var l=b.getAttribute('aria-label')||'';if(SKIP.test(l)||muted())return;var n=Date.now();if(n-last<60)return;last=n;pop(b.getAttribute('role')==='switch'?'sw':(b.tagName==='A'?'nav':'btn'));},true);})();`;
const fix = (s) => s.replace(/(["'(])([A-Za-z]+)\.dc\.html/g, '$1$2.html');
for (const file of fs.readdirSync(SRC).filter((f) => f.endsWith('.dc.html'))) {
  const html = fs.readFileSync(path.join(SRC, file), 'utf8');
  const title = (html.match(/<title>([^<]*)<\/title>/) || [, 'سبحة الأبطال'])[1];
  const xdc = html.match(/<x-dc>([\s\S]*?)<\/x-dc>/)[1];
  const helmet = (xdc.match(/<helmet>([\s\S]*?)<\/helmet>/) || [, ''])[1];
  const tpl = fix(xdc.replace(/<helmet>[\s\S]*?<\/helmet>/, ''));
  const script = html.match(/<script type="text\/x-dc"[^>]*>([\s\S]*?)<\/script>/)[1];
  const props = JSON.parse(html.match(/data-props='([^']*)'/)[1]);
  const { width: w, height: h } = props.$preview;
  const page = `<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no">
<meta name="theme-color" content="#7B5CFF">
<link rel="manifest" href="manifest.webmanifest">
${fs.existsSync(path.join(OUT, 'capacitor.js')) ? '<script src="capacitor.js"></script>' : ''}
<script src="tkstore.js"></script>
<script>window.TK_AUDIO=${JSON.stringify(TKA)};window.TK_TIMES=${JSON.stringify(TKT)};</script>
<title>${title}</title>
<style>html,body{margin:0;height:100%;overflow-x:hidden;-webkit-tap-highlight-color:transparent;-webkit-user-select:none;user-select:none}input{-webkit-user-select:text;user-select:text}#stage{position:absolute;overflow:hidden}</style>
${helmet}
<style>${FX3D_CSS}</style>
</head>
<body>
<div id="spacer"></div>
<div id="stage"><div id="root"></div></div>
<script type="text/x-dc-template" id="tpl">${tpl}</script>
<script src="runtime.js"></script>
<script>
${fix(script).replace(/<\/script/g, "<\\/script")}
DC.mount(Component, { w: ${w}, h: ${h} });
${SFX_JS}
${/^Main/.test(file) ? '' : FX3D_JS}
</script>
</body>
</html>
`;
  fs.writeFileSync(path.join(OUT, file.replace('.dc.html', '.html')), page);
}
fs.writeFileSync(path.join(OUT, 'index.html'), '<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=Start.html"><script>location.replace("Start.html")</script>');
console.log('built', fs.readdirSync(OUT).join(' '));
