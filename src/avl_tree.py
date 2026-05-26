from packet_rule import PacketRule

class AVLNode:
    def __init__(self, rule: PacketRule):
        self.rule = rule
        self.left = None
        self.right = None
        self.height = 1


class AvlRouterTree:
    def __init__(self):
        self.root = None

    def _get_height(self, node):
        return node.height if node else 0

    def _get_balance(self, node):
        return self._get_height(node.left) - self._get_height(node.right) if node else 0

    def rotate_right(self, y):
        x = y.left
        T2 = x.right

        # Executa a rotação
        x.right = y
        y.left = T2

        # Atualiza as alturas
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))

        return x

    def rotate_left(self, y):
        x = y.right
        T2 = x.left

        # Executa a rotação
        x.left = y
        y.right = T2

        # Atualiza as alturas
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))

        return x

    def insert_rule(self, rule: PacketRule):
        self.root = self._insert(self.root, rule)

    def _insert(self, root, rule: PacketRule):
        if not root:
            return AVLNode(rule)

        if rule.id_rule < root.rule.id_rule:
            root.left = self._insert(root.left, rule)
        else:
            root.right = self._insert(root.right, rule)

        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))

        balance = self._get_balance(root)

        # Caso 1: Direita Simples (Esquerda Esquerda)
        if balance > 1 and rule.id_rule < root.left.rule.id_rule:
            return self.rotate_right(root)

        # Caso 2: Esquerda Simples (Direita Direita)
        if balance < -1 and rule.id_rule > root.right.rule.id_rule:
            return self.rotate_left(root)

        # Caso 3: Dupla Direita (Esquerda Direita)
        if balance > 1 and rule.id_rule > root.left.rule.id_rule:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        # Caso 4: Dupla Esquerda (Direita Esquerda)
        if balance < -1 and rule.id_rule < root.right.rule.id_rule:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def display_tree(self, node=None, level=0):
        if not node:
            node = self.root
        if not node:
            return

        if node.right:
            self.display_tree(node.right, level + 1)

        print('    ' * level + f"[{node.rule.id_rule}: H={node.height}]")

        if node.left:
            self.display_tree(node.left, level + 1)