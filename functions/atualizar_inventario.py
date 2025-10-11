import json
import uuid
import random
from   datetime import datetime

# Logica de atualização de inventario
def atualizar_inventario(dados_do_status):

    status     = dados_do_status.get('status', 'DESCONHECIDO')
    pedido_id  = dados_do_status.get('pedido_id', 'N/A')
    produto_id = dados_do_status.get('id_produto', 'N/A')
    quantidade = dados_do_status.get('quantidade', 0)
    timestamp  = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    if status == "SUCESSO":
        log_inventario = {
            "timestamp": timestamp,
            "nivel": "INFO",
            "servico": "atualizar_inventario",
            "mensagem": f"Dando baixa de {quantidade} unidade(s) do produto '{produto_id}' no inventario.",
            "pedido_id": pedido_id
        }
        print(json.dumps(log_inventario, indent=4))
        return True
    else:
        print(f"INFO: Pedido '{pedido_id}' com status '{status}'. Nenhuma atualização no inventário necessária.")
        return False


# Simulação para apresentação
if __name__ == "__main__":
    print("Testando o microserviço 'atualizar_inventario'\n")

    # Simular 5 pedidos recebendo diferentes status
    for _ in range(5):
        status = random.choice(["SUCESSO", "FALHA"])
        detalhes = "Pagamento aprovado" if status == "SUCESSO" else "Erro no pagamento"

        pedido = {
            "pedido_id": str(uuid.uuid4()),
            "status": status,
            "detalhes": detalhes,
            "id_produto": f"Produto-{random.randint(100, 999)}",
            "quantidade": random.randint(1, 5)
        }

        print("\n[Processando notificação]")
        atualizar_inventario(pedido)
