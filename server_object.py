class ServerObject:
    def __init__(self, server_id, server_ip, server_port):
        self.server_id = server_id
        self.server_ip = server_ip
        self.server_port = server_port
        self.neighbors = {} # server_id => actual cost
        self.distance_vector = {} # server_id => {'least_cost' => least_cost, 'next_hop_server_id' => server_id}
        self.neighbor_dv = {} # server_id => {'least_cost' => least_cost, 'next_hop_server_id' => server_id}
        self.num_packets_rcvd = 0

    def init_distance_vector(self):
        for server_id in self.neighbors:
            if server_id == self.server_id:
                # For the host server, set least_cost to 0 and next_hop_server_id to itself
                self.distance_vector[server_id] = {'least_cost': 0, 'next_hop_server_id': self.server_id}
            else:
                # For neighbors, set least_cost to their actual cost and next_hop_server_id to themselves
                self.distance_vector[server_id] = {'least_cost': self.neighbors[server_id],
                                                   'next_hop_server_id': server_id}

    def add_neighbor_cost(self, server_id, cost):
        # Add the neighbor's cost to the neighbors dictionary
        self.neighbors[server_id] = cost

    def get_least_cost(self, server_id):
        pass

    def get_next_hop_server_id(self, server_id):
        pass

    def get_neighbor_cost(self, server_id):
        pass

    def update_neighbor_cost(self, server_id, cost):
        pass

    def display_routing_table(self):
        # Sort the keys (server IDs) in ascending order
        sorted_server_ids = sorted(self.distance_vector.keys())

        # Print the routing table in the desired format
        print("Routing Table:")
        print("<destination-server-ID> <next-hop-server-ID> <cost-of-path>")
        for server_id in sorted_server_ids:
            entry = self.distance_vector[server_id]
            destination = server_id
            next_hop = entry['next_hop_server_id']
            cost = entry['least_cost']
            print(f"{destination} {next_hop} {cost}")

    def get_packets_rcvd(self):
        pass

    def update_distance_vector(self):
        pass
