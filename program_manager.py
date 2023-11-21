from server_object import ServerObject
import socket, select

class ProgramManager:
    list_of_servers = {}  # server_id => ServerObject
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

    def add_server(self, server_id, server_ip, server_port):
        pass

    def udp_send(self, src_server_id, dest_server_id):
        pass

    def listen(self, server_ip, server_port, exit_event):
        # create a UDP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((server_ip, server_port))
        while not exit_event.is_set():
            readable, _, _ = select.select([server_socket], [], [], 1)
            if readable:
                message, client_address = server_socket.recvfrom(2048)
                packet = message.decode()
                # self.parse_packet(packet) TODO
        server_socket.close()

    def parse_packet(self, packet):
        pass

    def start_timer(self, exit_event):
        pass

    def disable_connection(self, host_id, server_id):
        pass

    def close_all_connections(self):
        pass
