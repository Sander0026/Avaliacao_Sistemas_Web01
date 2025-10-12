import json
import random
import uuid
from datetime import datetime

from faker import Faker

# Instância do gerador de dados falsos
fake = Faker()


def registrar_log(dados_do_status: dict) -> None:
    """
    Função responsável por registrar logs de auditoria a partir de mensagens recebidas.

    Parâmetros:
        dados_do_status (dict): Dicionário contendo informações sobre o pedido.
    """
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    pedido_id = dados_do_status.get('pedido_id', 'N/A')
    status = dados_do_status.get('status', 'DESCONHECIDO')
    detalhes = dados_do_status.get('detalhes', 'Sem detalhes')

    log_estruturado = {
        "timestamp": timestamp,
        "nivel": "AUDITORIA",
        "mensagem": f"Evento de processamento do pedido '{pedido_id}' recebido.",
        "dados_do_evento": {
            "pedido_id": pedido_id,
            "status_final": status,
            "detalhes_transacao": detalhes,
            "id_produto": dados_do_status.get('id_produto'),
            "quantidade": dados_do_status.get('quantidade'),
            "email_cliente": dados_do_status.get('email_cliente')
        }
    }

    print(json.dumps(log_estruturado, indent=4))


# --- Bloco Principal ---
if __name__ == '__main__':

    status = random.choice(['SUCESSO', 'FALHA'])
    detalhes = "Pagamento aprovado via PIX." if status == 'SUCESSO' else "Limite do cartão excedido."

    notificacao = {
        "pedido_id": str(uuid.uuid4()),
        "status": status,
        "detalhes": detalhes,
        "id_produto": fake.random_int(min=1, max=1000),
        "quantidade": fake.random_int(min=1, max=1000),
        "email_cliente": fake.email()
    }

    print("--- Testando o microserviço 'registrar_log' ---")
    print("\n[Registrando log]")
    registrar_log(notificacao)
