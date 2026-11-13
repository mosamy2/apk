"""Renders a crowd applause: ~70 people, each clapping at their own tempo with jitter; every clap is a
short band-limited noise burst (hand cavity resonance ~1-1.6 kHz + brighter slap ~3 kHz) placed in a small hall (synthetic reverb)."""
import numpy as np, scipy.signal as sg, subprocess, sys
rng = np.random.default_rng(7)
SR = 44100; DUR = 4.6
n = int(SR * DUR)
def clap(fc, q, decay, bright):
    L = int(SR * 0.09); t = np.arange(L) / SR
    noise = rng.standard_normal(L)
    b, a = sg.butter(2, [max(200, fc * 0.6) / (SR / 2), min(9000, fc * 1.5) / (SR / 2)], 'band')
    body = sg.lfilter(b, a, noise) * np.exp(-t / decay)
    b2, a2 = sg.butter(2, [2200 / (SR / 2), 6500 / (SR / 2)], 'band')
    slap = sg.lfilter(b2, a2, rng.standard_normal(L)) * np.exp(-t / (decay * 0.45)) * bright
    thump = np.sin(2 * np.pi * (180 + 60 * rng.random()) * t) * np.exp(-t / 0.012) * 0.25
    x = body + slap + thump
    x[:int(0.0004 * SR)] *= np.linspace(0, 1, int(0.0004 * SR))
    return x / (np.abs(x).max() + 1e-9)
bank = [clap(rng.uniform(900, 1900), 1, rng.uniform(0.007, 0.016), rng.uniform(0.3, 0.9)) for _ in range(40)]
out = np.zeros(n)
people = 70
env_t = np.arange(n) / SR
for p in range(people):
    start = rng.uniform(0, 0.55) ; end = DUR - 0.2 - rng.uniform(0, 1.2)       # people join at slightly different times and stop at different times
    tempo = rng.uniform(2.3, 4.0); t = start; gain = rng.uniform(0.35, 1.0)
    pan = 1.0
    while t < end:
        i = int(t * SR); c = bank[rng.integers(len(bank))] * gain * rng.uniform(0.6, 1.0)
        j = min(n, i + len(c)); out[i:j] += c[:j - i]
        t += (1 / tempo) * rng.uniform(0.82, 1.22)
# overall envelope: quick rise, held, natural fade
env = np.minimum(1, env_t / 0.35) * np.minimum(1, (DUR - env_t) / 1.3)
out *= env
# synthetic hall reverb (RT60 ~ 1.1 s) + early reflections
ir_len = int(SR * 1.4); ti = np.arange(ir_len) / SR
ir = rng.standard_normal(ir_len) * np.exp(-6.9 * ti / 1.1); ir[0] = 0
b, a = sg.butter(1, 5500 / (SR / 2)); ir = sg.lfilter(b, a, ir); ir /= np.abs(ir).max()
wet = sg.fftconvolve(out, ir)[:n]
mix = out * 0.72 + wet * 0.0016 * (np.abs(out).max() / (np.abs(wet).max() + 1e-9)) * 220
mix = sg.lfilter(*sg.butter(1, 120 / (SR / 2), 'high'), mix)
mix /= np.abs(mix).max(); mix *= 0.8
pcm = (mix * 32767).astype('<i2').tobytes()
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 's16le', '-ar', str(SR), '-ac', '1', '-i', '-', '-c:a', 'libmp3lame', '-b:a', '96k', sys.argv[1]], input=pcm, check=True)
f, P = sg.welch(mix, SR, nperseg=2048)
print('centroid Hz', round(float((f * P).sum() / P.sum())), 'rms dBFS', round(20 * np.log10(np.sqrt((mix ** 2).mean())), 1), 'peak', round(float(np.abs(mix).max()), 2))
