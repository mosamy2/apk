import asyncio, os, subprocess, edge_tts
TXT = "أَعُوذُ، بِكَلِمَاتِ اللَّهِ التَّامَّاتِ، مِنْ شَرِّ مَا خَلَقَ."
# (name, voice, formant/pitch factor, edge pitch, rate)
V = [("girl_salma_slow","ar-EG-SalmaNeural",1.08,"+2Hz","-14%"),
     ("girl_salma_slower","ar-EG-SalmaNeural",1.12,"+4Hz","-22%"),
     ("girl_zariyah_slow","ar-SA-ZariyahNeural",1.08,"+2Hz","-14%"),
     ("boy_shakir_slow","ar-EG-ShakirNeural",1.12,"+2Hz","-14%"),
     ("boy_shakir_slower","ar-EG-ShakirNeural",1.18,"+4Hz","-22%"),
     ("boy_hamed_slow","ar-SA-HamedNeural",1.14,"+2Hz","-14%")]
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
