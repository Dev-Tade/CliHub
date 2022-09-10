from sys import argv, stderr, stdout
from json import load, dump
from os import path, system 

class CliHub:
    def __init__(self) -> None:
        self.internal = {}
        self.support = ['native','python']
        if not path.exists('clihub.json'):
            with open('clihub.json','w') as f:
                dump(self.internal, f)

    def __get_type(self, name:str):
        if self.internal[name].endswith('.py'):
            return f'python {name}.py'
        else:
            return f'./{name}'

    def __new_cli(self, name:str, path:str):
        self.internal[name] = path
        stdout.write(f"Succesfully registered {path} as {name}.")
    def __del_cli(self, name:str):
        del self.internal[name]
        stdout.write(f"Succesfully deleted {name}.")
    def __run_cli(self, name:str, args:list):
        if name not in self.internal:
            stderr.write(f'run: {name} is unreferenced.')
            exit(1)
        else:
            app_type = self.__get_type(name)
            all = [app_type]
            for a in args: all.append(a)
            all = ' '.join(all)
            system(all)

    def __save(self) -> None:
        with open('clihub.json', 'w') as f:
            dump(self.internal, f)
    def __load(self) -> None:
        with open('clihub.json', 'r') as f:
            self.internal = load(f)

    def __help(self) -> None:
        stdout.write(f"clihub.py:\n\t-h | --help:\tshows this message.\n\tadd (app-name, app-path):\tadds (app-path) with (app-name) as reference.\n\tdel (app-name):\tdeletes (app-name) reference.\n\trun (app-name, ...):\texecutes (app-name) with (...) as arguments.\n\t\tsupported:\n\t\t\tclihub has support for: {self.support.__str__()}.\n")

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