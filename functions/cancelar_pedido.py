import json
import uuid
import random
from datetime import datetime
from zoneinfo import ZoneInfo

# lógica de um microserviço responsável por cancelar pedidos com base no status recebido de outro serviço
def cancelar_pedido(dados_do_status):

    # informações principais do pedido recebido
    status               = dados_do_status.get('status', 'DESCONHECIDO')
    pedido_id            = dados_do_status.get('pedido_id', 'N/A')
    detalhes             = dados_do_status.get('detalhes', 'Sem detalhes')
    horario_cancelamento = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d-%m-%Y %H:%M:%S")

    # Verifica se o status do pedido indica falha, nesse caso o microserviço deve iniciar o processo de cancelamento.
    if status == "FALHA":
        log_cancelamento = {
            "Horario do cancelamento": horario_cancelamento,
            "Nivel": "Informativo",
            "Servico": "cancelar_pedido",
            "Mensagem": f"Iniciando processo de cancelamento para o pedido '{pedido_id}'.",
            "Motivo": detalhes
        }

        # O log é impresso em JSON que vai simular o envio a um sistema de monitoramento.
        print(json.dumps(log_cancelamento, indent=4))
        return True # retornando true indica que o processo de cancelamento foi iniciado
    else:
        print(f"INFO: Pedido '{pedido_id}' com status '{status}'. Nenhuma ação de cancelamento necessaria.")
        return False # retornando false indica que o cancelamento não é necessario


# Simulação para apresentação
if __name__ == "__main__":
    print("Teste do microserviço 'cancelar_pedido'\n")

    # Simular 5 pedidos recebendo diferentes status
    for _ in range(5):
        status   = random.choice(["SUCESSO", "FALHA"])
        detalhes = "Pagamento recusado" if status == "FALHA" else "Pagamento aprovado"

        pedido = {
            "pedido_id": str(uuid.uuid4()), # padrão usado para gerar identificadores
            "status": status,
            "detalhes": detalhes
        }

        print("\n[Processando notificação]")
        cancelar_pedido(pedido)
