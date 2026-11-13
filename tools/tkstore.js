/* Parent account + children registry, kept on the device (localStorage). */
(function () {
  'use strict';
  var A = 'tk_acct';
  function nz(s) { return String(s == null ? '' : s).replace(/[٠-٩]/g, function (d) { return '٠١٢٣٤٥٦٧٨٩'.indexOf(d); }).replace(/[۰-۹]/g, function (d) { return '۰۱۲۳۴۵۶۷۸۹'.indexOf(d); }); }
  function hash(str) { // cyrb53 x2: not cryptographic, only keeps the PIN from sitting in plain text
    var out = '';
    [11, 97].forEach(function (seed) {
      var h1 = 0xdeadbeef ^ seed, h2 = 0x41c6ce57 ^ seed;
      for (var i = 0, ch; i < str.length; i++) { ch = str.charCodeAt(i); h1 = Math.imul(h1 ^ ch, 2654435761); h2 = Math.imul(h2 ^ ch, 1597334677); }
      h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507) ^ Math.imul(h2 ^ (h2 >>> 13), 3266489909);
      h2 = Math.imul(h2 ^ (h2 >>> 16), 2246822507) ^ Math.imul(h1 ^ (h1 >>> 13), 3266489909);
      out += (4294967296 * (2097151 & h2) + (h1 >>> 0)).toString(36);
    });
    return out;
  }
  var TK = {
    nz: nz,
    phone: function (s) { var p = nz(s).replace(/[\s\-()]/g, ''); return /^\+?\d{8,15}$/.test(p) ? p : null; },
    same: function (a, b) { var x = nz(a).replace(/\D/g, ''), y = nz(b).replace(/\D/g, ''); return x.length >= 9 && y.length >= 9 ? x.slice(-9) === y.slice(-9) : x === y; },
    pinOk: function (s) { var p = nz(s).trim(); return /^(\d{4}|\d{6})$/.test(p) ? p : null; },
    acct: function () { try { var a = JSON.parse(window.localStorage.getItem(A)); return a && a.phone && a.ph && Array.isArray(a.kids) ? a : null; } catch (e) { return null; } },
    save: function (a) { window.localStorage.setItem(A, JSON.stringify(a)); },
    wipe: function () { var ks = [], i; for (i = 0; i < window.localStorage.length; i++) { var k = window.localStorage.key(i); if (/^tk_/.test(k)) ks.push(k); } ks.forEach(function (k) { window.localStorage.removeItem(k); }); },
    create: function (phone, pin) { TK.wipe(); var a = { v: 1, phone: phone, len: pin.length, ph: hash(pin + '|' + phone), kids: [], t: Date.now() }; TK.save(a); return a; },
    checkPin: function (pin) { var a = TK.acct(); return !!a && a.ph === hash(nz(pin) + '|' + a.phone); },
    setPin: function (pin) { var a = TK.acct(); if (!a) return; a.len = pin.length; a.ph = hash(pin + '|' + a.phone); TK.save(a); },
    addKid: function (name, g) { var a = TK.acct(); if (!a) return null; var k = { id: 'k' + Date.now().toString(36) + Math.floor(Math.random() * 1296).toString(36), name: String(name).trim(), g: g === 'girl' ? 'girl' : 'boy' }; a.kids.push(k); TK.save(a); return k; },
    updateKid: function (id, name, g) { var a = TK.acct(); if (!a) return false; for (var i = 0; i < a.kids.length; i++) if (a.kids[i].id === id) { a.kids[i].name = String(name).trim(); a.kids[i].g = g === 'girl' ? 'girl' : 'boy'; TK.save(a); return true; } return false; },
    delKid: function (id) { var a = TK.acct(); if (!a) return false; var n = a.kids.length; a.kids = a.kids.filter(function (k) { return k.id !== id; });  if (a.kids.length === n) return false; TK.save(a); ['tk_db_', 'tk_times_', 'tk_live_', 'tk_fired_', 'tk_skip_'].forEach(function (p) { try { window.localStorage.removeItem(p + id); } catch (e) {} }); return true; },
    times: function (id) { var t = null; try { t = JSON.parse(window.localStorage.getItem('tk_times_' + id)); } catch (e) {} t = t || {}; return { amT: t.amT || 390, pmT: t.pmT || 900, am: t.am !== false, pm: t.pm !== false, sound: t.snd || (t.sound === 'off' ? 'off' : 'fun') }; },
    setTimes: function (id, t) { try { window.localStorage.setItem('tk_times_' + id, JSON.stringify(t)); } catch (e) {} },
    markSetup: function () { var a = TK.acct(); if (!a) return; a.setup = true; TK.save(a); },
    kid: function (id) { var a = TK.acct(); if (!a) return null; for (var i = 0; i < a.kids.length; i++) if (a.kids[i].id === id) return a.kids[i]; return null; },
    kidHref: function (k) { return (k.g === 'girl' ? 'MainGirl.html' : 'Main.html') + '?k=' + encodeURIComponent(k.id); },
    qs: function (k) { try { return new URLSearchParams(window.location.search).get(k); } catch (e) { return null; } },
    go: function (url) { window.location.href = url; }
  };
  /* ---- reminders: real phone notifications (Capacitor Local Notifications) ---- */
  function today(d) { d = d || new Date(); return d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate(); }
  function hash32(str) { var h = 7; for (var i = 0; i < str.length; i++) h = (Math.imul(h, 31) + str.charCodeAt(i)) >>> 0; return h % 90000; }
  /* Talks to the native LocalNotifications plugin. The pages do not bundle @capacitor/core's
     registerPlugin by default, so fall back to the bridge's nativePromise directly. */
  var LNP = null;
  function lnPlugin() {
    if (LNP) return LNP;
    var C = window.Capacitor; if (!C) return null;
    if (typeof C.registerPlugin === 'function') { try { LNP = (C.Plugins && C.Plugins.LocalNotifications) || C.registerPlugin('LocalNotifications'); return LNP; } catch (e) {} }
    if (typeof C.nativePromise === 'function') {
      var call = function (m) { return function (o) { return C.nativePromise('LocalNotifications', m, o || {}); }; };
      LNP = {}; ['checkPermissions', 'requestPermissions', 'createChannel', 'deleteChannel', 'listChannels', 'getPending', 'cancel', 'schedule', 'checkExactNotificationSetting', 'changeExactNotificationSetting'].forEach(function (m) { LNP[m] = call(m); });
      return LNP;
    }
    return null;
  }
  /* tone -> notification channel. 'fun' = the kid's own voice alert (boy/girl), the main one. */
  var CH = {
    fun_boy: { id: 'tk_fun_boy_v2', name: 'تنبيه مرح (ولد)', sound: 'boy_alerts.mp3' },
    fun_girl: { id: 'tk_fun_girl_v2', name: 'تنبيه مرح (بنت)', sound: 'girl_alerts.mp3' },
    soft: { id: 'tk_soft_v2', name: 'تنبيه هادئ', sound: 'fx_soft.mp3' },
    off: { id: 'tk_quiet_v2', name: 'تنبيه بدون صوت', sound: null }
  };
  function chFor(tone, girl) { return tone === 'off' ? CH.off : (tone === 'soft' ? CH.soft : (girl ? CH.fun_girl : CH.fun_boy)); }
  function toISO(d) { return new Date(d).toISOString(); }
  var chReady = null;
  var N = {
    DAYS: 14,
    native: function () { try { return !!(window.Capacitor && window.Capacitor.isNativePlatform && window.Capacitor.isNativePlatform()); } catch (e) { return false; } },
    plugin: function () { try { return N.native() ? lnPlugin() : null; } catch (e) { return null; } },
    base: function (kid, slot) { return (hash32(kid + '|' + slot) + 1) * 20; },
    skipped: function (kid, slot) { try { var s = JSON.parse(window.localStorage.getItem('tk_skip_' + kid)) || {}; return s[slot] === today(); } catch (e) { return false; } },
    /* tone file for in-app playback */
    toneUrl: function (tone, girl) { var A = window.TK_AUDIO || {}; if (tone === 'off') return null; if (tone === 'soft') return (A.fx || {}).soft || null; return (A[girl ? 'girl' : 'boy'] || {}).alerts || null; },
    /* plan: list of {id, at:Date, kid, slot} for the next DAYS days */
    plan: function (now) {
      var a = TK.acct(), out = []; now = now || new Date(); if (!a) return out;
      a.kids.forEach(function (k) {
        var t = TK.times(k.id);
        [['am', t.am, t.amT], ['pm', t.pm, t.pmT]].forEach(function (x) {
          if (!x[1]) return;
          for (var d = 0; d < N.DAYS; d++) {
            var at = new Date(now.getFullYear(), now.getMonth(), now.getDate() + d, Math.floor(x[2] / 60), x[2] % 60, 0, 0);
            if (at.getTime() <= now.getTime() + 5000) continue;
            if (d === 0 && N.skipped(k.id, x[0])) continue;
            out.push({ id: N.base(k.id, x[0]) + d, at: at, kid: k.id, name: k.name, girl: k.g === 'girl', slot: x[0], tone: t.sound });
          }
        });
      });
      return out;
    },
    /* 'granted' | 'denied' | 'prompt' | 'web' */
    status: function () {
      var LN = N.plugin(); if (!LN) return Promise.resolve('web');
      return LN.checkPermissions().then(function (p) { return p.display === 'granted' ? 'granted' : (p.display === 'denied' ? 'denied' : 'prompt'); }, function () { return 'prompt'; });
    },
    /* 'granted' | 'denied' | 'web' (Android 12+ "alarms & reminders" setting) */
    exact: function () {
      var LN = N.plugin(); if (!LN || !LN.checkExactNotificationSetting) return Promise.resolve('web');
      return LN.checkExactNotificationSetting().then(function (r) { return r && r.exact_alarm === 'denied' ? 'denied' : 'granted'; }, function () { return 'granted'; });
    },
    openExact: function () { var LN = N.plugin(); if (!LN || !LN.changeExactNotificationSetting) return Promise.resolve(); return LN.changeExactNotificationSetting().catch(function () {}); },
    /* ask the user for notification permission (Android 13+ shows the system dialog) */
    ask: function () {
      var LN = N.plugin(); if (!LN) return Promise.resolve('web');
      return LN.requestPermissions().then(function (p) { return p.display === 'granted' ? 'granted' : 'denied'; }, function () { return 'denied'; });
    },
    channels: function (LN) {
      if (!chReady) chReady = Promise.all(Object.keys(CH).map(function (k) {
        var c = CH[k], o = { id: c.id, name: c.name, description: 'تذكير الطفل بأذكار الصباح والمساء', importance: 5, visibility: 1, vibration: true, lights: true, lightColor: '#7B5CFF' };
        if (c.sound) o.sound = c.sound;
        return LN.createChannel(o).catch(function () {});
      })).then(function () { ['tk_boy_v1', 'tk_girl_v1'].forEach(function (id) { try { LN.deleteChannel({ id: id }).catch(function () {}); } catch (e) {} }); });
      return chReady;
    },
    item: function (p) {
      var c = chFor(p.tone, p.girl);
      var o = { id: p.id, title: 'يا ' + p.name + ' ' + (p.slot === 'am' ? '🌅' : '🌙'), body: p.body || (p.slot === 'am' ? 'وقت أذكار الصباح، يلا نبدأ الرحلة!' : 'وقت أذكار المساء، يلا نبدأ الرحلة!'),
        schedule: { at: toISO(p.at), allowWhileIdle: true }, channelId: c.id, smallIcon: 'ic_stat_tk', iconColor: '#7B5CFF', autoCancel: true, extra: { k: p.kid } };
      if (c.sound) o.sound = c.sound;
      return o;
    },
    sync: function () {
      var LN = N.plugin(); if (!LN) return Promise.resolve(false);
      return LN.checkPermissions().then(function (p) { return p.display === 'granted' ? p : LN.requestPermissions(); }).then(function (p) {
        if (p.display !== 'granted') return false;
        return N.channels(LN).then(function () { return LN.getPending(); }).then(function (r) {
          var old = (r && r.notifications || []).filter(function (n) { return +n.id !== 7; }).map(function (n) { return { id: n.id }; }); /* 7 = test notification */
          return old.length ? LN.cancel({ notifications: old }) : null;
        }).then(function () {
          var list = N.plan().map(N.item);
          return list.length ? LN.schedule({ notifications: list }) : null;
        }).then(function () { return true; });
      }).catch(function (e) { try { console.error('notif sync', e); } catch (x) {} return false; });
    },
    /* real notification a few seconds from now, so the parent can see / hear it */
    test: function (kid, secs) {
      var LN = N.plugin(), k = TK.kid(kid); if (!LN) return Promise.resolve('web');
      var t = TK.times(kid), girl = k ? k.g === 'girl' : false, name = k ? k.name : 'بطلنا';
      return N.ask().then(function (st) {
        if (st !== 'granted') return st;
        return N.channels(LN).then(function () {
          return LN.schedule({ notifications: [N.item({ id: 7, at: new Date(Date.now() + (secs || 5) * 1000), kid: kid, name: name, girl: girl, slot: new Date().getHours() < 12 ? 'am' : 'pm', tone: t.sound, body: 'هذا تنبيه تجريبي، كده التنبيهات شغالة ✅' })] });
        }).then(function () { return 'ok'; }, function () { return 'fail'; });
      });
    },
    /* the child started this session in the 30 minutes before its reminder: drop today's reminder */
    skipToday: function (kid, slot) {
      try { var s = JSON.parse(window.localStorage.getItem('tk_skip_' + kid)) || {}; s[slot] = today(); window.localStorage.setItem('tk_skip_' + kid, JSON.stringify(s)); } catch (e) {}
      try { var f = JSON.parse(window.localStorage.getItem('tk_fired_' + kid)) || {}; f[slot] = today(); window.localStorage.setItem('tk_fired_' + kid, JSON.stringify(f)); } catch (e) {}
      var LN = N.plugin(); if (LN) { try { LN.cancel({ notifications: [{ id: N.base(kid, slot) }] }); } catch (e) {} }
    },
    inWindow: function (kid, slot, now) { now = now || new Date(); var t = TK.times(kid), at = slot === 'am' ? t.amT : t.pmT, m = now.getHours() * 60 + now.getMinutes(); return m >= at - 30 && m < at; }
  };
  TK.notif = N;
  window.TK = TK;
})();
