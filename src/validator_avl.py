class AVLValidator:
    @staticmethod
    def calculate_real_height(node):

        if node is None:
            return 0
        return 1 + max(AVLValidator.calculate_real_height(node.left),
                       AVLValidator.calculate_real_height(node.right))

    @staticmethod
    def validate(node):
        if node is None:
            return True

        # Em vez de ler o atributo, nós calculamos a altura real dos braços
        left_height = AVLValidator.calculate_real_height(node.left)
        right_height = AVLValidator.calculate_real_height(node.right)

        balance = left_height - right_height

        # Se o fator de balanceamento real violar a regra AVL, reporta o erro
        if abs(balance) > 1:
            return False

        return (
            AVLValidator.validate(node.left)
            and AVLValidator.validate(node.right)
        )