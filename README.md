bot_wpps

Atendimento ao cliente por WhatsApp com base de dados de peças (consulta e cadastro).
O projeto integra um webhook de WhatsApp (Meta/Business), consulta uma base local (SQLite) de peças e expõe utilitários para cadastro/importação.


✨ Funcionalidades

Recebimento de mensagens via Webhook (WhatsApp Business): roteamento de mensagens e respostas automáticas.

Consulta de peças em base local (SQLite).

Cadastro / carga de peças por script Python.

Camada JS para interação/consumo (ex.: front simples ou utilitário de consulta).

Os nomes dos arquivos indicam: webhook em Python (whatsapp_webhook.py), carga/cadastro de peças (CadastrarPeças.py), utilitário em JS (pecas.js) e base SQLite (pecas_empilhadeira_pronto.db). 
GitHub

📦 Requisitos

Python 3.10+

Node.js 18+ (se for usar o pecas.js em um front de apoio)

Banco SQLite (já embarcado no Python via sqlite3)

Observação: não há requirements.txt versionado no momento — veja a seção abaixo para um exemplo sugerido.

⚙️ Variáveis de ambiente (sugeridas)

Crie um arquivo .env na raiz do projeto com as chaves usadas pelo webhook do WhatsApp:

# Token de verificação do Webhook (usado na validação GET)
VERIFY_TOKEN=seu_verify_token

# Token de acesso (permanente ou de longa duração) da API do WhatsApp Business
WHATSAPP_TOKEN=EAAG...

# Phone Number ID do WhatsApp Business
PHONE_NUMBER_ID=###########

# (Opcional) APP SECRET para validação de assinatura
APP_SECRET=xxxxxxxxxxxxxxxx


Se o código já carrega de outro jeito, mantenha o seu padrão. Essas chaves são as mais comuns para webhooks de WhatsApp Business.

🗄️ Banco de dados

Arquivo: pecas_empilhadeira_pronto.db (SQLite).

Tabelas/colunas podem variar conforme seu script. Se precisar, eu documento o schema a partir do seu arquivo atual.

Popular a base / cadastrar peças

Use o script de cadastro/importação:

python CadastrarPeças.py


Se o script espera um CSV/planilha, informe o caminho no próprio arquivo ou via argumentos. Posso padronizar isso pra --input caminho.csv se quiser.

🚀 Como rodar localmente

Clonar e entrar na pasta

git clone https://github.com/Meng0la/bot_wpps.git
cd bot_wpps


Criar e ativar virtualenv (Windows / Linux / macOS)

python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate


Instalar dependências (exemplo sugerido)

Se você ainda não tem requirements.txt, crie um com o conteúdo sugerido abaixo.

pip install -r requirements.txt


Definir variáveis de ambiente

# crie e preencha o arquivo .env conforme a seção anterior


Rodar o webhook

python whatsapp_webhook.py


Expor o servidor publicamente (para Meta validar o webhook)

Use ngrok ou similar para criar um túnel HTTPS até http://localhost:<porta>.

Cadastre a URL pública + caminho do webhook no app do WhatsApp Business.

Caso o whatsapp_webhook.py já defina a porta/caminho do endpoint, mantenha-os iguais na configuração do app.

🔌 Endpoints (exemplo genérico)

Como não vi o corpo do código nesta navegação, deixo um contrato padrão. Ajusto facilmente assim que você me disser os caminhos que usou.

GET /webhook – Verificação do webhook (Meta envia hub.mode, hub.verify_token, hub.challenge).

POST /webhook – Recebe mensagens do WhatsApp.
Entrada: payload da Meta (mensagem, remetente, tipo).
Saída: 200 OK.
Ações típicas: consultar peça por código/descrição e responder via API de mensagens.

📄 Exemplo de requirements.txt (sugerido)

Ajusto para bater 100% com o seu whatsapp_webhook.py assim que você quiser.

Flask>=3.0
python-dotenv>=1.0
requests>=2.32
gunicorn>=22.0    # opcional p/ deploy


Observação: sqlite3 já vem com o Python. Se estiver usando FastAPI no lugar de Flask, troco para fastapi + uvicorn.

🧩 Uso do pecas.js

Pode servir como módulo de consulta (fetch para um endpoint) ou lógica de front-end.

Se estiver sendo usado em uma página estática, hospede o arquivo e aponte o endpoint do seu backend Python.

🧪 Testes (sugestão)

Simular GET /webhook com VERIFY_TOKEN correto para validar.

Enviar um POST /webhook com payload da Meta de exemplo (posso fornecer um JSON de teste).

Consultar alguns termos/códigos de peça e validar a resposta.

📦 Deploy (sugestão)

Railway / Render / Fly.io / VPS:

Suba como serviço web.

Configure as variáveis .env.

Use gunicorn como server WSGI (caso Flask).

Atualize a URL pública no WhatsApp Business.

🗺️ Roadmap (ideias rápidas)

 Documentar schema do SQLite e criar migrações simples (ex.: alembic ou script SQL).

 Padronizar argumentos do CadastrarPeças.py (--input, --delimiter, --encoding).

 Adicionar Dockerfile e docker-compose.yml.

 Adicionar testes unitários de consulta de peças.

 Criar requirements.txt final e Makefile (tarefas comuns).

🤝 Contribuição

Faça um fork

Crie uma branch: git checkout -b feat/nome-da-feature

Commit: git commit -m "feat: descrição"

Push: git push origin feat/nome-da-feature

Abra um PR
