import sys
from avl_tree import AvlRouterTree, AVLNode
from validator_avl import AVLValidator
from packet_rule import PacketRule


def executar_suite_testes():
    print("=" * 60)
    print("      SIMULADOR DE FIREWALL - SUÍTE DE TESTES E VALIDAÇÃO      ")
    print("=" * 60)

    # -------------------------------------------------------------------------
    # CENÁRIO 1: Inserção Automática e Validação de Consistência
    # -------------------------------------------------------------------------
    print("\n[>] CENÁRIO 1: Construindo Árvore AVL e testando Auto-Balanceamento...")
    tree = AvlRouterTree()

    # Elementos que forçam rotações na inserção sequencial
    regras_id = [50, 25, 75, 15, 35, 60, 90, 10, 20, 30, 40]

    for _id in regras_id:
        # Usando a sua classe real com IPs e prioridade fictícios para o teste
        rule = PacketRule(id_rule=_id, src_ip="192.168.1.10", dst_ip="10.0.0.1", priority=1)
        tree.insert_rule(rule)

    print(f"[+] {len(regras_id)} Regras de pacotes inseridas no motor do Firewall.")

    # Chamando o validador dinâmico
    esta_valida = AVLValidator.validate(tree.root)

    print(f"[*] Executando AVLValidator no chassi da árvore...")
    if esta_valida:
        print("     [STATUS: SUCESSO] A árvore manteve a propriedade AVL (|B| <= 1).")
    else:
        print("     [STATUS: FALHA] A árvore violou as regras de balanceamento.")

    # -------------------------------------------------------------------------
    # CENÁRIO 2: Teste de Integridade de Perímetro (Detector de Anomalias)
    # -------------------------------------------------------------------------
    print("\n[>] CENÁRIO 2: Simulando ataque/injeção manual de nós (Desbalanceamento)...")
    if tree.root and tree.root.left and tree.root.left.left:
        atual = tree.root.left.left

        # Injeta nós burlados diretamente na referência do ponteiro, sem passar pelo algoritmo
        for i in range(1, 6):
            bypassed_rule = PacketRule(id_rule=5 - i, src_ip="10.0.0.5", dst_ip="182.16.0.1", priority=5)
            atual.left = AVLNode(bypassed_rule)
            atual = atual.left

        print("[!] Nós maliciosos inseridos ignorando a lógica de rotação.")

        # O validador precisa pegar essa alteração clandestina
        detectou_erro = not AVLValidator.validate(tree.root)

        print(f"[*] Executando AVLValidator para varredura de integridade...")
        if detectou_erro:
            print("     [STATUS: SUCESSO] Validador detectou a quebra de balanceamento com sucesso!")
        else:
            print("     [STATUS: FALHA] O validador falhou e deixou passar uma árvore corrompida.")

    print("\n" + "=" * 60)
    print("             FIM DA SUÍTE DE TESTES DA ESTRUTURA AVL            ")
    print("=" * 60)


if __name__ == "__main__":
    executar_suite_testes()