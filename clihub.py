from sys    import argv, stderr, stdout
from json   import load, dump
from os     import path, system 

class CliHub:
    def __init__(self) -> None:
        self.internal_cli = {}
        self.internal_bindings = {}

        if not path.exists('clihub.json'):
            with open('clihub.json','w') as f:
                dump(self.internal_cli, f)

        if not path.exists('ext_bindings.json'):
            with open('ext_bindings.json','w') as f:
                dump(self.internal_bindings, f)

    def __get_ext(self, name:str) -> str:
        ext: str = ""
        if '.' in name:
            ext = name.split('.')[1].lower()
        else:
            ext = 'exe'
        if not ext in self.internal_bindings:
                stderr.write(f"{name}.{ext} doesn't have a binding to a runtime")
                exit(1)
        else:
            return self.internal_bindings[ext]

    def __new_cli(self, name:str, path:str) -> None:
        self.internal_cli[name] = path
        stdout.write(f"Succesfully registered {path} as {name}.")

    def __del_cli(self, name:str) -> None:
        del self.internal_cli[name]
        stdout.write(f"Succesfully deleted {name}.")

    def __run_cli(self, name:str, args:list) -> None:
        if name not in self.internal_cli:
            stderr.write(f'run: {name} isn\'t registered.')
            exit(1)
        else:
            name = self.internal_cli[name]
            ext: str = self.__get_ext(name)
            cmd: str = f"{ext}{name} "
            all = [arg for arg in args]; all = ' '.join(all)
            system(cmd+all)

    def __save(self) -> None:
        with open('clihub.json', 'w') as f:
            dump(self.internal_cli, f)

    def __load(self) -> None:
        with open('clihub.json', 'r') as f:
            self.internal_cli = load(f)
        with open('ext_bindings.json', 'r') as f:
            self.internal_bindings = load(f)

    def __help(self) -> None:
        stdout.write(
            f"""
            clihub.py:
                -h | --help:                shows this message.
                add (app-name, app-path):   adds (app-path) with (app-name) as reference.
                del (app-name):             deletes (app-name) reference.
                run (app-name, ...):        executes (app-name) with (...) as arguments.
                    Extension-Support:
                        See 'ext_bindings.json'.
            """
        )

    def run(self) -> None:
        self.__load()
        if not len(argv) >= 2:
            stderr.write(f'Not enough arguments.')
            exit(1)
        else:
            action = argv[1]
            match action:
                case 'run':
                    if not len(argv) > 2:
                        stderr.write("run: Missing argument 'app-name'")
                        exit(1)
                    else:
                        self.__run_cli(argv[2], argv[3:])
                case 'add':
                    if not len(argv) >= 4:
                        stderr.write("add: Missing arguments 'app-name', 'app-path'")
                        exit(1)
                    else:
                        self.__new_cli(argv[2],argv[3])
                case 'del':
                    if not len(argv) >= 3:
                        stderr.write("del: Missing argument 'app-name'")
                        exit(1)
                    else:
                        self.__del_cli(argv[2])
                case '-h':
                    self.__help()
                case '--help':
                    self.__help()
                case _:
                    stderr.write(f"Unrecognized action: {argv[1]}")
                    exit(1)
        self.__save()

if __name__ == '__main__':
    hub = CliHub()
    hub.run()