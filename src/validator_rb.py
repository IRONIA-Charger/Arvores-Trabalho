import random
from packet_rule import PacketRule
from red_black_router_tree import RedBlackRouterTree, BLACK, RED


def validate_rbt_compact(tree_obj: RedBlackRouterTree):
    if tree_obj.root == tree_obj.Tnil: return True, 0, 0
    if tree_obj.root.color != BLACK: return False, 0, 0

    expected_black_height = None
    max_height = 0

    def dfs(node, current_black_height, current_height):
        nonlocal expected_black_height, max_height
        if current_height > max_height: max_height = current_height

        if node == tree_obj.Tnil:
            current_black_height += 1
            if expected_black_height is None: expected_black_height = current_black_height
            return current_black_height == expected_black_height

        if node.color == BLACK: current_black_height += 1

        # Double Red Check
        if node.color == RED and (node.left.color == RED or node.right.color == RED): return False

        # Integridade de BST e Ponteiros de Pai
        if node.left != tree_obj.Tnil and (
                node.left.rule.id_rule >= node.rule.id_rule or node.left.parent != node): return False
        if node.right != tree_obj.Tnil and (
                node.right.rule.id_rule <= node.rule.id_rule or node.right.parent != node): return False

        return dfs(node.left, current_black_height, current_height + 1) and dfs(node.right, current_black_height,
                                                                                current_height + 1)

    is_valid = dfs(tree_obj.root, 0, 1)
    return is_valid, max_height, (expected_black_height if expected_black_height else 0)

if __name__ == "__main__":
    random.seed(42)
    print("=" * 55)
    print("    AUDITORIA RBT (SEED 42)    ")
    print("=" * 55)

    tree = RedBlackRouterTree()
    regras = [
        PacketRule(id_rule=15, src_ip="192.168.1.1", dst_ip="10.0.0.5", priority=3),
        PacketRule(id_rule=10, src_ip="192.168.1.2", dst_ip="10.0.0.6", priority=2),
        PacketRule(id_rule=20, src_ip="192.168.1.3", dst_ip="10.0.0.7", priority=1),
        PacketRule(id_rule=5, src_ip="192.168.1.4", dst_ip="10.0.0.8", priority=5),
    ]

    print("\n[>] Inserindo Regras...")
    for r in regras:
        tree.insert_rule(r)
        ok, h, bh = validate_rbt_compact(tree)
        print(f" [+] ID {r.id_rule:2} | Status RBT: {ok} | H: {h} | BH: {bh}")

    print("\n[>] Removendo regra ID 10...")
    tree.delete_rule(10)
    ok, h, bh = validate_rbt_compact(tree)
    print(f" [*] Pós-Deleção ID 10 | Status RBT: {ok} | H: {h} | BH: {bh}")
    print("\n" + "=" * 55)
