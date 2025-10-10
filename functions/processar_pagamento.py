import json
import uuid
import random
from queue import Queue
from faker import Faker

def processar_pagamento(dados_do_pedido):
    """
    Responsabilidade: Ler o pedido da fila, simular a lógica de um gateway 
    de pagamento e criar uma nova mensagem com o resultado.
    """
    print(f"INFO: Processando pagamento para o pedido '{dados_do_pedido.get('pedido_id')}'...")

    # Simula a lógica de um gateway de pagamento (sorteio aleatório).
    status_pagamento = random.choice(['SUCESSO', 'FALHA'])
    
    # Define detalhes da transação com base no resultado.
    if status_pagamento == 'SUCESSO':
        detalhes = "Pagamento aprovado com sucesso."
        print(f"INFO: Pagamento do pedido '{dados_do_pedido.get('pedido_id')}' APROVADO.")
    else:
        detalhes = "Falha no pagamento: saldo insuficiente."
        print(f"INFO: Pagamento do pedido '{dados_do_pedido.get('pedido_id')}' RECUSADO.")

    # Cria a nova mensagem de status para ser publicada no SNS.
    mensagem_de_status = {
        "pedido_id": dados_do_pedido.get('pedido_id'),
        "status": status_pagamento,
        "detalhes": detalhes,
        "id_produto": dados_do_pedido.get('id_produto'),
        "quantidade": dados_do_pedido.get('quantidade'),
        "email_cliente": dados_do_pedido.get('email_cliente')
    }
    
    return mensagem_de_status

# --- Bloco de Execução Principal ---
if __name__ == '__main__':
    
    # Simulação da "fila_de_pedidos" (SQS) com um pedido aguardando.
    fila_de_pedidos = Queue()
    
    pedido_exemplo = {
        "pedido_id": str(uuid.uuid4()),
        "id_produto": Faker().random_int(min=1, max=1000),
        "quantidade": Faker().random_int(min=1, max=1000),
        "email_cliente": Faker().email()
    }
    fila_de_pedidos.put(pedido_exemplo)
    
    print("--- Testando o microserviço 'processar_pagamento' ---")
    print(f"Status da Fila de Pedidos: {fila_de_pedidos.qsize()} pedido(s) aguardando.")

    # Simula o gatilho da Lambda, lendo o pedido da fila SQS.
    if not fila_de_pedidos.empty():
        pedido_para_processar = fila_de_pedidos.get()
        print(f"\n[Cenário 1: Consumindo pedido da fila SQS]")
        
        # Chama a função principal para processar o pagamento.
        resultado_do_pagamento = processar_pagamento(pedido_para_processar)
        
        # Simula a publicação do resultado no tópico SNS.
        print("\n--- [Simulação de Publicação no Tópico SNS] ---")
        print("Mensagem a ser publicada:")
        print(json.dumps(resultado_do_pagamento, indent=4))
    else:
        print("\nFila de pedidos vazia. Nenhum item para processar.")
