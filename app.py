import os
import subprocess
import sys
import pyfiglet

class Files:
    def __init__(self):
        self.current_dir = ['.']
        self.parent_dir = ['..']
        self.folders = [folder for folder in next(os.walk('.'))[1]]
        self.files = [file for file in next(os.walk('.'))[2]]
        self.directory = self.current_dir + self.parent_dir + self.folders + self.files

def list_directory(path):
    try:
        print(f"Listing contents of {path}")
        for item in os.listdir(path):
            print(item)
    except Exception as e:
        print(f"Error: {e}")

def print_working_directory(path):
    print(f"Current directory: {path}")

def change_directory(current_path, dir_name):
    if dir_name == '..':
        new_path = os.path.dirname(current_path)
    else:
        new_path = os.path.join(current_path, dir_name)
    
    if os.path.isdir(new_path):
        print(f"Changing directory to {new_path}")
        return new_path
    else:
        print(f"{dir_name} is not a valid directory")
        return current_path

def create_file(path, file_name):
    try:
        with open(os.path.join(path, file_name), 'w') as f:
            pass
        print(f"File {file_name} created.")
    except Exception as e:
        print(f"Error: {e}")

def remove_file(path, file_name):
    try:
        os.remove(os.path.join(path, file_name))
        print(f"File {file_name} removed.")
    except Exception as e:
        print(f"Error: {e}")

def create_directory(path, dir_name):
    try:
        os.makedirs(os.path.join(path, dir_name))
        print(f"Directory {dir_name} created.")
    except Exception as e:
        print(f"Error: {e}")

def remove_directory(path, dir_name):
    try:
        os.rmdir(os.path.join(path, dir_name))
        print(f"Directory {dir_name} removed.")
    except Exception as e:
        print(f"Error: {e}")

def read_file(path, file_name):
    try:
        with open(os.path.join(path, file_name), 'r') as f:
            print(f.read())
    except Exception as e:
        print(f"Error: {e}")

def open_file(file):
    try:
        output = _open_file(file)
        if output.returncode != 0:
            for index, files in enumerate(Files().directory, start=1):
                if str(index) == file:
                    if os.path.isdir(files):
                        input("Cannot open directory. Press Enter to continue...")
                        return
                    output = _open_file(files)
                    if output.stderr:
                        input(output.stderr + 'Press ENTER to continue...')
                    return
            input('File does not exist. Press ENTER to continue...')
    except OSError as err:
        input(str(err) + ' Press ENTER to continue...')

def _open_file(file):
    if sys.platform == 'win32':
        return subprocess.run(
            [file],
            shell=True,
            capture_output=True,
            encoding='utf-8'
        )
    if sys.platform == 'linux':
        return subprocess.run(
            ['xdg-open', file],
            shell=True,
            capture_output=True,
            encoding='utf-8'
        )
    raise OSError("'OPEN' command not supported for this platform.")

def rename_file(path, old_name, new_name):
    try:
        os.rename(os.path.join(path, old_name), os.path.join(path, new_name))
        print(f"Renamed {old_name} to {new_name}")
    except Exception as e:
        print(f"Error: {e}")

def show_help():
    print("\t\t\t AVAILABLE COMMANDS")

    help_text = """
    ls                  List the contents of the current directory.
    pwd                 Print the current working directory.
    cd <dir>            Change the current directory to <dir>.
    touch <file>        Create a new file named <file>.
    rm <file>           Remove the file named <file>.
    mkdir <dir>         Create a new directory named <dir>.
    rmdir <dir>         Remove the directory named <dir>.
    cat <file>          Display the contents of the file named <file>.
    open <file>         Open the file named <file> with the default application.
    rename <old> <new>  Rename a file or directory from <old> to <new>.
    up                  Move up one directory level.
    exit                Exit the CLI file explorer.
    help                Display this help message.
    """
    
    print(help_text)

def main():
    print(pyfiglet.figlet_format("CLI File Explorer"))
    show_help()
    current_path = os.getcwd()

    commands = {
        'ls': lambda args: list_directory(current_path),
        'pwd': lambda args: print_working_directory(current_path),
        'cd': lambda args: change_directory(current_path, args[1]),
        'touch': lambda args: create_file(current_path, args[1]),
        'rm': lambda args: remove_file(current_path, args[1]),
        'mkdir': lambda args: create_directory(current_path, args[1]),
        'rmdir': lambda args: remove_directory(current_path, args[1]),
        'cat': lambda args: read_file(current_path, args[1]),
        'open': lambda args: open_file(args[1]),
        'rename': lambda args: rename_file(current_path, args[1], args[2]),
        'up': lambda args: os.path.dirname(current_path),
        'exit': lambda args: exit("Exiting File Explorer..."),
        'help': lambda args: show_help(),
    }

    while True:
        command = input(">>> ").strip().split()
        if command:
            cmd = command[0]
            func = commands.get(cmd, lambda args: print("UNKNOWN COMMAND!"))
            try:
                result = func(command)
                if result:
                    current_path = result
            except IndexError:
                print("Missing arguments for command. Type 'help' for usage.")

if __name__ == "__main__":
    main()