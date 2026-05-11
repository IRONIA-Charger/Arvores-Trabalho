class PacketRule:
    def __init__(self, id_rule:int, src_ip:str, dst_ip:str, priority:int):
        self.id_rule = id_rule
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.priority = priority
    def __repr__(self):
        return f"<PacketRule ID:{self.id_rule} | Prio:{self.priority} | {self.src_ip} -> {self.dst_ip}>"
    def to_dict(self):
        return {
            "id": self.id_rule,
            "priority": self.priority,
            "src_ip": self.src_ip,
            "dst_ip": self.dst_ip,
        }