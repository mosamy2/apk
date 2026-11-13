"""Builds audio/fx_soft.mp3: a calm 'soft' reminder chime (two gentle bell phrases).
Run: python3 tools/make_soft.py  (needs numpy + ffmpeg)"""
import subprocess, wave, numpy as np

SR = 44100
OUT_WAV = '/tmp/fx_soft.wav'
OUT = 'audio/fx_soft.mp3'


def bell(f, dur, vol):
    t = np.arange(int(SR * dur)) / SR
    # soft bell: fundamental + gentle inharmonic partials, slow decay, soft attack
    parts = [(1.0, 1.0, 2.2), (2.0, 0.28, 3.4), (3.01, 0.10, 5.0), (4.2, 0.05, 7.0)]
    s = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-d * t) for m, a, d in parts)
    att = np.minimum(1, t / 0.012)
    return vol * s * att


def place(buf, sig, at):
    i = int(at * SR)
    buf[i:i + len(sig)] += sig[: len(buf) - i]


total = 4.6
buf = np.zeros(int(SR * total))
# phrase 1: G5 - C6 - E6 (rising, calm) ; phrase 2: E6 - G6 (answer)
for at, f in [(0.00, 784.0), (0.32, 1046.5), (0.64, 1318.5)]:
    place(buf, bell(f, 2.4, 0.32), at)
for at, f in [(1.80, 1318.5), (2.12, 1568.0)]:
    place(buf, bell(f, 2.4, 0.26), at)
# light room reverb (few short echoes)
rev = np.zeros_like(buf)
for dly, g in [(0.045, 0.22), (0.083, 0.15), (0.131, 0.10), (0.197, 0.06)]:
    n = int(dly * SR)
    rev[n:] += g * buf[:-n]
buf = buf + rev
fade = int(0.4 * SR)
buf[-fade:] *= np.linspace(1, 0, fade)
buf = buf / np.max(np.abs(buf)) * 0.8
with wave.open(OUT_WAV, 'w') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((buf * 32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', OUT_WAV, '-ac', '1', '-ar', '44100', '-b:a', '96k', OUT], check=True)
print('wrote', OUT)
