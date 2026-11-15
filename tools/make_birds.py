"""Builds audio/fx_birds.mp3: ~14s seamless-looping morning birdsong (synthesised).
Run: python3 tools/make_birds.py  (needs numpy + ffmpeg)"""
import subprocess, wave, numpy as np
rng = np.random.default_rng(7)
SR = 32000; DUR = 14.0; N = int(SR * DUR)
buf = np.zeros(N)

def add(sig, at):
    i = int(at * SR)
    # wrap-around so the loop is seamless
    idx = (np.arange(len(sig)) + i) % N
    np.add.at(buf, idx, sig)

def chirp(f0, f1, dur, vol, vib=0.0, vibf=0.0, curve=1.0):
    t = np.arange(int(SR * dur)) / SR
    x = (t / dur) ** curve
    f = f0 + (f1 - f0) * x
    if vib: f = f * (1 + vib * np.sin(2 * np.pi * vibf * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) + 0.25 * np.sin(2 * ph)
    env = np.sin(np.pi * np.minimum(1, t / dur)) ** 0.8
    return vol * s * env

def tweet(at, base, vol, n=3, gap=0.11, up=True):
    for k in range(n):
        d = rng.uniform(0.07, 0.11)
        a, b = (base, base * 1.35) if up else (base * 1.3, base * 0.9)
        add(chirp(a, b, d, vol * (0.85 + 0.15 * rng.random())), at + k * gap)

def trill(at, base, vol, n=14, rate=0.045):
    for k in range(n):
        add(chirp(base * (1 + 0.08 * (k % 2)), base * 1.18, 0.035, vol * (1 - k / (n * 1.4))), at + k * rate)

def warble(at, base, vol, dur=0.9):
    t = np.arange(int(SR * dur)) / SR
    f = base * (1 + 0.22 * np.sin(2 * np.pi * 7 * t) + 0.12 * np.sin(2 * np.pi * 13 * t + 1))
    ph = 2 * np.pi * np.cumsum(f) / SR
    env = np.sin(np.pi * t / dur) ** 1.2 * (0.7 + 0.3 * np.sin(2 * np.pi * 9 * t))
    add(vol * (np.sin(ph) + 0.2 * np.sin(2 * ph)) * env, at)

# bird A: bright "tswit-tswit-tswit" (sparrow-like), bird B: trills, bird C: far warbler, bird D: descending whistle
for at in [0.4, 3.1, 5.6, 8.9, 11.7]: tweet(at, 3300 + rng.uniform(-200, 200), 0.22, n=int(rng.integers(3, 6)))
for at in [1.7, 7.3, 12.4]: trill(at, 4200, 0.16)
for at in [2.4, 6.4, 10.2]: warble(at, 2600, 0.14)
for at in [4.6, 9.6]:
    add(chirp(3600, 2300, 0.32, 0.2, vib=0.01, vibf=30), at); add(chirp(3600, 2300, 0.32, 0.17), at + 0.48)
for at in [0.9, 5.0, 11.0]: tweet(at, 5200, 0.07, n=2, gap=0.09)   # distant, quiet
# soft airy bed
noise = np.convolve(rng.standard_normal(N), np.ones(60) / 60, mode='same'); buf += 0.01 * noise
# light reverb (circular so loop stays seamless)
rev = np.zeros(N)
for d, g in [(0.06, 0.28), (0.11, 0.2), (0.19, 0.14), (0.29, 0.09)]: rev += g * np.roll(buf, int(d * SR))
buf = buf + rev
buf = buf / np.max(np.abs(buf)) * 0.85
with wave.open('/tmp/fx_birds.wav', 'w') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((buf * 32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', '/tmp/fx_birds.wav', '-ac', '1', '-b:a', '80k', 'audio/fx_birds.mp3'], check=True)
print('ok')
