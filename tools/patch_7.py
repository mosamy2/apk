import re
XS=[105,238,112,231,119,225,112,210]
YS=[510,444,377,311,245,178,112,46]
C='['+','.join(f'[{x},{y}]' for x,y in zip(XS,YS))+']'
AR='١٢٣٤٥٦٧'
for f in ['src/Main.dc.html','src/MainGirl.dc.html']:
    s=open(f).read()
    def rep(a,b,cnt=1):
        global s
        assert s.count(a)==cnt,(f,a[:80],s.count(a))
        s=s.replace(a,b)
    rep("this.C = [[105,505],[238,410],[112,310],[231,210],[119,112],[210,46]];","this.C = "+C+";")
    rep("const C = [[105,505],[238,410],[112,310],[231,210],[119,112],[210,46]];","const C = this.C;")
    for lv,add in {1:"'ist', 'sal'",2:"'ist', 'sal'",3:"'ist', 'sal'",4:"'ist', 'sal'",5:"'ist', 'sal'"}.items():
        m=re.search(rf"{lv}: \[([^\]]*)\]",s[s.index('this.LVK'):]); assert m
    i=s.index('this.LVK = {'); j=s.index('};',i)+2
    blk=s[i:j]; blk2=re.sub(r"(\d): \[([^\]]*)\]",lambda m:f"{m.group(1)}: [{m.group(2)}, 'ist', 'sal']",blk); s=s[:i]+blk2+s[j:]
    rep("this.CNT = { 1: 14, 2: 45, 3: 43, 4: 41, 5: 108 };","this.CNT = { 1: 20, 2: 65, 3: 63, 4: 61, 5: 151 };")
    rep('const P = {"rad":','const P = {"ist": {"t": "أَسْتَغْفِرُ اللَّهَ وَأَتُوبُ إِلَيْهِ", "h": "نطلب من الله أن يغفر لنا", "f": 28, "s": "أستغفر الله"}, "sal": {"t": "اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ", "h": "نحب نبينا محمدًا ونصلّي عليه", "f": 26, "s": "الصلاة على النبي"}, "rad":')
    rep('["ikh", 1]], "2":','["ikh", 1], ["ist", 3], ["sal", 3]], "2":')
    rep('["rad", 3]], "3":','["rad", 3], ["ist", 10], ["sal", 10]], "3":')
    rep('["sub", 33]], "4":','["sub", 33], ["ist", 10], ["sal", 10]], "4":')
    rep('["sub", 33]], "5":','["sub", 33], ["ist", 10], ["sal", 10]], "5":')
    rep('["sub", 100]]};','["sub", 100], ["ist", 33], ["sal", 10]]};')
    rep("(this.CNT[this.state.level] + 20)), stNeed = 16;","(this.CNT[this.state.level] + 24)), stNeed = 23;")
    # station-count literals
    rep("Math.min(5, p + 1)","Math.min(7, p + 1)")
    s=s.replace("np >= 5","np >= 7").replace("np < 5","np < 7")
    rep("LV[s.level][Math.min(s.progress, 4)]","LV[s.level][Math.min(s.progress, 6)]")
    rep("for (let k = 1; k <= 5; k++) {\nconst st = k <= dp","for (let k = 1; k <= 7; k++) {\nconst st = k <= dp")
    rep("const sz = st === 'cur' ? 88 : 64,","const sz = st === 'cur' ? 76 : 56,")
    rep("const mi = Math.min(s.progress, 5), mc = C[mi];","const mi = Math.min(s.progress, 7), mc = C[mi];")
    rep("const open = s.progress >= 5;","const open = s.progress >= 7;")
    rep("if (s.progress < 5 && ['map', 'play']","if (s.progress < 7 && ['map', 'play']")
    rep("progressTxt: ar(Math.min(s.progress, 5)) + ' من ٥',","progressTxt: ar(Math.min(s.progress, 7)) + ' من ٧',")
    rep("backLabel: s.progress >= 4 ?","backLabel: s.progress >= 6 ?")
    rep("bars: [0,1,2,3,4].map(","bars: [0,1,2,3,4,5,6].map(")
    rep("ar(Math.min(s.progress, 4) + 1) + ' من ٥',","ar(Math.min(s.progress, 6) + 1) + ' من ٧',")
    rep("cheerTitle: s.progress >= 4 ?","cheerTitle: s.progress >= 6 ?")
    rep("cheerSub: s.progress >= 4 ?","cheerSub: s.progress >= 6 ?")
    rep("db.v === 1","db.v === 2"); rep("JSON.stringify({ v: 1, t: Date.now()","JSON.stringify({ v: 2, t: Date.now()")
    # template: path + stations
    segs=''
    for k in range(7):
        x0,y0=XS[k],YS[k]; x1,y1=XS[k+1],YS[k+1]; ym=(y0+y1)/2
        d=f"M{x0} {y0} C {x0} {ym} {x1} {ym} {x1} {y1}"
        segs+=f'<path d="{d}" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round" stroke-dasharray="2 22"/><sc-if value="{{{{g{k+1}}}}}" hint-placeholder-val="{{{{ false }}}}"><path d="{d}" fill="none" stroke="#FFC93C" stroke-width="14" stroke-linecap="round" stroke-dasharray="2 22"/></sc-if>'
    L=s.split('\n')
    i=[k for k,l in enumerate(L) if l.startswith('<svg width="350" height="560"')][0]
    L[i]='<svg width="350" height="560" viewBox="0 0 350 560" style="position:absolute;left:0;top:0" aria-hidden="true">'+segs+'</svg>'
    s='\n'.join(L)
    a=s.index('<button aria-label="المحطة 1"'); b=s.index('<div style="{{l5}}">{{n5}}</div>')+len('<div style="{{l5}}">{{n5}}</div>')
    chk='<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#1F2A5A" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5 9-10"/></svg>'
    st='\n'.join(f'<button aria-label="المحطة {k}" onClick="{{{{t{k}}}}}" style="{{{{s{k}}}}}"><sc-if value="{{{{d{k}}}}}" hint-placeholder-val="{{{{ false }}}}">{chk}</sc-if><sc-if value="{{{{u{k}}}}}" hint-placeholder-val="{{{{ true }}}}">{AR[k-1]}</sc-if></button>\n<div style="{{{{l{k}}}}}">{{{{n{k}}}}}</div>' for k in range(1,8))
    s=s[:a]+st+s[b:]
    open(f,'w').write(s)
print('ok')
