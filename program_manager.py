from server_object import ServerObject
from packet import Packet
import socket, select
import time


class ProgramManager:
    list_of_servers = {}  # server_id => ServerObject
    time_stamp = {} # server_id => {'timestamp': timestamp, 'update_interval': update_inverval}
    update_interval = 0
    our_server_id = None
    host_server = None

    def read_file(self, file_name):
        try:
            with open(file_name, 'r') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: The file '{file_name}' was not found.")
            return None
        except IOError:
            print(f"Error: An IO error occurred while reading '{file_name}'.")
            return None
        except Exception as e:
            print(f"Error: An unexpected error occurred: {e}")
            return None

    def validate_topology_file(self, lines, num_servers, num_edges):
        # Attempt to convert the first line to an integer
        try:
            first_line = int(lines[0])
        except ValueError:
            print("Error: The first line does not contain a valid number.")
            return False

        # Attempt to convert the second line to an integer
        try:
            second_line = int(lines[1])
        except ValueError:
            print("Error: The second line does not contain a valid number.")
            return False

        # Check if the number of lines is correct
        expected_line_count = 2 + num_servers + num_edges
        if len(lines) != expected_line_count:
            print("Error: The topology file does not contain the correct number of servers or neighbors.")
            return False

        # Extract "our" server ID from the first number in the last num_edges lines
        try:
            self.our_server_id = int(lines[2 + num_servers + num_edges - 1].split()[0])
        except ValueError:
            print("Error: Unable to determine host server from the topology file.")
            return False

        return True

    def parse_topology(self, content):
        lines = content.split('\n')
        num_servers = int(lines[0])
        num_edges = int(lines[1])

        # Validate the topology file
        if not self.validate_topology_file(lines, num_servers, num_edges):
            raise Exception("Invalid topology file.")

        # Split the content into lines and process server information
        lines = content.split('\n')
        for i in range(2, 2 + num_servers):
            line = lines[i].split()
            server_id = int(line[0])
            ip = line[1]
            port = int(line[2])
            self.list_of_servers[server_id] = ServerObject(server_id, ip, port)

        # Get the host server ServerObject based on our_server_id
        self.host_server = self.get_server_by_id(self.our_server_id)

        # Retrieve neighbor id and cost from the content and add it to the host_server's neighbors
        for i in range(2 + num_servers, 2 + num_servers + num_edges):
            line = lines[i].split()
            neighbor_id = int(line[1])
            cost = int(line[2])
            self.host_server.add_neighbor_cost(neighbor_id, cost)

        # Set a large cost (e.g., infinity) for non-direct neighbors
        for server_id in self.list_of_servers.keys():
            if server_id != self.host_server.server_id and server_id not in self.host_server.neighbors:
                self.host_server.add_neighbor_cost(server_id, float('inf'))

    def init_topology(self, file_name):
        content = self.read_file(file_name)
        if not content:
            raise Exception("Error: The topology file is empty or could not be read.")

        # Parse the topology file and populate the list_of_servers dictionary
        # Get the host server ServerObject based on our_server_id
        # Also retrieve neighbor id and cost from the content and add it to the host_server's neighbors
        self.parse_topology(content)

        return self.our_server_id

    def get_server_by_id(self, server_id):
        # Check if the server_id exists in the list_of_servers dictionary
        if server_id in self.list_of_servers:
            # Return the ServerObject associated with the server_id
            return self.list_of_servers[server_id]
        else:
            # Server with the given ID does not exist
            print("Server with the given ID does not exist")
            return None

    def set_update_interval(self, update_interval):
        self.update_interval = update_interval

    def udp_send(self, dest_server_id):
        # Get the destination server's IP and port from the list_of_servers
        dest_server = self.get_server_by_id(dest_server_id)

        # Create a Packet object with the relevant information
        num_update_fields = len(self.host_server.distance_vector)  # Number of update fields in the distance vector
        src_server_ip = self.host_server.server_ip
        src_server_port = self.host_server.server_port
        distance_vector = self.host_server.distance_vector

        # Serialize the Packet object to a string
        packet = Packet(num_update_fields, src_server_ip, src_server_port, distance_vector)
        packet_str = str(packet) + f"/{self.update_interval}"

        # Create a UDP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            # Send the serialized Packet to the destination server
            client_socket.sendto(packet_str.encode(), (dest_server.server_ip, dest_server.server_port))
        except Exception as e:
            print(f"Error sending UDP message to server {dest_server_id}: {e}")
        finally:
            client_socket.close()

    def listen(self, server_ip, server_port, exit_event):
        # create a UDP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((server_ip, server_port))
        while not exit_event.is_set():
            readable, _, _ = select.select([server_socket], [], [], 1)
            if readable:
                message, client_address = server_socket.recvfrom(2048)
                packet = message.decode()
                self.host_server.num_packets_rcvd += 1
                update = self.parse_packet(packet)
                self.update(update[0], update[1])
        server_socket.close()
        
    def timeout(self, exit_event):
        #IDEA: Loop through our list_of_servers ids and verify they have data in 
        #the time_stamp dictionary. If 3, then "turn off" the server.
        while not exit_event.is_set():
            for id in self.list_of_servers.keys():
                if id in self.time_stamp.keys():
                    if time.time() - self.time_stamp[id]['timestamp'] >= self.time_stamp[id]['update_interval'] * 3:
                        self.host_server.turn_off(id)

    def parse_packet(self, packet):
        import ast
        # f'{self.num_update_fields}/{self.src_server_ip}/{self.src_server_port}/{self.distance_vector}/{self.update_interval}'
        packetRawData = packet.split('/')
        RAWdistance_vector = packetRawData[3]  # Obtain the raw distance vector
        RAWdistance_vector = RAWdistance_vector.replace('inf', '\"inf\"')
        RAWdistance_vector = ast.literal_eval(RAWdistance_vector)

        # get the server id of who sent the packet
        src_server_ip = packetRawData[1]
        src_server_port = packetRawData[2]
        for server in self.list_of_servers.values():
            if server.server_ip == src_server_ip and server.server_port == int(src_server_port):
                src_server_id = server.server_id
                break

        # Print a message indicating that a message was received from the source server
        print(f'RECEIVED A MESSAGE FROM SERVER {src_server_id}')

        # update the host's copy of its neighbor's distance vector
        for server_id in RAWdistance_vector:
            if src_server_id not in self.host_server.neighbor_dv:
                self.host_server.neighbor_dv[src_server_id] = {server_id: {}}
            if server_id not in self.host_server.neighbor_dv[src_server_id]:
                self.host_server.neighbor_dv[src_server_id][server_id] = {}
            self.host_server.neighbor_dv[src_server_id][server_id]['least_cost'] = RAWdistance_vector[server_id]['least_cost'] if RAWdistance_vector[server_id]['least_cost'] != 'inf' else float('inf')
            self.host_server.neighbor_dv[src_server_id][server_id]['next_hop_server_id'] = RAWdistance_vector[server_id]['next_hop_server_id']

        # update the host's distance vector
        self.update_distance_vector(self.host_server.server_id)
        return (src_server_id, int(packetRawData[4]))

    def start_timer(self, exit_event):
        start_time = time.time()  # Initialize the start time
        while not exit_event.is_set():
            current_time = time.time()  # Get the current time
            elapsed_time = current_time - start_time  # Calculate elapsed time

            if elapsed_time >= self.update_interval:
                # Iterate through the list of servers and send UDP messages
                for neighbor_id, cost in self.host_server.neighbors.items():
                    if cost != float('inf'):
                        dest_server_id = neighbor_id
                        self.udp_send(dest_server_id)

                # Reset the start time
                start_time = current_time

    def update(self, server_id, update_interval):
        self.time_stamp[server_id] = {'timestamp':time.time(), 'update_interval': update_interval}

    def update_distance_vector(self, src_server_id):
        try:
            for dest_server_id in self.list_of_servers:
                if src_server_id == dest_server_id:
                    # don't need to find cost to myself (src_server)
                    continue

                # prepare to find least cost to dest_server from src_server's neighbors
                least_cost = float('inf')
                next_hop_server_id = None
                src_server = self.get_server_by_id(src_server_id)
                for neighbor_id in src_server.neighbors:
                    if src_server.get_neighbor_cost(neighbor_id) == float('inf'):
                        continue

                    # D_x(y) = min_v{c(x,v) + D_v(y)}
                    if neighbor_id != dest_server_id:
                        # what is the cost to dest_server from one of my neighbors?
                        curr_cost = src_server.get_neighbor_cost(neighbor_id) + src_server.neighbor_dv[neighbor_id][dest_server_id]['least_cost']
                    else:
                        # the cost to dest_server if the current neighbor in the loop is dest_server is just the direct cost
                        curr_cost = src_server.get_neighbor_cost(neighbor_id)

                    if curr_cost < least_cost:
                        # there's a cheaper way to get to dest_server than what we currently are storing
                        least_cost = curr_cost
                        next_hop_server_id = neighbor_id

                src_server.distance_vector[dest_server_id]['least_cost'] = least_cost
                src_server.distance_vector[dest_server_id]['next_hop_server_id'] = next_hop_server_id
        except KeyError:
            # this host has not received a distance vector from one of its neighbors yet
            # false alarm -- don't need to do anything
            pass
