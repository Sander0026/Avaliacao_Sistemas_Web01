import json
import random
import uuid
from faker import Faker

# Cria uma instância do Faker configurada para o idioma português do Brasil
# Isso permite gerar dados mais localizados.
faker = Faker('pt_BR')

# Definição da Função Principal

def enviar_notificacao(dados_do_status):
    """
    Responsabilidade: Receber os dados do status de um pedido, simular o envio de um
    e-mail de notificação para o cliente e retornar um relatório da operação em formato JSON.
    """
    # Extrair e Validar os Dados de Entrada 

    # Extrai as informações essenciais do dicionário de entrada.
    # O método get é uma forma segura de acessar um valor, pois retorna None
    # se a chave não existir, em vez de causar um erro que quebraria a execução.
    status = dados_do_status.get('status')
    email_cliente = dados_do_status.get('email_cliente')
    pedido_id = dados_do_status.get('pedido_id')

    # Valida se todas as informações mínimas para enviar a notificação foram recebidas.
    # A função all retorna True apenas se todos os itens na lista forem verdadeiros 
    if not all([status, email_cliente, pedido_id]):
        print("AVISO: Notificação recebida com dados incompletos. Não é possível enviar e-mail.")

        # Cria um dicionário de resposta padronizado para o caso de falha na validação.
        resultado_operacao = {
            "status_envio": "FALHA_DADOS_INCOMPLETOS",
            "mensagem": "Dados insuficientes para enviar a notificação.",
            "pedido_id": pedido_id, 
            "destinatario": email_cliente
        }
        # Converte o dicionário de erro em uma string JSON e encerra a função imediatamente.
        return json.dumps(resultado_operacao, indent=4)

    # Simular o Envio do E-mail com Base no Status 

    # A estrutura condicional decide qual ação tomar com base no status do pedido.
    if status == 'SUCESSO':
        # Monta o conteúdo do e-mail para um pedido bem-sucedido.
        assunto = f"Seu pedido {pedido_id} foi aprovado!"
        corpo_email = f"""
        Olá!

        Ótimas notícias! O pagamento do seu pedido {pedido_id} foi confirmado e ele já está sendo preparado para envio.

        Obrigado por comprar conosco!
        """
        # Imprime no console para simular o envio real do e-mail.
        print(f"SIMULANDO ENVIO DE E-MAIL")
        print(f"PARA: {email_cliente}")
        print(f"ASSUNTO: {assunto}")
        print(corpo_email)
        print("---------------------------------")

        # Define o dicionário de resultado para registrar que a operação foi bem-sucedida.
        resultado_operacao = {
            "status_envio": "ENVIADA",
            "mensagem": f"Notificação de SUCESSO enviada para {email_cliente}.",
            "pedido_id": pedido_id,
            "destinatario": email_cliente
        }

    elif status == 'FALHA':
        # Monta o conteúdo do e-mail para um pedido com falha no pagamento.
        assunto = f"Problema no pagamento do seu pedido {pedido_id}"
        corpo_email = f"""
        Olá,

        Infelizmente, ocorreu um problema ao processar o pagamento do seu pedido {pedido_id}.
        Por favor, verifique os dados do seu cartão ou tente outra forma de pagamento.

        Qualquer dúvida, entre em contato com nosso suporte.
        """
        # Simula o envio do e-mail de falha.
        print(f"SIMULANDO ENVIO DE E-MAIL")
        print(f"PARA: {email_cliente}")
        print(f"ASSUNTO: {assunto}")
        print(corpo_email)
        print("---------------------------------")

        # Define o dicionário de resultado para registrar o envio da notificação de falha.
        resultado_operacao = {
            "status_envio": "ENVIADA",
            "mensagem": f"Notificação de FALHA enviada para {email_cliente}.",
            "pedido_id": pedido_id,
            "destinatario": email_cliente
        }

    else: # Este bloco captura qualquer outro status que não seja 'SUCESSO' ou 'FALHA'.
        print(f"INFO: Status '{status}' do pedido '{pedido_id}' não requer notificação por e-mail.")

        # Define o dicionário de resultado para status que não geram uma ação de envio.
        resultado_operacao = {
            "status_envio": "NAO_APLICAVEL",
            "mensagem": f"O status '{status}' não requer notificação por e-mail.",
            "pedido_id": pedido_id,
            "destinatario": email_cliente
        }

    # Retornar o Relatório da Operação como JSON

    # Converte o dicionário 'resultado_operacao' (definido em um dos blocos acima) em uma string JSON.
    # O argumento 'indent=4' formata a string com 4 espaços de indentação para torná-la legível.
    return json.dumps(resultado_operacao, indent=4)


# Bloco de Execução Principal para Teste
# A condição 'if __name__ == '__main__':' garante que o código abaixo
# só será executado quando o script for rodado diretamente (e não quando importado).
if __name__ == '__main__':

    # Prepara os dados de teste.
    # random.choice() seleciona aleatoriamente um item da lista para testar diferentes lógicas da função.
    status = random.choice(['SUCESSO', 'FALHA', 'PROCESSANDO'])
    detalhes = ""
    if status == 'FALHA':
        detalhes = "Cartão recusado."
    else:
        detalhes = "Pagamento aprovado."

    # Cria um dicionário de 'notificacao' para simular uma mensagem que viria de um serviço como Amazon SNS.
    # Usa Faker e UUID para gerar dados de teste realistas e únicos a cada execução.
    notificacao = {
        "pedido_id": str(uuid.uuid4()),
        "status": status,
        "detalhes": detalhes,
        "id_produto": Faker().random_int(min=1, max=1000),
        "quantidade": Faker().random_int(min=1, max=1000),
        "email_cliente": Faker().email()
    }

    print("Testando o microserviço 'enviar_notificacao'")

    # Chama a função principal, passando a notificação de teste.
    # A variável 'resultado' armazena o valor retornado pela função, que é a string JSON.
    print("\n[Processando notificação...]")
    resultado = enviar_notificacao(notificacao)

    # Imprime o JSON retornado pela função para que possamos verificar se a saída está correta.
    print("\n[Resultado da Operação de Notificação (JSON Retornado)]")
    print(resultado)