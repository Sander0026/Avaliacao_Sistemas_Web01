
# Simulação de Arquitetura de Microserviços para E-commerce

## Introdução

Este projeto simula uma arquitetura de microserviços baseada em eventos para o processamento de pedidos em um sistema de e-commerce. O objetivo é demonstrar de forma prática e simplificada como diferentes serviços podem interagir de maneira assíncrona, utilizando conceitos comuns em ambientes de nuvem como a AWS.

Cada arquivo Python no diretório `functions/` representa um "microserviço" (simulado como uma função), que é responsável por uma etapa específica do fluxo de processamento de um pedido.

## Fluxo do Projeto

O fluxo de processamento de um pedido é orquestrado da seguinte maneira:

1.  **Recebimento do Pedido (`receber_pedido.py`)**
    *   Um novo pedido é recebido com os dados do produto, quantidade e e-mail do cliente.
    *   A função valida os dados, enriquece o pedido com um ID único (`pedido_id`) e o adiciona a uma fila de processamento.
    *   **Simulação AWS:** Representa um *API Gateway* que recebe a requisição e invoca uma função *Lambda* que, por sua vez, envia uma mensagem para uma fila *SQS (Simple Queue Service)*.

2.  **Processamento do Pagamento (`processar_pagamento.py`)**
    *   Esta função consome o pedido da fila para processar o pagamento.
    *   Ela simula a comunicação com um gateway de pagamento, resultando em um status de "SUCESSO" ou "FALHA".
    *   O resultado do processamento (com o status do pagamento) é então publicado para que outros serviços possam reagir.
    *   **Simulação AWS:** Representa uma função *Lambda* que é acionada por mensagens na fila *SQS*. Após o processamento, ela publica o resultado em um tópico *SNS (Simple Notification Service)*.

3.  **Reação ao Status do Pagamento**
    *   Com base no status do pagamento publicado, diferentes microserviços são acionados para dar continuidade ao fluxo.

    *   **Se o pagamento for um SUCESSO:**
        *   **Atualização de Inventário (`atualizar_inventario.py`):** A função é acionada para dar baixa no estoque do produto vendido.
        *   **Notificação de Sucesso (`enviar_notificacao.py`):** Uma notificação por e-mail é enviada ao cliente confirmando a aprovação do pedido.

    *   **Se o pagamento for uma FALHA:**
        *   **Cancelamento do Pedido (`cancelar_pedido.py`):** O pedido é marcado como cancelado no sistema.
        *   **Notificação de Falha (`enviar_notificacao.py`):** Uma notificação por e-mail é enviada ao cliente informando sobre a falha no pagamento.

4.  **Registro de Logs (`registrar_log.py`)**
    *   Ao longo de todo o processo, os serviços podem registrar logs de suas operações (embora o arquivo `registrar_log.py` no projeto atual esteja duplicado, a ideia é que ele centralize ou padronize a forma como os logs são capturados).
    *   **Simulação AWS:** Representa o serviço *CloudWatch*, que centraliza os logs de todas as funções *Lambda* e outros serviços da AWS, permitindo monitoramento e depuração.

## Conclusão

Este projeto oferece uma visão simplificada, porém técnica, de uma arquitetura de microserviços orientada a eventos. Ele demonstra como a separação de responsabilidades e a comunicação assíncrona permitem construir sistemas mais escaláveis, resilientes e fáceis de manter.

Cada "microserviço" opera de forma independente, reagindo a eventos específicos, o que é um padrão de arquitetura fundamental para aplicações de nuvem modernas.
