import sys, re
KEYS = """@keyframes drift{0%{transform:translateX(-140px)}100%{transform:translateX(540px)}}
@keyframes twinkle{0%,100%{opacity:.25;transform:scale(.8)}50%{opacity:1;transform:scale(1.2)}}
@keyframes floaty{0%,100%{transform:translateY(0) rotate(-4deg)}50%{transform:translateY(-16px) rotate(4deg)}}
@keyframes sway{0%,100%{transform:rotate(-3deg)}50%{transform:rotate(3deg)}}
@keyframes rise{0%{transform:translateY(0)}100%{transform:translateY(-980px)}}
@keyframes clap{0%,100%{transform:scale(1) rotate(-10deg)}50%{transform:scale(1.4) rotate(10deg)}}
@keyframes bird{0%{transform:translate(-50px,0)}50%{transform:translate(200px,-26px)}100%{transform:translate(470px,0)}}
@keyframes glow{0%,100%{opacity:.55}50%{opacity:1}}
"""
CLOUD = lambda top, w, dur, delay, op: f'<div style="position:absolute;top:{top}px;left:0;width:{w}px;height:{int(w*0.42)}px;opacity:{op};animation:drift {dur}s linear {delay}s infinite"><svg width="{w}" height="{int(w*0.42)}" viewBox="0 0 120 50" aria-hidden="true"><ellipse cx="60" cy="34" rx="52" ry="14" fill="#fff"/><circle cx="38" cy="26" r="16" fill="#fff"/><circle cx="64" cy="20" r="20" fill="#fff"/><circle cx="88" cy="28" r="14" fill="#fff"/></svg></div>'
SCENE = ('<div aria-hidden="true" style="position:absolute;left:0;top:0;width:390px;height:844px;z-index:-1;overflow:hidden;pointer-events:none"><div style="{{skyStyle}}"></div>'
 # sun (morning)
 '<sc-if value="{{sceneAm}}" hint-placeholder-val="{{ true }}"><div style="position:absolute;left:286px;top:92px;width:90px;height:90px"><div style="position:absolute;left:-35px;top:-35px;width:160px;height:160px;border-radius:80px;background:repeating-conic-gradient(rgba(255,214,90,.55) 0 8deg,rgba(255,214,90,0) 8deg 24deg);animation:spin 40s linear infinite"></div><div style="position:absolute;left:0;top:0;width:90px;height:90px;border-radius:45px;background:radial-gradient(circle at 35% 35%,#FFF3A8,#FFC93C 70%,#FFB020);box-shadow:0 0 30px 10px rgba(255,214,90,.5)"></div><svg width="90" height="90" viewBox="0 0 90 90" style="position:absolute;left:0;top:0" aria-hidden="true"><circle cx="32" cy="42" r="4" fill="#7A4A00"/><circle cx="58" cy="42" r="4" fill="#7A4A00"/><path d="M33 56q12 11 24 0" fill="none" stroke="#7A4A00" stroke-width="4" stroke-linecap="round"/><circle cx="24" cy="52" r="5" fill="#FF8FB1" opacity=".6"/><circle cx="66" cy="52" r="5" fill="#FF8FB1" opacity=".6"/></svg></div>'
 '<div style="position:absolute;left:0;top:250px;animation:bird 16s linear 2s infinite"><svg width="30" height="14" viewBox="0 0 30 14" aria-hidden="true"><path d="M2 10q6-10 13 0q7-10 13 0" fill="none" stroke="#5A6AA8" stroke-width="2.4" stroke-linecap="round"/></svg></div>'
 '<div style="position:absolute;left:0;top:300px;animation:bird 22s linear 9s infinite"><svg width="22" height="10" viewBox="0 0 30 14" aria-hidden="true"><path d="M2 10q6-10 13 0q7-10 13 0" fill="none" stroke="#5A6AA8" stroke-width="2.6" stroke-linecap="round"/></svg></div></sc-if>'
 # moon and stars (evening)
 '<sc-if value="{{sceneNight}}" hint-placeholder-val="{{ false }}"><div style="position:absolute;left:290px;top:92px;width:84px;height:84px;filter:drop-shadow(0 0 14px rgba(255,236,150,.9))"><svg width="84" height="84" viewBox="0 0 84 84" aria-hidden="true"><path d="M58 8a34 34 0 1 0 18 52a28 28 0 1 1-18-52z" fill="#FFE98A"/><circle cx="36" cy="40" r="3" fill="#E8C95A"/><circle cx="46" cy="58" r="4" fill="#E8C95A"/></svg></div>'
 '<sc-for list="{{skyStars}}" as="z" hint-placeholder-count="12"><i style="{{z.style}}"></i></sc-for></sc-if>'
 + CLOUD(120, 120, 60, -20, 0.95) + CLOUD(200, 90, 80, -50, 0.8) + CLOUD(330, 110, 95, -10, 0.7) + CLOUD(60, 80, 70, -35, 0.85) +
 # hills + village
 '<svg width="390" height="300" viewBox="0 0 390 300" style="position:absolute;left:0;top:544px" aria-hidden="true">'
 '<path d="M0 90 C 70 30 150 30 220 80 C 290 120 340 40 390 70 L390 300 L0 300z" fill="#A8E6A1"/>'
 '<g transform="translate(298 8)"><rect x="12" y="44" width="52" height="40" rx="3" fill="#B7A8F0"/><path d="M8 46a30 30 0 0 1 60 0z" fill="#9A89E6"/><rect x="36" y="-4" width="4" height="12" rx="2" fill="#E8C95A"/><circle cx="38" cy="10" r="4" fill="#E8C95A"/><rect x="72" y="20" width="9" height="64" rx="3" fill="#B7A8F0"/><path d="M70 22a6.5 6.5 0 0 1 13 0z" fill="#9A89E6"/><rect x="76" y="8" width="2" height="10" fill="#E8C95A"/><rect x="28" y="56" width="10" height="16" rx="5" fill="#FFE08A" style="animation:glow 3s ease-in-out infinite"/><rect x="42" y="56" width="10" height="16" rx="5" fill="#FFE08A" style="animation:glow 3s ease-in-out 1s infinite"/></g>'
 '<path d="M0 150 C 90 100 180 120 260 150 C 320 172 360 150 390 140 L390 300 L0 300z" fill="#7DD08B"/>'
 '<g style="transform-origin:48px 150px;animation:sway 4s ease-in-out infinite"><rect x="44" y="118" width="8" height="32" rx="3" fill="#8A5A3A"/><circle cx="48" cy="106" r="22" fill="#4FB872"/><circle cx="36" cy="116" r="14" fill="#5CC67E"/><circle cx="60" cy="116" r="14" fill="#5CC67E"/></g>'
 '<g style="transform-origin:352px 168px;animation:sway 5s ease-in-out .8s infinite"><rect x="348" y="140" width="8" height="30" rx="3" fill="#8A5A3A"/><circle cx="352" cy="128" r="20" fill="#4FB872"/><circle cx="341" cy="138" r="13" fill="#5CC67E"/></g>'
 '<path d="M0 214 C 110 180 230 200 390 186 L390 300 L0 300z" fill="#5FC27A"/>'
 '<g><circle cx="30" cy="224" r="5" fill="#FF6FA5"/><circle cx="30" cy="224" r="2" fill="#FFE08A"/><circle cx="80" cy="238" r="5" fill="#FFC93C"/><circle cx="80" cy="238" r="2" fill="#fff"/><circle cx="150" cy="226" r="5" fill="#fff"/><circle cx="150" cy="226" r="2" fill="#FFC93C"/><circle cx="262" cy="222" r="5" fill="#FF8A3D"/><circle cx="262" cy="222" r="2" fill="#fff"/><circle cx="330" cy="236" r="5" fill="#FF6FA5"/><circle cx="330" cy="236" r="2" fill="#FFE08A"/></g></svg>'
 '<div style="position:absolute;left:8px;top:430px;font-size:34px;animation:floaty 5s ease-in-out infinite">🎈</div>'
 '<div style="position:absolute;left:340px;top:520px;font-size:28px;animation:floaty 6s ease-in-out 1.2s infinite">🦋</div>'
 '</div>')
WIRD = ('<sc-if value="{{isWird}}" hint-placeholder-val="{{ false }}"><div style="position:absolute;left:0;right:0;top:0;bottom:0;z-index:10;background:linear-gradient(180deg,#FFF3C4 0%,#FFD6E8 52%,#CFE9FF 100%);display:flex;flex-direction:column;align-items:center;padding:60px 20px 0;text-align:center;overflow:hidden">'
 '<div style="position:absolute;left:-155px;top:-40px;width:700px;height:700px;border-radius:350px;background:repeating-conic-gradient(rgba(255,255,255,.7) 0 9deg,rgba(255,255,255,0) 9deg 22deg);animation:spin 30s linear infinite;pointer-events:none"></div>'
 '<div style="position:absolute;left:0;right:0;top:0;height:844px;pointer-events:none"><sc-for list="{{confetti}}" as="c" hint-placeholder-count="3"><i style="{{c.style}}"></i></sc-for></div>'
 '<sc-for list="{{balloons}}" as="b" hint-placeholder-count="6"><div style="{{b.style}}">{{b.e}}</div></sc-for>'
 '<div style="position:relative;display:flex;align-items:center;justify-content:center;gap:6px;margin-top:6px"><div style="font-size:46px;animation:clap .7s ease-in-out infinite">👏</div>'
 '<svg width="190" height="200" viewBox="0 0 190 200" role="img" aria-label="ميدالية الورد" style="animation:zoomIn .7s ease-out"><path d="M58 100 L38 186 L66 170 L84 196 L100 108z" fill="#FF6FA5"/><path d="M132 100 L152 186 L124 170 L106 196 L90 108z" fill="#7B5CFF"/><circle cx="95" cy="82" r="68" fill="#E39A00"/><circle cx="95" cy="82" r="60" fill="#FFC93C"/><circle cx="95" cy="82" r="48" fill="#FFE08A" stroke="#E39A00" stroke-width="3"/><path d="M95 44l11 24 26 3-19 18 5 26-23-13-23 13 5-26-19-18 26-3z" fill="#FF8A3D" stroke="#E39A00" stroke-width="3" stroke-linejoin="round"/><circle cx="52" cy="40" r="5" fill="#fff" opacity=".8"/><circle cx="140" cy="132" r="4" fill="#fff" opacity=".7"/></svg>'
 '<div style="font-size:46px;animation:clap .7s ease-in-out .35s infinite">👏</div></div>'
 '<div style="position:relative;font-size:30px;font-weight:700;margin-top:6px;line-height:1.3;animation:zoomIn .5s .15s ease-out both">{{wTitle}}</div>'
 '<div style="position:relative;font-size:16px;font-weight:600;margin-top:8px;line-height:1.6;color:#44507F">{{wSub}}</div>'
 '<div style="position:relative;display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:16px"><sc-for list="{{wPills}}" as="p" hint-placeholder-count="7"><span style="{{p.style}}">✓ {{p.name}}</span></sc-for></div>'
 '<div style="position:relative;display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:14px"><sc-for list="{{wRewards}}" as="r" hint-placeholder-count="3"><span style="height:38px;padding:0 14px;border-radius:19px;background:#fff;border:3px solid #FFC93C;display:flex;align-items:center;gap:6px;font-size:14px;font-weight:700;animation:zoomIn .6s ease-out both">{{r}}</span></sc-for></div>'
 '<div style="position:relative;margin-top:16px;width:100%;box-sizing:border-box;padding:14px 16px;border-radius:22px;background:rgba(255,255,255,.88);font-size:15px;font-weight:700;line-height:1.7">{{wQuote}}</div>'
 '<button onClick="{{wGo}}" style="position:absolute;left:20px;right:20px;bottom:44px;height:60px;border-radius:30px;border:0;background:#20B2A6;box-shadow:0 5px 0 #138A80;color:#1F2A5A;font-size:19px;font-weight:700;animation:pulse .8s ease-in-out infinite">{{wBtn}}</button>'
 '</div></sc-if>\n')
PAL = "['#FF8FB1','#FFC93C','#6FD3A8','#7BB8FF','#FF8A3D','#B28CFF','#FF6F6F']"
VALS = ("isWird: s.view === 'wird', sceneAm: am, sceneNight: !am, "
 "skyStyle: 'position:absolute;left:0;top:0;width:390px;height:844px;background:' + (am ? 'linear-gradient(180deg,#8FD3FF 0%,#C6ECFF 42%,#FFF1C9 78%,#DDF5C8 100%)' : 'linear-gradient(180deg,#B9A8FF 0%,#F0B6DD 46%,#FFDDB0 80%,#D9EBC0 100%)'), "
 "skyStars: Array.from({ length: 16 }, (_, i) => ({ style: 'position:absolute;left:' + ((i * 53 + 17) % 360) + 'px;top:' + (70 + (i * 37) % 260) + 'px;width:' + (4 + (i % 3) * 2) + 'px;height:' + (4 + (i % 3) * 2) + 'px;border-radius:50%;background:#fff;box-shadow:0 0 8px 2px rgba(255,255,255,.9);animation:twinkle ' + (1.6 + (i % 4) * 0.5) + 's ease-in-out ' + ((i % 5) * 0.3) + 's infinite' })), "
 "balloons: ['🎈','🎈','🎀','🎈','⭐','🎈'].map((e, i) => ({ e, style: 'position:absolute;left:' + (20 + i * 62) + 'px;top:860px;font-size:' + (30 + (i % 3) * 8) + 'px;animation:rise ' + (6 + (i % 3) * 1.5) + 's linear ' + (i * 0.7) + 's infinite;pointer-events:none' })), "
 "wTitle: t('ما شاء الله! خلصتَ ورد ', 'ما شاء الله! خلصتِ ورد ') + (am ? 'الصباح' : 'المساء') + '!', "
 "wSub: t('أنت بطل الأذكار يا ', 'أنتِ بطلة الأذكار يا ') + kidNm + '، ' + t('ركبتَ القطار ووصلتَ للهدية', 'ركبتِ القطار ووصلتِ للهدية'), "
 "wPills: LV[s.level].map((c, i) => ({ name: P[c[0]].s, style: 'height:32px;padding:0 12px;border-radius:16px;font-size:13px;font-weight:700;display:flex;align-items:center;color:#1F2A5A;border:2px solid #fff;background:' + " + PAL + "[i % 7] + ';animation:zoomIn .5s ease-out ' + (i * 0.08) + 's both' })), "
 "wRewards: ['⭐ ' + ar(10) + ' نجوم هدية', '🏅 شارة ورد ' + (am ? 'الصباح' : 'المساء'), '📅 اليوم ' + ar(Math.min(s.day, 4)) + ' من ٤'], "
 "wQuote: ['ألا بذكر الله تطمئن القلوب 💛', 'الله يحبك ويفرح بك، واصل يا بطل!', 'أحب الأعمال إلى الله أدومها وإن قلّ 🌟', 'كل ذكر تقوله يقرّبك من الله 🤍', 'غدًا قطار جديد ومحطات جديدة بإذن الله 🚂'][(s.day + (am ? 0 : 2)) % 5], "
 "wBtn: am ? t('يا سلام! أكمل', 'يا سلام! أكملي') : 'إلى الخريطة', "
 "wGo: () => { this.clearAll(); this.setState({ view: am ? 'levelend' : 'map' }); }, ")
for f in sys.argv[1:]:
    s = open(f, encoding='utf8').read()
    # keyframes
    a = "@keyframes trainIn{0%{transform:scale(.4);opacity:0}100%{transform:scale(1);opacity:1}}\n"; assert a in s; s = s.replace(a, a + KEYS, 1)
    # root: stacking context + scene
    r = "background:#DFF3FF;font-family:'Noto Sans Arabic',Arial,sans-serif;color:#1F2A5A;position:relative;overflow:hidden\">\n"
    assert r in s
    s = s.replace(r, r.replace("position:relative;", "position:relative;isolation:isolate;") + SCENE + "\n", 1)
    # wird view before level end
    b = '<sc-if value="{{isLevelEnd}}"'; assert b in s; s = s.replace(b, WIRD + b, 1)
    # vals
    c = "isPlay: s.view === 'play', isCheer: s.view === 'cheer',"; assert c in s; s = s.replace(c, c + " " + VALS, 1)
    # station colours
    d = "const col = st === 'done' ? 'background:#FFC93C;border:4px solid #E39A00;color:#1F2A5A'"; assert d in s
    s = s.replace(d, "const col = st === 'done' ? 'background:' + " + PAL + "[(k - 1) % 7] + ';border:4px solid #fff;box-shadow:0 3px 0 rgba(31,42,90,.25);color:#1F2A5A'", 1)
    # finish -> celebration
    e = "if (this.state.tab === 'am') this.setState({ view: 'levelend' }); else this.say(this.g === 'girl' ? 'ما شاء الله! أتممتِ أذكار المساء' : 'ما شاء الله! أتممتَ أذكار المساء', ''); } }, 3200);"
    assert e in s
    s = s.replace(e, "this.arp([523, 659, 784, 1047, 1319, 1568], 0.11, 'triangle', 0.2); this.setState({ view: 'wird' }); } }, 3200);", 1)
    f2 = "tC: () => open ? (am ? this.setState({ view: 'levelend' }) : this.say(t('ما شاء الله! أتممتَ أذكار المساء', 'ما شاء الله! أتممتِ أذكار المساء'), ''))"
    assert f2 in s
    s = s.replace(f2, "tC: () => open ? this.setState({ view: 'wird' })", 1)
    open(f, 'w', encoding='utf8').write(s)
    print('patched', f)
