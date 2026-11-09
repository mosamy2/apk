# سبحة الأبطال (Tasbeeh Kids)

- `src/` : صفحات التصميم (`*.dc.html`)
- `build.mjs` + `tools/runtime.js` : يحوّلها لتطبيق ويب مستقل في `www/`
- `.github/workflows/build-apk.yml` : يبني ملف APK تلقائيًا (Actions ← آخر تشغيل ← Artifacts ← tasbeeh-kids-apk)

للتشغيل محليًا: `npm install && npm run build` ثم افتح `www/index.html` عبر خادم محلي.
