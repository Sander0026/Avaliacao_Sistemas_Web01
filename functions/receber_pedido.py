# --- Importação de Bibliotecas ---
import json
import uuid
from queue import Queue
from faker import Faker

# --- Configuração Inicial ---

# Cria uma instância do Faker configurada para o idioma português do Brasil ('pt_BR').
# Isso permite gerar dados mais localizados, como nomes e endereços brasileiros.
faker = Faker('pt_BR')

# Cria uma instância global da classe Queue para simular a fila de pedidos.
# Em uma aplicação real, aqui estaria a conexão com o serviço SQS da AWS.
fila_de_pedidos = Queue()

# --- Definição da Função Principal ---

def receber_pedido(dados_do_pedido, fila):
    """
    Responsabilidade: Receber os dados de um pedido, validar, enriquecer 
    e enviá-lo para uma fila para processamento assíncrono.
    Simula o comportamento de um endpoint de API (como um API Gateway + Lambda).
    """
    # Validação dos dados de entrada.
    # Define uma lista com os nomes das chaves que são obrigatórias no dicionário do pedido.
    campos_obrigatorios = ['id_produto', 'quantidade', 'email_cliente']
    
    # Itera sobre cada campo obrigatório para verificar sua existência.
    for campo in campos_obrigatorios:
        # Se um campo da lista não estiver presente no dicionário 'dados_do_pedido'...
        if campo not in dados_do_pedido:
            # ... imprime uma mensagem de erro no console para fins de log.
            print(f"Erro de validação: O campo '{campo}' é obrigatório.")
            
            # Cria um dicionário de erro padronizado para ser retornado como resposta.
            erro_json = {
                "message": f"Erro de validação: O campo '{campo}' é obrigatório.",
                "pedido_recebido": dados_do_pedido  # Inclui os dados recebidos para facilitar a depuração.
            }
            # Converte o dicionário de erro para uma string JSON e interrompe a execução da função.
            return json.dumps(erro_json, indent=4)

    
    # Enriquecimento do pedido.
    # Adiciona um ID de pedido único ao dicionário. `uuid.uuid4()` gera um ID aleatório.
    # `str()` converte o objeto UUID para uma string, que é um formato mais comum para serialização.
    dados_do_pedido['pedido_id'] = str(uuid.uuid4())

    # Envio para a fila.
    # O método `.put()` adiciona o dicionário completo do pedido à fila para ser processado posteriormente.
    fila.put(dados_do_pedido)
    print(f"Pedido {dados_do_pedido['pedido_id']} foi adicionado à fila com sucesso.")
    
    # Montagem da resposta de sucesso.
    # Cria um dicionário para a resposta que será enviada de volta ao cliente (a API).
    # Esta resposta confirma que o pedido foi recebido e está na fila.
    resposta_api = {
        'message': 'Pedido recebido e em processamento.',
        'pedido_id': dados_do_pedido['pedido_id']
    }
    
    # Converte o dicionário de resposta em uma string JSON formatada e a retorna.
    # O argumento 'indent=4' formata a string JSON com 4 espaços de indentação,
    # tornando-a mais legível para humanos (útil para logs e debugging).
    # Este é o retorno final da função em caso de sucesso.
    return json.dumps(resposta_api, indent=4)


# --- Funções Auxiliares para Testes ---

def criar_pedido():
    """
    Função auxiliar que usa a biblioteca Faker para gerar um dicionário
    de pedido com dados aleatórios, simulando o "payload" de uma requisição de API.
    """
    pedido = {
        "id_produto" : Faker().random_int(min=1, max=1000),
        "quantidade" : Faker().random_int(min=1, max=1000),
        "email_cliente" : Faker().email(),
    }
    return pedido

# --- Bloco de Execução Principal ---

# A condição 'if __name__ == '__main__':' garante que o código dentro deste bloco
# só será executado quando o script for rodado diretamente.
if __name__ == '__main__':
    
    # O bloco 'try...except' é usado para capturar e tratar possíveis erros
    # que possam ocorrer durante a execução do teste, evitando que o programa quebre.
    try:
        # Chama a função auxiliar para gerar um novo pedido.
        payload = criar_pedido()
        
        print("--- [Simulação] Gerando e processando um novo pedido ---")
        print("Dados do Pedido Gerado:", payload)
        
        # Chama a função principal 'receber_pedido', passando o payload gerado e a fila.
        # A variável 'resultado' armazena o retorno da função, que é uma string JSON.
        resultado = receber_pedido(payload, fila_de_pedidos)
        
        print("\n--- [Simulação de Resposta da API] ---")
        # Verifica se a variável 'resultado' não é nula ou vazia.
        if resultado:
            # Imprime a resposta da API, que já está formatada como uma string JSON.
            print("Resposta da API (string JSON):")
            print(resultado)
            
            # O método .qsize() retorna o número atual de itens na fila.
            print(f"\nStatus da Fila: {fila_de_pedidos.qsize()} pedido(s) aguardando processamento.")
            
        else:
            # Esta mensagem seria exibida se a função retornasse None.
            print("Falha ao processar o pedido. Verifique os erros de validação.")

    # Se ocorrer qualquer erro (Exceção) dentro do bloco 'try'...
    except Exception as e:
        # ... o programa captura o erro na variável 'e' e imprime uma mensagem amigável.
        print(f"Ocorreu um erro inesperado durante a execução: {e}")