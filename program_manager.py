from server_object import ServerObject


class ProgramManager:
    list_of_servers = {}  # server_id => ServerObject
    update_interval = 0
    our_server_id = None

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
            print(f"An unexpected error occurred: {e}")
            return None

    def validate_topology_file(self, lines, num_servers, num_edges):
        # Check if the first two lines contain single numbers

        if not (lines[0].isdigit() and lines[1].isdigit()):
            print("Error: The first or second line does not contain a valid number.")
            return False

        # Check if the number of lines is correct
        expected_line_count = 2 + num_servers + num_edges
        if len(lines) != expected_line_count:
            print("Error: The topology file does not contain the correct number of lines.")
            return False

        # Use a set to track the server IDs from each line
        server_ids_sets = []

        # Process connection lines and add server IDs to sets
        connection_lines = lines[2 + num_servers:2 + num_servers + num_edges]
        for line in connection_lines:
            server_ids = set(map(int, line.split()[:2]))
            server_ids_sets.append(server_ids)

        # Find the common server ID across all lines
        common_server_id = set.intersection(*server_ids_sets)

        # Check if there is exactly one common server ID
        if len(common_server_id) == 1:
            self.our_server_id = common_server_id.pop()
        else:
            print("Error: Unable to determine 'our' server from the topology file.")
            return False

        return True

    def parse_topology(self, content):
        lines = content.split('\n')
        num_servers = int(lines[0])
        num_edges = int(lines[1])

        # Validate the topology file
        if not self.validate_topology_file(lines, num_servers, num_edges):
            raise Exception("Invalid topology file.")

        lines = content.split('\n')
        for i in range(2, 2 + num_servers):
            line = lines[i].split()
            server_id = int(line[0])
            ip = line[1]
            port = int(line[2])
            self.list_of_servers[server_id] = ServerObject(server_id, ip, port)

    def init_topology(self, file_name):
        content = self.read_file(file_name)
        if not content:
            raise Exception("Error: The topology file is empty or could not be read.")

        self.parse_topology(content)
        return self.our_server_id

    def get_server_by_id(self, server_id):
        pass

    def add_server(self, server_id, server_ip, server_port):
        pass

    def udp_send(self, src_server_id, dest_server_id):
        pass

    def listen(self, server_ip, server_port, exit_event):
        pass

    def parse_packet(self, packet):
        pass

    def update_link_cost(self, server_id_1, server_id_2, cost):
        pass

    def start_timer(self, exit_event):
        pass

    def disable_connection(self, host_id, server_id):
        pass

    def close_all_connections(self):
        pass
