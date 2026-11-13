import re,sys
NEW_CTOR = """this.DAYS = [['ikh', 'sub', 'rad'], ['kur', 'aud', 'hwl'], ['sey', 'hmd', 'hyy'], ['bis', 'lai', 'hsb']]; this.CT = { ikh: [1,3,3,3,3], fal: [1,3,3,3,3], nas: [1,3,3,3,3], kur: [1,1,1,1,1], sey: [1,1,1,1,1], sub: [10,33,33,33,100], ist: [3,10,10,10,33], sal: [3,10,10,10,10], rad: [1,3,3,3,3], aud: [1,3,3,3,3], bis: [1,3,3,3,3], lai: [1,3,10,10,10], hmd: [1,3,3,3,3], hwl: [3,10,10,10,33], hsb: [1,3,3,7,7], hyy: [1,3,3,3,3] }; this.dayKeys = (day) => this.DAYS[(Math.max(1, day) - 1) % 4].concat(['fal', 'nas', 'ist', 'sal']); this.dayList = (lv, day) => this.dayKeys(day).map((k) => [k, this.CT[k][lv - 1]]); this.seenKeys = () => { const out = []; for (let d = 1; d <= Math.min(this.state.day || 1, 4); d++) this.dayKeys(d).forEach((k) => { if (out.indexOf(k) < 0) out.push(k); }); return out; };"""
for f in sys.argv[1:]:
    s=open(f,encoding='utf8').read()
    s,n1=re.subn(r"this\.LVK = \{.*?\}; this\.CNT = \{[^}]*\};",lambda m:NEW_CTOR,s,count=1,flags=re.S)
    s,n2=re.subn(r"this\.LVK\[this\.state\.level\]","this.seenKeys()",s)
    s,n3=re.subn(r"Math\.ceil\(0\.8 \* 4 \* \(this\.CNT\[this\.state\.level\] \+ 24\)\)","Math.ceil(0.8 * [1, 2, 3, 4].reduce((a, d) => a + this.dayList(this.state.level, d).reduce((x, c) => x + c[1], 0) + 24, 0))",s)
    s,n4=re.subn(r"const LV = \{.*?\};\n","const LV = {}; for (let l = 1; l <= 5; l++) LV[l] = this.dayList(l, l === s.level ? s.day : 1);\n",s,count=1,flags=re.S)
    s,n5=re.subn(r"LV\[n\]\.map","this.dayList(n, 1).map",s)
    print(f,n1,n2,n3,n4,n5)
    open(f,'w',encoding='utf8').write(s)
