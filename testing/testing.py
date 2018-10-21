from mcdatapack import DataPack

dp = DataPack(name="FirstDataPack", pack_format=2, description="I hope you like it!")


@dp.mcfunc(event='tick')
def teleport(ctx):
    ctx.execute('give', '@p', 'minecraft:tnt', '64')


@dp.mcfunc(event='load')
def huh(ctx):
    ctx.execute('say', 'Hi! This is a cool thing I made!')


if __name__ == '__main__':
    dp.build()
