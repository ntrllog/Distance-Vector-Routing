class Packet:
    def __init__(self, num_update_fields, src_server_ip, src_server_port, distance_vector):
        self.num_update_fields = num_update_fields
        self.src_server_ip = src_server_ip
        self.src_server_port = src_server_port
        self.distance_vector = distance_vector # [{'server_id' => server_id, 'server_port' => server_port, 'cost' => cost, 'next_hop_server_id' => server_id},]

    def __str__(self):
        return f'{self.num_update_fields}/{self.src_server_ip}/{self.src_server_port}/{self.distance_vector}'
