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

    def _fix_insert(self, k):
        while k.parent.color == RED:
            if k.parent == k.parent.parent.left:
                uncle = k.parent.parent.right

                if uncle.color == RED:
                    k.parent.color = BLACK
                    uncle.color = BLACK
                    k.parent.parent.color = RED
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = BLACK
                    k.parent.parent.color = RED
                    self.right_rotate(k.parent.parent)
            else:
                uncle = k.parent.parent.left

                if uncle.color == RED:
                    k.parent.color = BLACK
                    uncle.color = BLACK
                    k.parent.parent.color = RED
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = BLACK
                    k.parent.parent.color = RED
                    self.left_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = BLACK

    def left_rotate(self, x):
        y = x.right
        x.right = y.left

        if y.left != self.Tnil:
            y.left.parent = x
        y.parent = x.parent

        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right

        if y.right != self.Tnil:
            y.right.parent = x
        y.parent = x.parent

        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y
