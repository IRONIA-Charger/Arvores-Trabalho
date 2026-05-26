from packet_rule import PacketRule
from red_black_router_tree import RedBlackRouterTree


# Função auxiliar na main para varrer a árvore e mostrar os nós ordenados
def print_in_order(node, tnil):
    if node != tnil:
        print_in_order(node.left, tnil)

        # Mapeia o bit da cor para um emoji tático
        # 0 = RED, 1 = BLACK
        cor_emoji = "🔴" if node.color == 0 else "⚫"
        parent_id = node.parent.rule.id_rule if node.parent else "Raiz"

        print(f" Regra ID: {node.rule.id_rule:<3} | Cor: {cor_emoji} | Pai ID: {parent_id}")

        print_in_order(node.right, tnil)


def executar_teste():
    print("=" * 55)
    print("🛡️ PROTOCOLO DE TESTE - RED BLACK ROUTER TREE 🛡️")
    print("=" * 55)

    # 1. Inicializa a árvore
    roteador = RedBlackRouterTree()

    # 2. Dados de teste (IDs fora de ordem/decrescentes para forçar balanceamento)
    regras = [
        PacketRule(id_rule=50, src_ip="10.0.0.1", dst_ip="192.168.1.50", priority=1),
        PacketRule(id_rule=40, src_ip="10.0.0.2", dst_ip="192.168.1.40", priority=2),
        PacketRule(id_rule=30, src_ip="10.0.0.3", dst_ip="192.168.1.30", priority=3),
        PacketRule(id_rule=20, src_ip="10.0.0.4", dst_ip="192.168.1.20", priority=4),
        PacketRule(id_rule=10, src_ip="10.0.0.5", dst_ip="192.168.1.10", priority=5)
    ]

    # 3. Carga no Firewall
    for r in regras:
        roteador.insert_rule(r)
        print(f"[+] PacketRule ID {r.id_rule} injetado com sucesso.")

    print("\n" + "-" * 55)
    print("📋 AUDITORIA DO PERÍMETRO (TRAVESSIA IN-ORDER):")
    print("-" * 55)

    # Chama a função passando a raiz e o nó sentinela Tnil da sua árvore
    print_in_order(roteador.root, roteador.Tnil)
    print("=" * 55)


if __name__ == "__main__":
    executar_teste()