"""Cuts audio/full/<who>_all.mp3 into one file per dhikr, at the real silences between adhkar.
Whisper word starts (audio/full_asr.json) are only used to know which silence belongs to which boundary."""
import json, subprocess, array, sys
KEYS = ['rad','aud','sub','bis','ist','sal','sey','lai','hmd','hwl','hsb','hyy']
NW = [11, 8, 3, 16, 4, 6, 36, 17, 7, 6, 12, 6]   # words per dhikr, in order
full = json.load(open('audio/full_asr.json', encoding='utf8'))
out = {}
# بالله/حسبي are spoken with no pause in both recordings; cut points found by probing with ASR
FORCE = {'boy': {10: 66.26}, 'girl': {10: 65.93}}
for who in ('boy', 'girl'):
    src = f'audio/full/{who}_all.mp3'; W = full[f'{who}_all.mp3']['words']
    raw = subprocess.run(['ffmpeg','-loglevel','error','-i',src,'-f','s16le','-ac','1','-ar','16000','-'], capture_output=True).stdout
    a = array.array('h'); a.frombytes(raw); fr = 160
    en = [sum(abs(x) for x in a[i:i+fr]) / fr for i in range(0, len(a) - fr, fr)]
    med = sorted(en)[len(en) // 2]; th = med * 0.04
    sil = []; i = 0
    while i < len(en):
        if en[i] < th:
            j = i
            while j < len(en) and en[j] < th: j += 1
            if j - i >= 20: sil.append((i / 100, j / 100))
            i = j
        else: i += 1
    idx = [sum(NW[:k]) for k in range(len(NW) + 1)]          # first-word index of each dhikr, + the first Quran word
    bounds = [(0.0, 0.0)]
    for k in range(1, len(idx)):
        if k in FORCE[who]: bounds.append((FORCE[who][k], FORCE[who][k])); continue
        s = W[idx[k]]['s']
        cand = [x for x in sil if s - 0.6 <= x[0] <= s + 1.6]
        assert cand, (who, k, s)
        bounds.append(min(cand, key=lambda x: abs(x[1] - (s + 0.45))))
    for k, key in enumerate(KEYS):
        st = max(0.0, bounds[k][1] - min(0.12, (bounds[k][1] - bounds[k][0]) / 2)) if k else 0.0        # 120 ms of silence before the first sound
        en_t = bounds[k + 1][0] + min(0.15, (bounds[k + 1][1] - bounds[k + 1][0]) / 2)                         # 150 ms after the last sound
        subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',f'{st:.2f}','-to',f'{en_t:.2f}','-i',src,
                        '-af',f'afade=t=in:d=0.03,afade=t=out:st={en_t-st-0.05:.2f}:d=0.05','-c:a','libmp3lame','-b:a','96k','-ac','1',f'audio/{who}_{key}.mp3'], check=True)
        out[f'{who}_{key}'] = {'start': round(st, 2), 'end': round(en_t, 2), 'w0': idx[k], 'n': NW[k]}
        print(who, key, f'{st:.2f}-{en_t:.2f}', 'gap', round(bounds[k+1][1]-bounds[k+1][0], 2), 'first', W[idx[k]]['w'], W[idx[k]]['s'])
json.dump(out, open('audio/full_cuts.json', 'w'), indent=1)
