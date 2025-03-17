
import asyncio

testinfo = 0

async def simulatepopup():
    print("popup started")
    await asyncio.sleep(2)
    print("popup ended")

def simulatelogic():
    global testinfo
    if testinfo == 0:
        print("logic started")
        asyncio.run(simulatepopup())
        print("back to logic")
    else:
        print("logic not needed")

simulatelogic()
