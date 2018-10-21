# MCDataPack
Minecraft Datapack creator in Python. Right now it only supports functions, but more is being added!

# Example
```python
from mcdatapack import DataPack

dp = DataPack(name='GoldGalore', pack_format=1, description='Spams you with gold forever!')


@dp.mcfunc(event='tick')
def gold_spam(ctx):
    ctx.execute('give', '@p', 'minecraft:gold_block')


if __name__ == '__main__':
    dp.build('./datapack/')
```

# Links
- Minecraft Datapack Documentation: https://minecraft.gamepedia.com/Data_pack
- Minecraft Datapack Tutorial: https://minecraft.gamepedia.com/Tutorials/Creating_a_data_pack