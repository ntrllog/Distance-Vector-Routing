from program_manager import ProgramManager
import threading
import socket
import os


# Function to handle the first server command
def validate_command(server_command):
    parts = server_command.split()

    # Check if the command starts with 'server'
    if parts[0] != "server":
        return "Error: Command must start with 'server'.", None, None

    # Check if '-t' is present and followed by a file name
    if "-t" not in parts or len(parts) <= parts.index("-t") + 1:
        return "Error: Missing topology file name.", None, None

    file_name = parts[parts.index("-t") + 1]
    if not os.path.isfile(file_name):
        return f"Error: File '{file_name}' does not exist.", None, None

    # Check if '-i' is present and followed by a time interval
    if "-i" not in parts or len(parts) <= parts.index("-i") + 1:
        return "Error: Missing routing update interval.", None, None

    update_interval = int(parts[parts.index("-i") + 1])

    # Check if there are any additional inputs after <routing-update-interval>
    if len(parts) > parts.index("-i") + 2:
        return "Error: Additional inputs found after <routing-update-interval>.", None, None

    return "valid", file_name, update_interval


if __name__ == '__main__':
    program_manager = ProgramManager()

    # ask for user command (only accept "server" at the beginning),
    # and read topology file
    print("Enter 'server -t <topology-file-name> -i <routing-update-interval>' at the startup.")
    while True:
        try:
            user_input = input("Enter a command: ")
            validation_result, file_name, update_interval = validate_command(user_input)
            if validation_result == "valid":
                host_id = program_manager.init_topology(file_name)
                host_server = program_manager.get_server_by_id(host_id)
                program_manager.set_update_interval(update_interval)
                break
            else:
                print("Please re-enter the command.")
                print("'server -t <topology-file-name> -i <routing-update-interval>'")
        except Exception as e:
            print(f"{e}")
            print("Please re-enter the command correctly.")

    # initialize this server's distance vector
    host_server.init_distance_vector()

    # start UDP socket (using this server's ip and port) on another thread
    host_ip = host_server.server_ip
    host_port = host_server.server_port
    exit_event = threading.Event()
    socket_thread = threading.Thread(target=program_manager.listen, args=[host_ip, host_port, exit_event])
    socket_thread.start()

    # start timer on another thread
    timer_thread = threading.Thread(target=program_manager.start_timer, args=[exit_event])
    timer_thread.start()

    # ask for user input
    while True:
        try:
            command = input('Enter a command: ').split()
            if command[0] == 'update':
                server_id_1, server_id_2, link_cost = int(command[1]), int(command[2]), command[3]
                if link_cost == 'inf':
                    link_cost = float('inf')
                else:
                    link_cost = int(link_cost)
                if server_id_1 != host_server.server_id and server_id_2 != host_server.server_id:
                    print(f'update ERROR: Server {host_server.server_id} is not part of the link.')
                else:
                    if server_id_1 == host_server.server_id:
                        host_server.add_neighbor_cost(server_id_2, link_cost)
                    elif server_id_2 == host_server.server_id:
                        host_server.add_neighbor_cost(server_id_1, link_cost)
                    program_manager.update_distance_vector(host_server.server_id)
                    print('update SUCCESS')
            elif command[0] == 'step':
                for neighbor_id in host_server.neighbors:
                    if host_server.get_neighbor_cost(neighbor_id) == float('inf'):
                        continue
                    program_manager.udp_send(neighbor_id)
                print('step SUCCESS')
            elif command[0] == 'packets':
                print(f"Packets received: {host_server.get_packets_rcvd()}")
                print('packets SUCCESS')
            elif command[0] == 'display':
                host_server.display_routing_table()
                print('display SUCCESS')
            elif command[0] == 'disable':
                server_id = int(command[1])
                is_neighbor = False
                for neighbor_id in host_server.neighbors:
                    if server_id == neighbor_id and host_server.get_neighbor_cost(neighbor_id) != float('inf'):
                        host_server.add_neighbor_cost(server_id, float('inf'))
                        program_manager.update_distance_vector(host_server.server_id)
                        is_neighbor = True
                        break
                if not is_neighbor:
                    raise Exception(f'Server {server_id} is not a neighbor')
                print('disable SUCCESS')
                pass
            elif command[0] == 'crash':
                print('crash SUCCESS')
                exit_event.set()
                exit()
            elif command[0] == 'help':
                pass
        except KeyboardInterrupt:
            exit_event.set()
            exit()
        except IndexError:
            # not enough/too many args passed to update or disable command
            print(f'{command[0]} ERROR: wrong number of args passed')
        except ValueError:
            # args to update or disable command are not numbers
            print(f'{command[0]} ERROR: arg passed is not a number')
        except KeyError:
            # a host has not received a distance vector from one of its neighbors yet
            # false alarm -- don't need to do anything
            pass
        except Exception as e:
            print(f'{command[0]} ERROR: {e}')
