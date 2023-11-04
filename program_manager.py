class ProgramManager:
    list_of_servers = {} # server_id => ServerObject
    update_interval = 0

    def init_topology(self, file_name):
        pass

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
