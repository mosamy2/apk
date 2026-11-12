"""Aligns each recording in audio/ to its dhikr text and writes word start times to audio/timings.json.
File naming: audio/<who>_<key>.(mp3|m4a|ogg|wav), who in boy|girl|husary, key = dhikr key from src/Main.dc.html (ikh, fal, ...)."""
import json, os, re, sys, difflib
from faster_whisper import WhisperModel

src = open('src/Main.dc.html', encoding='utf8').read()
P = json.loads(re.search(r'const P = (\{.*\});', src).group(1))
OUT = 'audio/timings.json'
timings = json.load(open(OUT, encoding='utf8')) if os.path.exists(OUT) else {}

def norm(w):
    w = re.sub('[ً-ْٰـۖ-ۭ]', '', w)
    w = re.sub('[أإآٱ]', 'ا', w).replace('ى', 'ي').replace('ة', 'ه')
    return re.sub('[^ء-ي]', '', w)

model = None
files = sorted(f for f in os.listdir('audio') if re.match(r'^(boy|girl|husary)_[a-z]+\.(mp3|m4a|ogg|wav)$', f))
todo = [f for f in files if os.path.splitext(f)[0] not in timings or os.environ.get('FORCE')]
for f in todo:
    name = os.path.splitext(f)[0]; key = name.split('_', 1)[1]
    if key not in P: print('skip unknown key', key); continue
    ref = P[key]['t'].split()
    if model is None: model = WhisperModel('large-v3', device='cpu', compute_type='int8')
    segs, info = model.transcribe('audio/' + f, language='ar', word_timestamps=True, beam_size=5, initial_prompt=P[key]['t'], condition_on_previous_text=False)
    asr = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words if w.word.strip()]
    rn = [norm(w) for w in ref]; an = [norm(w[0]) for w in asr]
    sm = difflib.SequenceMatcher(None, rn, an, autojunk=False)
    start = [None] * len(ref); end = [None] * len(ref)
    for a, b, n in sm.get_matching_blocks():
        for k in range(n): start[a + k] = asr[b + k][1]; end[a + k] = asr[b + k][2]
    matched = sum(1 for x in start if x is not None)
    # fill unmatched reference words by interpolation between known neighbours
    dur = info.duration
    known = [i for i, x in enumerate(start) if x is not None]
    if not known: start = [dur * i / len(ref) for i in range(len(ref))]; end = [dur * (i + 1) / len(ref) for i in range(len(ref))]
    else:
        for i in range(len(ref)):
            if start[i] is not None: continue
            lo = max([k for k in known if k < i], default=None); hi = min([k for k in known if k > i], default=None)
            if lo is None: t0, t1, i0, i1 = asr[0][1] if asr else 0, start[hi], -1, hi
            elif hi is None: t0, t1, i0, i1 = end[lo], dur, lo, len(ref)
            else: t0, t1, i0, i1 = end[lo], start[hi], lo, hi
            frac = (i - i0) / (i1 - i0); start[i] = t0 + (t1 - t0) * frac; end[i] = start[i] + (t1 - t0) / (i1 - i0)
    timings[name] = {'duration': round(dur, 2), 'matched': matched, 'total': len(ref), 'asr': ' '.join(w[0] for w in asr),
                     'words': [{'w': ref[i], 's': round(start[i], 2), 'e': round(end[i], 2)} for i in range(len(ref))]}
    print(name, 'matched', matched, '/', len(ref), 'duration', round(dur, 1))
json.dump(timings, open(OUT, 'w', encoding='utf8'), ensure_ascii=False, indent=1)

# plain transcription of unknown recordings dropped in audio/inbox/
IN = 'audio/inbox'; INOUT = 'audio/inbox_asr.json'
if os.path.isdir(IN):
    done = json.load(open(INOUT, encoding='utf8')) if os.path.exists(INOUT) else {}
    for f in sorted(os.listdir(IN)):
        if f in done or not re.search(r'\.(mp3|m4a|ogg|wav)$', f): continue
        if model is None: model = WhisperModel('large-v3', device='cpu', compute_type='int8')
        segs, info = model.transcribe(IN + '/' + f, language='ar', beam_size=5, condition_on_previous_text=False)
        done[f] = {'duration': round(info.duration, 2), 'text': ' '.join(s.text.strip() for s in segs)}
        print(f, done[f])
    json.dump(done, open(INOUT, 'w', encoding='utf8'), ensure_ascii=False, indent=1)

# word-level transcription of long recordings (several adhkar in one file) in audio/full/
FU = 'audio/full'; FUOUT = 'audio/full_asr.json'
if os.path.isdir(FU):
    done = json.load(open(FUOUT, encoding='utf8')) if os.path.exists(FUOUT) else {}
    for f in sorted(os.listdir(FU)):
        if f in done or not re.search(r'\.(mp3|m4a|ogg|wav)$', f): continue
        if model is None: model = WhisperModel('large-v3', device='cpu', compute_type='int8')
        segs, info = model.transcribe(FU + '/' + f, language='ar', word_timestamps=True, beam_size=5, condition_on_previous_text=False)
        done[f] = {'duration': round(info.duration, 2), 'words': [{'w': w.word.strip(), 's': round(w.start, 2), 'e': round(w.end, 2)} for s in segs for w in s.words if w.word.strip()]}
        print(f, len(done[f]['words']), 'words')
    json.dump(done, open(FUOUT, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
