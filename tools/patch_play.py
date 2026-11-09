import re
for f in ['src/Main.dc.html','src/MainGirl.dc.html']:
    s=open(f).read()
    def rep(a,b,cnt=1):
        global s
        assert s.count(a)==cnt,(f,a[:70],s.count(a))
        s=s.replace(a,b)
    rep('<div style="padding:56px 20px 8px;display:flex;align-items:center;gap:12px">\n<button aria-label="رجوع للخريطة"','<div style="padding:44px 20px 6px;display:flex;align-items:center;gap:12px">\n<button aria-label="رجوع للخريطة"')
    rep('<div style="text-align:center;font-size:14px;font-weight:600;margin-top:4px">{{header}}</div>','<div style="text-align:center;font-size:13px;font-weight:600;margin:2px 0 8px">{{header}}</div>')
    # card
    rep('<div style="margin:12px 20px 0;border:3px solid #FFC93C;border-radius:24px;padding:20px 20px 18px;text-align:center;background:#fff;min-height:300px;box-sizing:border-box;display:flex;flex-direction:column;justify-content:center">',
        '<div style="position:relative;flex:1;min-height:0;margin:0 14px;border:3px solid #FFC93C;border-radius:24px;padding:18px 16px 12px;text-align:center;background:#fff;box-sizing:border-box;display:flex;flex-direction:column;justify-content:center">\n<button aria-label="اضغط الجرس لنقرأ الذكر معًا" onClick="{{ringBell}}" style="position:absolute;top:8px;left:8px;width:48px;height:48px;border-radius:24px;border:0;background:#FF8A3D;box-shadow:0 4px 0 #D86A1F;display:flex;align-items:center;justify-content:center;padding:0"><span style="display:flex;transform-origin:50% 10%;animation:{{bellAnim}}"><svg width="26" height="26" viewBox="0 0 24 24" fill="#fff" stroke="#fff" stroke-width="1.5" stroke-linejoin="round" aria-hidden="true"><path d="M12 3a6 6 0 0 0-6 6v4l-2 3h16l-2-3V9a6 6 0 0 0-6-6z"/><path d="M10 19a2 2 0 0 0 4 0"/></svg></span></button>')
    # help line smaller
    rep('<div style="font-size:15px;margin:2px 0 14px">{{dHelp}}</div>','<div style="font-size:13px;margin:8px 0 0;color:#44507F">{{dHelp}}</div>')
    # remove old bell row + label
    a=s.index('<div style="display:flex;align-items:center;justify-content:center;gap:10px;min-height:76px">')
    b=s.index('<div style="font-size:14px;font-weight:600;margin-top:8px">{{bellLabel}}</div>')+len('<div style="font-size:14px;font-weight:600;margin-top:8px">{{bellLabel}}</div>\n')
    s=s[:a]+s[b:]
    # bottom area
    rep('<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;position:relative">\n<div style="font-size:15px;font-weight:600">{{tapHint}}</div>','<div style="flex:none;display:flex;flex-direction:column;align-items:center;gap:8px;padding:10px 0 12px;position:relative">\n<div style="font-size:14px;font-weight:600">{{tapHint}}</div>')
    # mascot row compact
    rep('<div style="padding:0 20px 36px;display:flex;align-items:center;gap:12px"><div style="animation:{{mascotAnim}}"><svg width="60" height="60"','<div style="padding:0 20px 18px;display:flex;align-items:center;gap:10px"><div style="animation:{{mascotAnim}}"><svg width="44" height="44"')
    rep('<div style="flex:1;border-radius:18px;padding:12px 14px;background:#fff;font-size:15px;font-weight:600">{{msg}}</div>','<div style="flex:1;border-radius:16px;padding:8px 12px;background:#fff;font-size:14px;font-weight:600">{{msg}}</div>')
    # text box
    rep("dBox: 'font-size:' + (d.t.length <= 35 ? 34 : d.t.length <= 70 ? 26 : d.t.length <= 110 ? 22 : d.t.length <= 170 ? 19 : d.t.length <= 300 ? 16 : 14) + 'px;font-weight:700;line-height:1.6;overflow-y:auto;max-height:' + (d.t.length > 200 ? 270 : 170) + 'px',",
        "dBox: 'font-size:' + (d.t.length <= 35 ? 38 : d.t.length <= 70 ? 30 : d.t.length <= 110 ? 26 : d.t.length <= 170 ? 23 : d.t.length <= 300 ? 20 : 19) + 'px;font-weight:700;line-height:1.7;overflow-y:auto;min-height:0;padding:0 2px'")
    open(f,'w').write(s)
print('ok')
