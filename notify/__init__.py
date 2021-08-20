from .webPagesParse import inform, informburo, kzinform, nur, time, total, zakon, lada, tengrinews, inaktau, azattyqruhy, azattyq


async def main(new_keyword=None):
    await inform(new_keyword)
    await informburo(new_keyword)
    await kzinform(new_keyword)
    await nur(new_keyword)
    await time(new_keyword)
    await total(new_keyword)
    await zakon(new_keyword)
    await azattyq(new_keyword)
    await azattyqruhy(new_keyword)
    await inaktau(new_keyword)
    await tengrinews(new_keyword)
    await lada(new_keyword)