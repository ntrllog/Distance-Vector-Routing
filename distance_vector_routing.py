from program_manager import ProgramManager
from server_object import ServerObject
import threading
import socket

serverIP = "xxx.xxx.xxx"
serverPort = 0000

user_input = None
startupCmdEntered = False
running = True


def get_user_input():
    global user_input, startupCmdEntered, running
    while running:
        user_input = input('Enter a command: ')

        if user_input.startswith("server -t") and not startupCmdEntered:
            startupCmdEntered = True
            execute_command(user_input)
        elif not user_input.startswith("server -t") and not startupCmdEntered:
            print("COMMAND IS NOT AN AVAILABLE COMMAND")
            print("Enter 'server -t <topology-file-name> -i <routing-update-interval>' at the startup.")
        elif user_input.startswith("server -t") and startupCmdEntered:
            print("SERVER already used")
        else:
            execute_command(user_input)  # call execute_command here debug


def execute_command(commands):
    try:
        command = commands.split()
        if command[0] == 'help':
            print("Print commands list here")  # debug
            pass
        elif command[0] == 'server':
            print("Read topology file and update routing every x seconds")  # debug
            pass
        elif command[0] == 'update':
            server_id_1, server_id_2, link_cost = int(command[1]), int(command[2]), int(command[3])
            pass
        elif command[0] == 'step':
            pass
        elif command[0] == 'packets':
            pass
        elif command[0] == 'display':
            pass
        elif command[0] == 'disable':
            server_id = int(command[1])
            pass
        elif command[0] == 'crash':
            pass
    except KeyboardInterrupt:
        exit_event.set()
        exit()
    except IndexError:
        # not enough/too many args passed to update or disable command
        pass
    except ValueError:
        # args to update or disable command are not numbers
        pass


if __name__ == '__main__':
    program_manager = ProgramManager()

    # ask for user command (only accept "server" at the beginning)
    print("Enter 'server -t <topology-file-name> -i <routing-update-interval>' to startup the server.")
    input_thread = threading.Thread(target=get_user_input)
    input_thread.start()

    # read topology file

    # initialize this server's distance vector

    # start UDP socket (using this server's ip and port) on another thread
    exit_event = threading.Event()

    # start timer on another thread

    # ask for user input on another thread
