// Converts src/*.dc.html (design pages) into standalone pages in www/
import fs from 'fs';
import path from 'path';
const SRC = 'src', OUT = 'www';
fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(OUT, { recursive: true });
fs.copyFileSync('tools/runtime.js', path.join(OUT, 'runtime.js'));
for (const f of ['manifest.webmanifest', 'icon-192.png', 'icon-512.png']) if (fs.existsSync('tools/' + f)) fs.copyFileSync('tools/' + f, path.join(OUT, f));
const TKA = { boy: {}, girl: {}, husary: {} };
if (fs.existsSync('audio')) {
  fs.mkdirSync(path.join(OUT, 'audio'), { recursive: true });
  for (const f of fs.readdirSync('audio')) {
    const m = /^(boy|girl|husary)_([a-z]+)\.(mp3|m4a|ogg|wav)$/.exec(f);
    if (!m) continue;
    fs.copyFileSync(path.join('audio', f), path.join(OUT, 'audio', f));
    TKA[m[1]][m[2]] = 'audio/' + f;
  }
}
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
<script>window.TK_AUDIO=${JSON.stringify(TKA)};</script>
<title>${title}</title>
<style>html,body{margin:0;height:100%;overflow-x:hidden;-webkit-tap-highlight-color:transparent;-webkit-user-select:none;user-select:none}input{-webkit-user-select:text;user-select:text}#stage{position:absolute;overflow:hidden}</style>
${helmet}
</head>
<body>
<div id="spacer"></div>
<div id="stage"><div id="root"></div></div>
<script type="text/x-dc-template" id="tpl">${tpl}</script>
<script src="runtime.js"></script>
<script>
${fix(script).replace(/<\/script/g, "<\\/script")}
DC.mount(Component, { w: ${w}, h: ${h} });
</script>
</body>
</html>
`;
  fs.writeFileSync(path.join(OUT, file.replace('.dc.html', '.html')), page);
}
fs.writeFileSync(path.join(OUT, 'index.html'), '<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=Start.html"><script>location.replace("Start.html")</script>');
console.log('built', fs.readdirSync(OUT).join(' '));
