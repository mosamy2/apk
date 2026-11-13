/* Mini runtime for the .dc.html pages: DCLogic, {{holes}}, <sc-if>, <sc-for>, DOM morphing. */
(function () {
  'use strict';
  class DCLogic {
    constructor(props) { this.props = props || {}; this.state = {}; this.__q = false; }
    setState(patch, cb) {
      const p = typeof patch === 'function' ? patch(this.state) : patch;
      if (p) Object.assign(this.state, p);
      if (typeof cb === 'function') { try { cb(); } catch (e) { console.error(e); } }
      this.__schedule && this.__schedule();
    }
  }
  window.DCLogic = DCLogic;

  const HOLE = /\{\{\s*([^}]*?)\s*\}\}/g;
  const WHOLE = /^\s*\{\{\s*([^}]*?)\s*\}\}\s*$/;

  function lookup(path, ctx, vals) {
    const parts = path.split('.');
    let cur;
    if (parts[0] in ctx) cur = ctx[parts[0]];
    else cur = vals[parts[0]];
    for (let i = 1; i < parts.length; i++) { if (cur == null) return undefined; cur = cur[parts[i]]; }
    return cur;
  }
  function evalHole(expr, ctx, vals) {
    if (expr === 'true') return true;
    if (expr === 'false') return false;
    if (expr === 'null') return null;
    return lookup(expr, ctx, vals);
  }
  function interp(str, ctx, vals) {
    return str.replace(HOLE, (_, e) => { const v = evalHole(e, ctx, vals); return v == null || v === false ? '' : String(v); });
  }

  const SVGNS = 'http://www.w3.org/2000/svg';

  function build(node, ctx, vals, out) {
    if (node.nodeType === 3) { out.appendChild(document.createTextNode(interp(node.nodeValue, ctx, vals))); return; }
    if (node.nodeType !== 1) return;
    const name = node.localName.toLowerCase();
    if (name === 'sc-if') {
      const m = WHOLE.exec(node.getAttribute('value') || '');
      const v = m ? evalHole(m[1], ctx, vals) : false;
      if (v) for (const c of node.childNodes) build(c, ctx, vals, out);
      return;
    }
    if (name === 'sc-for') {
      const m = WHOLE.exec(node.getAttribute('list') || '');
      const list = (m && evalHole(m[1], ctx, vals)) || [];
      const as = node.getAttribute('as') || 'item';
      let i = 0;
      for (const item of list) {
        const c2 = Object.assign({}, ctx); c2[as] = item; c2.index = i++;
        for (const c of node.childNodes) build(c, c2, vals, out);
      }
      return;
    }
    const el = node.namespaceURI === SVGNS ? document.createElementNS(SVGNS, node.localName) : document.createElement(node.localName);
    for (const a of Array.from(node.attributes)) {
      const an = a.name;
      if (an.indexOf('hint-') === 0) continue;
      const m = WHOLE.exec(a.value);
      if (/^on[a-z]+$/i.test(an) && m) {
        const fn = evalHole(m[1], ctx, vals);
        if (typeof fn === 'function') { const ev = an.slice(2).toLowerCase(); (el.__h = el.__h || {})[ev] = fn; el['on' + ev] = fn; }
        continue;
      }
      let val;
      if (m) {
        val = evalHole(m[1], ctx, vals);
        if (val === false || val == null) continue;
        if (val === true) val = '';
      } else val = interp(a.value, ctx, vals);
      try { el.setAttribute(an, String(val)); } catch (e) { /* ignore bad names */ }
    }
    for (const c of node.childNodes) build(c, ctx, vals, el);
    out.appendChild(el);
  }

  function syncHandlers(live, next) {
    const nh = next.__h || {}, lh = live.__h || {};
    for (const k in lh) if (!(k in nh)) live['on' + k] = null;
    for (const k in nh) live['on' + k] = nh[k];
    live.__h = nh;
  }
  function morphEl(live, next) {
    // attributes
    for (const a of Array.from(live.attributes)) if (!next.hasAttribute(a.name)) live.removeAttribute(a.name);
    for (const a of Array.from(next.attributes)) if (live.getAttribute(a.name) !== a.value) live.setAttribute(a.name, a.value);
    if (live.localName === 'input') {
      const v = next.getAttribute('value');
      if (v != null && live.value !== v && document.activeElement !== live) live.value = v;
    }
    syncHandlers(live, next);
    morphKids(live, next);
  }
  function morphKids(live, next) {
    const nk = Array.from(next.childNodes);
    let i = 0;
    for (; i < nk.length; i++) {
      const n = nk[i], l = live.childNodes[i];
      if (!l) { live.appendChild(n); continue; }
      if (l.nodeType === 3 && n.nodeType === 3) { if (l.nodeValue !== n.nodeValue) l.nodeValue = n.nodeValue; continue; }
      if (l.nodeType === 1 && n.nodeType === 1 && l.localName === n.localName && l.namespaceURI === n.namespaceURI) { morphEl(l, n); continue; }
      live.replaceChild(n, l);
    }
    while (live.childNodes.length > nk.length) live.removeChild(live.lastChild);
  }

  /* scroll=true: fill the screen width and let the page scroll up/down with the finger */
  function fit(stage, w, h, scroll) {
    const vw = window.innerWidth, vh = window.innerHeight;
    const tall = h > 850 || (scroll && (h * vw / w) > vh + 1);
    let k = Math.min(vw / w, vh / h);
    if (tall) k = vw / w; // fit width and scroll
    stage.style.transform = 'scale(' + k + ')';
    stage.style.transformOrigin = 'top left';
    const sw = w * k, sh = h * k;
    stage.style.left = Math.max(0, (vw - sw) / 2) + 'px';
    stage.style.top = tall ? '0px' : Math.max(0, (vh - sh) / 2) + 'px';
    document.getElementById('spacer').style.height = (tall ? sh : 0) + 'px';
    document.documentElement.style.overflowY = tall ? 'auto' : 'hidden';
    document.body.style.overflowY = tall ? 'auto' : 'hidden';
  }

  window.DC = {
    mount(Component, opt) {
      const w = opt.w, h = opt.h;
      const tplText = document.getElementById('tpl').textContent;
      const t = document.createElement('template');
      t.innerHTML = tplText;
      const tpl = t.content;
      const root = document.getElementById('root');
      const stage = document.getElementById('stage');
      stage.style.width = w + 'px'; stage.style.height = h + 'px';
      const inst = new Component({});
      let first = true, pending = false, scroll = false;
      const render = () => {
        pending = false;
        let vals;
        try { vals = inst.renderVals() || {}; } catch (e) { console.error('renderVals', e); return; }
        const out = document.createElement('div');
        for (const c of tpl.childNodes) build(c, {}, vals, out);
        if (first) {
          while (out.firstChild) root.appendChild(out.firstChild);
          first = false;
          const fe = root.firstElementChild;
          if (fe) { const bg = fe.style.backgroundColor || fe.style.background; if (bg) document.body.style.background = bg; }
        } else morphKids(root, out);
        let sc = false; try { sc = typeof inst.scrollable === 'function' && !!inst.scrollable(); } catch (e) {}
        if (sc !== scroll) { scroll = sc; fit(stage, w, h, scroll); if (!sc) window.scrollTo(0, 0); }
      };
      inst.__schedule = () => { if (!pending) { pending = true; Promise.resolve().then(render); } };
      window.addEventListener('resize', () => fit(stage, w, h, scroll));
      fit(stage, w, h, scroll);
      window.__dc = inst;
      render();
    }
  };
})();
