from program_manager import ProgramManager
from server_object import ServerObject
import threading

if __name__ == '__main__':
    program_manager = ProgramManager()

    # ask for user command (only accept "server" at the beginning)

    # read topology file

    # initialize this server's distance vector

    # send this server's distance vector to its neighbors

    # start UDP socket (using this server's ip and port) on another thread
    exit_event = threading.Event()
    socket_thread = threading.Thread(target=program_manager.listen, args=[host_server.server_ip, host_server.server_port, exit_event])
    socket_thread.start()

    # start timer on another thread

    # ask for user input
    while True:
        try:
            command = input('Enter a command: ').split()
            if command[0] == 'update':
                server_id_1, server_id_2, link_cost = int(command[1]), int(command[2]), int(command[3])
                if server_id_1 != host_server.server_id and server_id_2 != host_server.server_id:
                    continue
                if server_id_1 == host_server.server_id:
                    host_server.add_neighbor_cost(server_id_2, link_cost)
                elif server_id_2 == host_server.server_id:
                    host_server.add_neighbor_cost(server_id_1, link_cost)
                host_server.update_distance_vector()
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
