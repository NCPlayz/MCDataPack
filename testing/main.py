from mcdatapack import DataPack

dp = DataPack(name="MyDataPack", pack_format=5, description="Just A Little Thing")


@dp.mcfunc(event="load")
def hello_world(ctx):
    ctx.execute('say', f'Hello World! This is {dp.name}, version {dp.pack_format}.0!')


@dp.mcfunc(event="tick")
def troll(ctx):
    ctx.execute('kill', '@p')


if __name__ == '__main__':
    dp.build()
