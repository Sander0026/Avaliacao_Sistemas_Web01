import json
import uuid
from queue import Queue
from faker import Faker

faker = Faker('pt_BR')

# Criar uma instância da fila SQS.
fila_de_pedidos = Queue()

def receber_pedido(dados_do_pedido, fila):
    """
    Responsabilidade: Receber os dados do pedido, fazer uma validação inicial,
    e enviar o pedido como uma mensagem para a fila.
    Retorna um dicionário com a mensagem de sucesso para a API.
    """
    # Validar se os campos obrigatórios existem no dicionário de entrada.
    campos_obrigatorios = ['id_produto', 'quantidade', 'email_cliente']
    for campo in campos_obrigatorios:
        if campo not in dados_do_pedido:
            print(f"Erro de validação: O campo '{campo}' é obrigatório.")
            return None # Retorna None em caso de falha na validação

   
    # Garante que cada pedido tenha um identificador único.
    dados_do_pedido['pedido_id'] = str(uuid.uuid4())

    # Colocar a mensagem (pedido) na fila.
    fila.put(dados_do_pedido)
    print(f"Pedido {dados_do_pedido['pedido_id']} foi adicionado à fila com sucesso.")
    
    # Montar a resposta de sucesso que seria retornada pela API.
    resposta_api = {
        'message': 'Pedido recebido e em processamento.',
        'pedido_id': dados_do_pedido['pedido_id']
    }
    
    return resposta_api


#-----------Testes e Simulações-----------#
def criar_pedido():
    """
    Função auxiliar para criar um pedido de exemplo.
    """
    pedido = {
        "id_produto" : Faker().random_int(min=1, max=1000),
        "quantidade" : Faker().random_int(min=1, max=1000),
        "email_cliente" : Faker().email(),
    }
    return pedido

# --- Bloco de Execução Principal ---
if __name__ == '__main__':
    
    try:
        # Criamos um pedido falso usando a função.
        payload = criar_pedido()
        
        
        print("--- [Simulação] Gerando e processando um novo pedido ---")
        print("Dados do Pedido Gerado:", payload)
        
        # Chama a função para validar e colocar o pedido na fila em memória.
        resultado = receber_pedido(payload, fila_de_pedidos)
        
        print("\n--- [Simulação de Resposta da API] ---")
        if resultado:
            print(json.dumps(resultado, indent=4))
            print(f"\nStatus da Fila: {fila_de_pedidos.qsize()} pedido(s) aguardando processamento.")
        else:
            print("Falha ao processar o pedido. Verifique os erros de validação.")

    except Exception as e:
        print(f"Ocorreu um erro inesperado durante a execução: {e}")

