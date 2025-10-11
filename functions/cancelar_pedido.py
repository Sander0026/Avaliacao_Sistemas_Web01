import json
import uuid
import random
from   datetime import datetime

# Logica de cancelamento
def cancelar_pedido(dados_do_status):

    status    = dados_do_status.get('status', 'DESCONHECIDO')
    pedido_id = dados_do_status.get('pedido_id', 'N/A')
    detalhes  = dados_do_status.get('detalhes', 'Sem detalhes')
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    if status == "FALHA":
        log_cancelamento = {
            "timestamp": timestamp,
            "nivel": "INFO",
            "servico": "cancelar_pedido",
            "mensagem": f"Iniciando processo de cancelamento para o pedido '{pedido_id}'.",
            "motivo": detalhes
        }
        print(json.dumps(log_cancelamento, indent=4))
        return True
    else:
        print(f"INFO: Pedido '{pedido_id}' com status '{status}'. Nenhuma ação de cancelamento necessária.")
        return False


# Simulação para apresentação
if __name__ == "__main__":
    print("Testando o microserviço 'cancelar_pedido'\n")

    # Simular 5 pedidos recebendo diferentes status
    for _ in range(5):
        status = random.choice(["SUCESSO", "FALHA"])
        detalhes = "Pagamento recusado" if status == "FALHA" else "Pagamento aprovado"

        pedido = {
            "pedido_id": str(uuid.uuid4()),
            "status": status,
            "detalhes": detalhes
        }

        print("\n[Processando notificação]")
        cancelar_pedido(pedido)
