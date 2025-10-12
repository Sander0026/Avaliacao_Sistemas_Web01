# --- Importação de Bibliotecas ---
import json
import uuid
import random
from queue import Queue
from faker import Faker


# Cria uma instância da classe Queue para simular a fila de pedidos do SQS.
# Pedidos serão adicionados a esta fila antes de serem processados.
fila_de_pedidos = Queue()

# --- Definição da Função Principal ---

def processar_pagamento(dados_do_pedido):
    """
    Responsabilidade: Simular o processamento de um pagamento de um pedido.
    Esta função recebe os dados de um pedido, simula uma tentativa de pagamento
    e retorna o resultado formatado como uma string JSON.
    """
    # Imprime uma mensagem informativa no console para logging e depuração.
    # O método .get('chave') é uma forma segura de acessar um valor em um dicionário,
    # pois retorna None se a chave não existir, em vez de gerar um erro.
    print(f"INFO: Processando pagamento para o pedido '{dados_do_pedido.get('pedido_id')}'...")

    # Simulação da lógica de um gateway de pagamento.
    # random.choice() seleciona aleatoriamente um item de uma lista.
    # Neste caso, simula que um pagamento pode ser aprovado ('SUCESSO') ou negado ('FALHA').
    status_pagamento = random.choice(['SUCESSO', 'FALHA'])
    
    # Estrutura condicional para definir os detalhes da transação com base no status.
    if status_pagamento == 'SUCESSO':
        # Define a mensagem de detalhe para um pagamento bem-sucedido.
        detalhes = "Pagamento aprovado com sucesso."
        print(f"INFO: Pagamento do pedido '{dados_do_pedido.get('pedido_id')}' APROVADO.")
    else:
        # Define a mensagem de detalhe para um pagamento que falhou.
        detalhes = "Falha no pagamento: saldo insuficiente."
        print(f"INFO: Pagamento do pedido '{dados_do_pedido.get('pedido_id')}' RECUSADO.")

    # Cria um dicionário Python para estruturar a mensagem de status do pagamento.
    # Esta mensagem contém todas as informações relevantes sobre o resultado da transação.
    mensagem_de_status = {
        "pedido_id": dados_do_pedido.get('pedido_id'),
        "status": status_pagamento,
        "detalhes": detalhes,
        "id_produto": dados_do_pedido.get('id_produto'),
        "quantidade": dados_do_pedido.get('quantidade'),
        "email_cliente": dados_do_pedido.get('email_cliente')
    }
    
    # Converte o dicionário 'mensagem_de_status' em uma string no formato JSON.
    # O argumento 'indent=4' formata a string JSON com 4 espaços de indentação,
    # tornando-a mais legível para humanos (útil para logs e debugging).
    # Esta string JSON é o valor que a função retorna.
    return json.dumps(mensagem_de_status, indent=4)


# --- Bloco de Execução Principal ---

# A condição 'if __name__ == '__main__':' garante que o código dentro deste bloco
# só será executado quando o script for rodado diretamente (e não quando for importado por outro script).
# É o local padrão para colocar testes e demonstrações da funcionalidade do script.
if __name__ == '__main__':
    
          
    # Cria um dicionário para representar um pedido de exemplo.
    # Os dados são gerados usando 'uuid' e 'Faker' para serem únicos e realistas a cada execução.
    pedido_exemplo = {
        "pedido_id": str(uuid.uuid4()),
        "id_produto": Faker().random_int(min=1, max=1000),
        "quantidade": Faker().random_int(min=1, max=1000),
        "email_cliente": Faker().email()
    }
    # Adiciona o pedido de exemplo à fila usando o método .put().
    fila_de_pedidos.put(pedido_exemplo)
    
    print("--- Testando o microserviço 'processar_pagamento' ---")
    # .qsize() retorna o número de itens atualmente na fila.
    print(f"Status da Fila de Pedidos: {fila_de_pedidos.qsize()} pedido(s) aguardando.")

    # Verifica se a fila não está vazia antes de tentar consumir um item.
    # Isso evita erros caso o script seja executado sem nenhum pedido na fila.
    if not fila_de_pedidos.empty():
        # Retira o próximo item da fila usando o método .get().
        # Este é o comportamento de um consumidor (como uma função Lambda) lendo uma mensagem do SQS.
        pedido_para_processar = fila_de_pedidos.get()
        print(f"\n[Cenário 1: Consumindo pedido da fila SQS]")
        
        # Chama a função principal 'processar_pagamento', passando o pedido consumido da fila.
        # A variável 'resultado_do_pagamento' armazena o valor retornado, que é uma string JSON.
        resultado_do_pagamento = processar_pagamento(pedido_para_processar)
        
        # Simula a próxima etapa da arquitetura: publicar o resultado em um tópico do Amazon SNS.
        print("\n--- [Simulação de Publicação no Tópico SNS] ---")
        print("Mensagem a ser publicada (string JSON):")
        
        # Imprime o resultado diretamente. Como a função já retorna uma string JSON formatada,
        # não é necessário usar json.dumps() novamente aqui.
        print(resultado_do_pagamento)
        
    else:
        # Mensagem exibida caso a fila esteja vazia no início da execução.
        print("\nFila de pedidos vazia. Nenhum item para processar.")