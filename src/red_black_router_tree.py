from packet_rule import PacketRule

RED = 0
BLACK = 1

class RBTNode:
    def __init__(self, rule: PacketRule):
        self.rule = rule
        self.left = None
        self.right = None
        self.parent = None
        self.color = RED

class RedBlackRouterTree:
    def __init__(self):
        self.Tnil = RBTNode(PacketRule(id_rule=0, src_ip="", dst_ip="", priority=0))
        self.Tnil.color = BLACK
        self.root = self.Tnil

    def insert_rule(self, rule: PacketRule):
        new_node = RBTNode(rule)
        new_node.left = self.Tnil
        new_node.right = self.Tnil
        new_node.color = RED

        y = None
        x = self.root

        while x != self.Tnil:
            y = x
            if new_node.rule.id_rule < x.rule.id_rule:
                x = x.left
            else:
                x = x.right

        new_node.parent = y

        # Tratamento tático do pai nulo (Árvore vazia)
        if y is None:
            self.root = new_node
            new_node.color = BLACK
            return
        elif new_node.rule.id_rule < y.rule.id_rule:
            y.left = new_node
        else:
            y.right = new_node

        # Se o avô não existir, a propriedade RBT está preservada
        if new_node.parent.parent is None:
            return

        # Executa o fixup se houver colisão de nós vermelhos
        if new_node.parent.color == RED:
            self._fix_insert(new_node)