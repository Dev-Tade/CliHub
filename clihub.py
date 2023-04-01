from json           import load, dump
from sys            import argv, stderr, stdout
from os             import path, system

class CliHub:
    def __init__(self) -> None:
        self.internal_cli = {}

        if not path.exists('clihub.json'):
            with open('clihub.json','w') as f:
                dump(self.internal_cli, f)

    def __new_cli(self, name:str, path:str) -> None:
        self.internal_cli[name] = path
        stdout.write(f"Succesfully registered {path} as {name}.")

    def __del_cli(self, name:str) -> None:
        del self.internal_cli[name]
        stdout.write(f"Succesfully deleted {name}.")

    def __flush(self) -> None:
        self.internal_cli = {}
        self.__save()

    def __run_cli(self, name:str, args:list) -> None:
        if name not in self.internal_cli:
            stderr.write(f'run: {name} isn\'t registered.')
            exit(1)
        else:
            name = self.internal_cli[name]
            _args = [arg for arg in args]; _args = ' '.join(_args)
            system(name+' '+_args)

    def __save(self) -> None:
        with open('clihub.json', 'w') as f:
            dump(self.internal_cli, f)

    def __load(self) -> None:
        with open('clihub.json', 'r') as f:
            self.internal_cli = load(f)

    def __help(self) -> None:
        stdout.write(
            f"""
    clihub.py:
        <command> | <app-name> <...>:   if <app-name> is binded executes it with <...> as args
                                        if <app-name> isn't binded executes <command> as clihub command.
        <command>:
            help | -h | --help:             shows this message.
            bind   <app-name> <app-path>:   binds <app-path> with <app-name>.
            unbind <app-name>:              unbinds <app-name> reference.
            flush:                          unbinds all references.
            """
        )

    def run(self) -> None:
        self.__load()
        if not len(argv) >= 2:
            stderr.write(f'Not enough arguments. Try -h')
            exit(1)
        else:
            action = argv[1]
            match action:
                case 'bind':
                    if not len(argv) >= 4:
                        stderr.write("bind: Missing arguments 'app-name', 'app-path'")
                        exit(1)
                    else:
                        self.__new_cli(argv[2],argv[3])
                case 'unbind':
                    if not len(argv) >= 3:
                        stderr.write("unbind: Missing argument 'app-name'")
                        exit(1)
                    else:
                        self.__del_cli(argv[2])
                case '-h':
                    self.__help()
                case '--help':
                    self.__help()
                case 'help':
                    self.__help()
                case 'flush':
                    self.__flush()
                case _:
                    if argv[1] in self.internal_cli:
                        self.__run_cli(argv[1], argv[2:])
                    else:
                        stderr.write(f"action/tool \"{argv[1]}\" isn't defined")
                        exit(1)
        self.__save()

if __name__ == '__main__':
    hub = CliHub()
    hub.run()