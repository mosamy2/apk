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
    kid: function (id) { var a = TK.acct(); if (!a) return null; for (var i = 0; i < a.kids.length; i++) if (a.kids[i].id === id) return a.kids[i]; return null; },
    kidHref: function (k) { return (k.g === 'girl' ? 'MainGirl.html' : 'Main.html') + '?k=' + encodeURIComponent(k.id); },
    qs: function (k) { try { return new URLSearchParams(window.location.search).get(k); } catch (e) { return null; } },
    go: function (url) { window.location.href = url; }
  };
  window.TK = TK;
})();
