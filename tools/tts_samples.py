import asyncio, os, edge_tts
TXT = "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ"
V = {"salma_eg":"ar-EG-SalmaNeural","zariyah_sa":"ar-SA-ZariyahNeural","shakir_eg":"ar-EG-ShakirNeural","hamed_sa":"ar-SA-HamedNeural"}
async def main():
    os.makedirs("audio/samples", exist_ok=True)
    for k, v in V.items():
        for rate in ("-15%",):
            try:
                await edge_tts.Communicate(TXT, v, rate=rate).save(f"audio/samples/{k}.mp3")
                print("ok", k)
            except Exception as e:
                print("fail", k, e)
asyncio.run(main())
