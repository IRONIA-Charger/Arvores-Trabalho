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

    def _tree_minimum(self, node):
        while node.left != self.Tnil:
            node = node.left
        return node

    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete_rule(self, id_rule: int):
        # Busca iterativa (mais rápida para o firewall)
        z = self.root
        while z != self.Tnil and z.rule.id_rule != id_rule:
            if id_rule < z.rule.id_rule:
                z = z.left
            else:
                z = z.right

        if z == self.Tnil:
            print(f"[-] Regra ID {id_rule} não encontrada no Firewall.")
            return

        self._delete_node(z)

    def _delete_node(self, z):
        y = z
        y_original_color = y.color

        if z.left == self.Tnil:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.Tnil:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._tree_minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        # Se um nó PRETO saiu, a altura preta quebrou. Chama a cavalaria.
        if y_original_color == BLACK:
            self._fix_delete(x)

    def _fix_delete(self, x):
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                w = x.parent.right

                # Caso 1: Irmão Vermelho
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.left_rotate(x.parent)
                    w = x.parent.right

                # Caso 2: Irmão Preto e ambos os filhos pretos
                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    # Caso 3: Irmão Preto, filho esquerdo vermelho
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self.right_rotate(w)
                        w = x.parent.right

                    # Caso 4: Irmão Preto, filho direito vermelho
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left

                # Caso 1 Espelhado
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.right_rotate(x.parent)
                    w = x.parent.left

                # Caso 2 Espelhado
                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    # Caso 3 Espelhado
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self.left_rotate(w)
                        w = x.parent.left

                    # Caso 4 Espelhado
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self.right_rotate(x.parent)
                    x = self.root

        x.color = BLACK

