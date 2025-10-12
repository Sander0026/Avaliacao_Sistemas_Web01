# --- Importação de Bibliotecas ---
import json
import random
import uuid
from faker import Faker

# Instância única do gerador de dados falsos
fake = Faker()

def enviar_notificacao(dados_do_status):
    """
    Responsabilidade:
    Receber a mensagem do SNS, verificar o status e simular o envio de um
    e-mail para o cliente informando o resultado do processamento do pedido.
    """
    # Extrai informações essenciais
    status = dados_do_status.get('status')
    email_cliente = dados_do_status.get('email_cliente')
    pedido_id = dados_do_status.get('pedido_id')

    # Verifica se os dados mínimos foram fornecidos
    if not all([status, email_cliente, pedido_id]):
        print("[AVISO] Dados incompletos na notificação. E-mail não será enviado.")
        return

    # Monta e simula o envio do e-mail
    print("\n--- SIMULANDO ENVIO DE E-MAIL ---")
    print(f"PARA: {email_cliente}")

    if status == 'SUCESSO':
        assunto = f"Seu pedido {pedido_id} foi aprovado!"
        corpo_email = f"""
Olá!

Ótimas notícias! O pagamento do seu pedido {pedido_id} foi confirmado e ele já está sendo preparado para envio.

Obrigado por comprar conosco!
        """
    elif status == 'FALHA':
        assunto = f"Problema no pagamento do seu pedido {pedido_id}"
        corpo_email = f"""
Olá,

Infelizmente, ocorreu um problema ao processar o pagamento do seu pedido {pedido_id}.
Por favor, verifique os dados do seu cartão ou tente outra forma de pagamento.

Qualquer dúvida, entre em contato com nosso suporte.
        """
    else:
        print(f"[INFO] Status '{status}' do pedido '{pedido_id}' não requer notificação por e-mail.")
        return

    # Imprime o conteúdo simulado do e-mail
    print(f"ASSUNTO: {assunto}")
    print(corpo_email)
    print("-----------------------------------")


# --- Execução Principal ---
if __name__ == '__main__':
    # Define aleatoriamente o status do pedido
    status = random.choice(['SUCESSO', 'FALHA'])

    detalhes = "Pagamento aprovado." if status == 'SUCESSO' else "Cartão recusado."

    # Simula uma notificação com dados aleatórios
    notificacao = {
        "pedido_id": str(uuid.uuid4()),
        "status": status,
        "detalhes": detalhes,
        "id_produto": fake.random_int(min=1, max=1000),
        "quantidade": fake.random_int(min=1, max=5),
        "email_cliente": fake.email()
    }

    print("\n=== Testando o microserviço 'enviar_notificacao' ===")
    print("\n[Recebendo notificação SNS simulada]")
    enviar_notificacao(notificacao)
