import json
import uuid
import random
from datetime import datetime
from zoneinfo import ZoneInfo  

# lógica de um microserviço que reduz a quantidade de um produto no estoque após uma compra ser finalizada com sucesso.
def atualizar_inventario(dados_do_status):

    # informações principais do status da atualização de inventário
    status     = dados_do_status.get('status', 'DESCONHECIDO')
    pedido_id  = dados_do_status.get('pedido_id', 'N/A')
    produto_id = dados_do_status.get('id_produto', 'N/A')
    quantidade = dados_do_status.get('quantidade', 0)
    timestamp  = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d-%m-%Y %H:%M:%S")

    # Com status sucesso, o microserviço vai atuar iniciando a atualização de inventário
    if status == "SUCESSO":

        # Cria um registro de log no formato JSON
        log_inventario = {
            "timestamp": timestamp,
            "nivel": "INFO",
            "servico": "atualizar_inventario",
            "mensagem": f"Dando baixa de {quantidade} unidade(s) do produto '{produto_id}' no inventário.",
            "pedido_id": pedido_id
        }

        # O log é impresso em JSON para simular o envio a um sistema de atualização de inventário
        print(json.dumps(log_inventario, indent=4))
        return True  # Retorna True indicando que o processo de atualização foi executado
    else:
        print(f"INFO: Pedido '{pedido_id}' com status '{status}'. Nenhuma atualização no inventário necessária.")
        return False  # Retorna False indicando que não há necessidade de atualização


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
