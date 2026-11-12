import asyncio, os, subprocess, edge_tts
TXT = "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ"
# (name, voice, formant/pitch factor, edge pitch, rate)
V = [("girl_salma_a","ar-EG-SalmaNeural",1.12,"+8Hz","+6%"),
     ("girl_salma_b","ar-EG-SalmaNeural",1.20,"+10Hz","+8%"),
     ("girl_zariyah_a","ar-SA-ZariyahNeural",1.12,"+8Hz","+6%"),
     ("boy_shakir_a","ar-EG-ShakirNeural",1.22,"+6Hz","+6%"),
     ("boy_shakir_b","ar-EG-ShakirNeural",1.32,"+8Hz","+8%"),
     ("boy_hamed_a","ar-SA-HamedNeural",1.25,"+6Hz","+6%")]
async def main():
    os.makedirs("audio/samples", exist_ok=True)
    for n, v, f, p, r in V:
        raw = f"/tmp/{n}.mp3"
        await edge_tts.Communicate(TXT, v, rate=r, pitch=p).save(raw)
        # raise pitch + formants (younger timbre), keep original duration
        subprocess.run(["ffmpeg","-y","-loglevel","error","-i",raw,"-af",
            f"asetrate=24000*{f},aresample=24000,atempo={1/f:.4f},highpass=f=120,loudnorm=I=-16",
            "-ac","1",f"audio/samples/{n}.mp3"],check=True)
        print("ok", n)
asyncio.run(main())
