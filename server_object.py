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

    def display_routing_table(self):
        pass

    def get_packets_rcvd(self):
        pass

    def update_distance_vector(self):
        from program_manager import ProgramManager
        dv_updated = False
        for server_id in ProgramManager().list_of_servers:
            if self.server_id == server_id:
                continue
            least_cost = float('inf')
            next_hop_server_id = None
            for neighbor_id in self.neighbors:
                if self.neighbors[neighbor_id] == float('inf'):
                    continue
                # D_x(y) = min_v{c(x,v) + D_v(y)}
                curr_cost = self.get_neighbor_cost(neighbor_id) + self.neighbor_dv[neighbor_id][server_id]['least_cost']
                if curr_cost < least_cost:
                    least_cost = curr_cost
                    next_hop_server_id = neighbor_id
            if self.distance_vector[server_id]['least_cost'] != least_cost:
                dv_updated = True
            self.distance_vector[server_id]['least_cost'] = least_cost
            self.distance_vector[server_id]['next_hop_server_id'] = next_hop_server_id
        if dv_updated:
            for neighbor_id in self.neighbors:
                if self.neighbors[neighbor_id] == float('inf'):
                    continue
                # ProgramManager().udp_send(self.server_id, neighbor_id) TODO