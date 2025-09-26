# Chatbot de Qualificação de Leads para WhatsApp com IA

Este projeto é um assistente virtual (chatbot) que automatiza o processo de qualificação de leads através do WhatsApp. Utilizando a API da OpenAI (GPT-4o/GPT-3.5), o bot é capaz de manter uma conversa natural com o usuário, extrair informações relevantes e decidir se o lead está qualificado para ser passado para a equipe de vendas (Hunters), seguindo a lógica de negócio definida em um fluxograma.

## Fluxo de Qualificação

O comportamento do bot é baseado no seguinte fluxo de processo:

*(Nota: Substitua o link acima pelo caminho para a imagem do seu fluxograma, se desejar)*

As principais etapas e decisões do fluxo são:

1.  **Entrada do Lead**: Um novo lead entra em contato via WhatsApp.
2.  [cite\_start]**Qualificação com IA**: O bot inicia uma conversa para coletar dados com base nas perguntas de qualificação[cite: 1].
3.  [cite\_start]**Análise de Perfil**: A IA analisa se o lead pertence ao ramo de atuação desejado (ex: segurança eletrônica)[cite: 1].
4.  [cite\_start]**Análise de Maturidade**: O sistema verifica se o lead é considerado "maduro" (por exemplo, com base no número de colaboradores) para decidir se avança ou entra em um fluxo de nutrição[cite: 1].
5.  **Decisão**: Com base nas respostas, o lead é classificado como:
      * **Qualificado**: Pronto para ser abordado por um vendedor (Hunter).
      * [cite\_start]**Desqualificado/Nutrição**: Não possui o perfil ideal no momento e pode receber materiais de marketing para amadurecimento[cite: 1].

## Features

  * **Integração com a API do WhatsApp Business**: Recebe e envia mensagens em tempo real.
  * **Processamento de Linguagem Natural (PNL)**: Utiliza os modelos da OpenAI para entender as respostas dos usuários de forma flexível e extrair dados estruturados.
  * **Gerenciamento de Estado de Conversa**: O bot sabe quais perguntas já foram feitas e o que precisa perguntar a seguir para completar a qualificação.
  * **Lógica de Negócio Customizável**: As regras de qualificação e as perguntas podem ser facilmente ajustadas no código.
  * **Tratamento de Erros**: Possui uma lógica de fallback para continuar a conversa mesmo que a API da OpenAI falhe.

## Tecnologias Utilizadas

  * **Backend**: Python 3
  * **Framework Web**: Flask
  * **Inteligência Artificial**: OpenAI API (GPT-4o)
  * **Gerenciamento de Ambiente**: python-dotenv

## Pré-requisitos

Antes de começar, garanta que você tenha:

  * Python 3.8 ou superior.
  * Uma conta na **Plataforma da Meta for Developers** com um aplicativo configurado para a API do WhatsApp Business.
  * Uma conta na **OpenAI** com um método de pagamento configurado para acesso à API.
  * **ngrok** para expor seu ambiente de desenvolvimento local à internet e testar o webhook.

## Instalação e Configuração

Siga os passos abaixo para configurar e executar o projeto.

**1. Clone o Repositório**

```bash
git clone <url-do-seu-repositorio>
cd <nome-do-repositorio>
```

**2. Crie um Ambiente Virtual e Ative-o**

```bash
python3 -m venv venv
source venv/bin/activate
# No Windows, use: venv\Scripts\activate
```

**3. Instale as Dependências**
Crie um arquivo `requirements.txt` com o seguinte conteúdo:

```txt
flask
openai
python-dotenv
requests
```

E instale as dependências:

```bash
pip install -r requirements.txt
```

**4. Configure as Variáveis de Ambiente**
Crie um arquivo chamado `.env` na raiz do projeto e adicione as seguintes chaves. **Nunca compartilhe este arquivo.**

```env
# Token de verificação do Webhook (crie qualquer string segura)
VERIFY_TOKEN="SEU_TOKEN_SECRETO_PARA_O_WEBHOOK"

# Credenciais da API do WhatsApp (obtidas no painel da Meta)
WHATSAPP_API_TOKEN="SEU_TOKEN_DA_API_DO_WHATSAPP"
WHATSAPP_PHONE_NUMBER_ID="ID_DO_SEU_NUMERO_DE_TELEFONE"

# Chave da API da OpenAI (obtida no painel da OpenAI)
OPENAI_API_KEY="sk-SUA_CHAVE_SECRETA_DA_OPENAI"
```

## Executando a Aplicação

**1. Inicie o Servidor Flask**

```bash
python3 app.py
```

O servidor estará rodando localmente em `http://127.0.0.1:5000`.

**2. Exponha seu Servidor com o ngrok**
Em um novo terminal, inicie o ngrok para que a API do WhatsApp possa se comunicar com sua aplicação local.

```bash
ngrok http 5000
```

O ngrok irá gerar uma URL pública HTTPS, como `https://xxxxxxxxxxxx.ngrok-free.app`. Copie esta URL.

**3. Configure o Webhook no Painel da Meta**

  - Vá até o painel de controle do seu aplicativo na plataforma da Meta.
  - Navegue até a seção "WhatsApp" \> "Configuração".
  - No campo "URL de Retorno de Chamada" do Webhook, cole a URL gerada pelo ngrok e adicione `/webhook` no final (ex: `https://xxxxxxxxxxxx.ngrok-free.app/webhook`).
  - No campo "Token de Verificação", insira o mesmo valor que você definiu para `VERIFY_TOKEN` no seu arquivo `.env`.
  - Salve e assine os eventos do webhook, principalmente o evento `messages`.

Agora, qualquer mensagem enviada para o seu número do WhatsApp será recebida pela sua aplicação Flask, processada pela IA e respondida automaticamente.

## Estrutura do Projeto

```
.
├── app.py                # Arquivo principal: Servidor Flask e rota do webhook.
├── flow_manager.py       # Gerencia o estado da conversa e o fluxo de perguntas.
├── nlp_service.py        # Módulo de PNL, responsável por chamar a API da OpenAI.
├── whatsapp_service.py   # Módulo para enviar mensagens via API do WhatsApp.
├── crm_service.py        # (Simulado) Módulo para interagir com um CRM.
├── .env                  # Arquivo para armazenar chaves de API e segredos.
└── requirements.txt      # Lista de dependências Python.
```
