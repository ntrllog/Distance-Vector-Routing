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

    def update_link_cost(self, server_id_1, server_id_2, cost):
        pass

    def start_timer(self, exit_event):
        pass

    def disable_connection(self, host_id, server_id):
        pass

    def close_all_connections(self):
        pass
