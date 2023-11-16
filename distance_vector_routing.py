from program_manager import ProgramManager
from server_object import ServerObject
import threading
import os


def validate_command(server_command):
    parts = server_command.split()

    # Check if the command starts with 'server'
    if parts[0] != "server":
        return "Error: Command must start with 'server'.", None

    # Check if '-t' is present and followed by a file name
    if "-t" not in parts or len(parts) <= parts.index("-t") + 1:
        return "Error: Missing topology file name.", None

    file_name = parts[parts.index("-t") + 1]
    if not os.path.isfile(file_name):
        return f"Error: File '{file_name}' does not exist.", None

    # Check if '-i' is present and followed by a time interval
    if "-i" not in parts or len(parts) <= parts.index("-i") + 1:
        return "Error: Missing routing update interval.", None

    try:
        interval = int(parts[parts.index("-i") + 1])
        if not 1 <= interval <= 10:
            return "Error: Routing update interval must be between 1 and 10 seconds.", None
    except ValueError:
        return "Error: Routing update interval must be a number.", None

    return "valid", file_name


if __name__ == '__main__':
    program_manager = ProgramManager()

    # ask for user command (only accept "server" at the beginning),
    # and read topology file
    print("Enter 'server -t <topology-file-name> -i <routing-update-interval>' at the startup.")
    while True:
        try:
            user_input = input("Enter a command: ")
            validation_result, file_name = validate_command(user_input)
            if validation_result == "valid":
                host_id = program_manager.init_topology(file_name)  # debug
                host_server = program_manager.get_server_by_id(host_id)  # debug
                print("get_update_interval.....")  # incomplete
                break
            else:
                print(validation_result)
                print("Please re-enter the command.")
                print("'server -t <topology-file-name> -i <routing-update-interval>'")
        except Exception as e:
            print(f"{e}")
            print("Please re-enter the command correctly.")

    # initialize this server's distance vector
    host_server.init_distance_vector()
    host_server.display_routing_table() # debug

    # start UDP socket (using this server's ip and port) on another thread
    exit_event = threading.Event()

    # start timer on another thread

    # ask for user input
    while True:
        try:
            command = input('Enter a command: ').split()
            if command[0] == 'update':
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
