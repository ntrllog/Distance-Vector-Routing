class ServerObject:
    def __init__(self, server_id, server_ip, server_port):
        self.server_id = server_id
        self.server_ip = server_ip
        self.server_port = server_port
        self.neighbors = {} # server_id => actual cost
        self.distance_vector = {} # server_id => {'least_cost' => least_cost, 'next_hop_server_id' => server_id}
        self.neighbor_dv = {} # neighbor_id => {server_id => {'least_cost' => least_cost, 'next_hop_server_id' => server_id}}
        self.num_packets_rcvd = 0

    def init_distance_vector(self):
        pass

    def add_neighbor_cost(self, server_id, cost):
        pass

    def get_least_cost(self, server_id):
        pass

    def get_next_hop_server_id(self, server_id):
        pass

    def get_neighbor_cost(self, server_id):
        pass

    def update_neighbor_cost(self, server_id, cost):
        pass

    def display_routing_table(self):
        pass

    def get_packets_rcvd(self):
        pass

    def update_distance_vector(self):
        pass
