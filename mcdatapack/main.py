import os
import json


class DataPack:
    """
    A DataPack instance is a instance of a Minecraft datapack. It can be made from scratch, or from folder.

    :param name: The name used for your datapack. It will also be used for the namespace. Defaults to 'DataPackPy'.
    :param pack_format: The version of your datapack. Defaults to 1.
    :param description: The description of your datapack. Defaults to 'Data Pack made in Python'.
    """
    def __init__(self, name: str="DataPackPy", pack_format: int=1, *, description: str="Data Pack made in Python"):
        self.name = name
        self.description = description
        self.pack_format = pack_format
        self.functions = {}

    def build(self, build_path: str=""):
        """
        [Work In Progress]
        Builds your datapack. This is currently very clunky, and is being optimised.
        This essentially uses the standards advised by Minecraft, so that you can use the datapack properly in-game.

        :param build_path: The path where you want the datapack to build in. It goes to `./datapack/{name}` by default.
        """
        if not os.path.exists(build_path):
            build_path = f'.\\data_packs\\{self.name.lower()}'
            os.makedirs(build_path, exist_ok=True)

        with open(f'{build_path}\\pack.mcmeta', 'w') as f:
            s = {'pack': {'pack_format': self.pack_format, 'description': self.description}}
            json.dump(s, f, indent=4)

        data_path = os.path.join(build_path, 'data')

        os.makedirs(os.path.join(data_path, f'{self.name.lower()}'), exist_ok=True)

        self.walk_mcfunctions()
        func_path = os.path.join(data_path, f'{self.name.lower()}', 'functions')
        os.makedirs(func_path, exist_ok=True)

        for i in self.functions.keys():
            with open(os.path.join(func_path, f'{i}.mcfunction'), 'w') as f:
                f.write(self.functions[i]['code'])

            function_tag_path = os.path.join(data_path, 'minecraft', 'tags', 'functions')
            if self.functions[i]['event'] in ['load', 'tick']:
                if not os.path.exists(function_tag_path):
                    os.makedirs(function_tag_path, exist_ok=True)

                with open(os.path.join(function_tag_path, f'{self.functions[i]["event"]}.json'), 'w') as f:
                    s = {"values": [f"{self.name.lower()}:{i}",]}
                    json.dump(s, f, indent=4)

    def mcfunc(self, event):
        """
        A decorator to signify that the function below it is a Minecraft Function

        :param event: A trigger event for the function. It can be 'tick' or 'load'.
        """
        def wrapper(func):
            self.functions[func.__name__] = {'function': func, 'event': event}
            return func
        return wrapper

    def walk_mcfunctions(self):
        for i in self.functions.keys():
            result = ""
            ctx = Context()
            self.functions[i]['function'](ctx)

            for c in ctx.commands_executed:
                result += c + "\n"

            self.functions[i]['code'] = result

    @classmethod
    def from_folder(cls, path: str):
        """
        [Work In Progress]
        Class Method to get a `DataPack` instance from a specific Folder.
        There are currently unresolved issues with it.

        :param path: The path of the folder.
        :return: An instance of `DataPack`.
        """
        if not os.path.exists(path):
            raise FileNotFoundError('There is no folder at {}'.format(path))

        with open(path + '/pack.mcmeta', 'r') as f:
            d = json.load(f)
            description = d['description'] if d['description'] else "Data Pack made in Python"
            pack_format = d['pack_format'] if d['pack_format'] else 1

        return cls(os.path.dirname(path), pack_format, description=description)


class Context:
    def __init__(self):
        self.commands_executed = []

    def execute(self, command: str, *args):
        """
        Executes a command within Minecraft.

        :param command: The command name. (EG. `say`)
        :param args: The command arguments (EG. `@p ~ ~ ~`)
        :return: The whole command put together (EG. `give @p minecraft:tnt 64`)
        """
        self.commands_executed.append(f'{command} {" ".join(args)}')
        return
