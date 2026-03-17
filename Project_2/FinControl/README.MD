# FinControl

Aplicação web de controle financeiro pessoal construída com Flask, Firebase Authentication e SQLAlchemy. Permite registrar entradas e saídas, acompanhar metas de economia e visualizar relatórios financeiros com gráficos interativos.

---

## Stack

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.13 / Flask |
| Autenticação | Firebase Authentication (Google + Microsoft OAuth) |
| Banco de dados | SQLite (dev) / PostgreSQL (prod) |
| ORM | SQLAlchemy + Flask-Migrate (Alembic) |
| Validação | Marshmallow |
| Frontend | Jinja2 + Tailwind CSS (CDN) + Chart.js |
| Segurança de rotas | Firebase Admin SDK (verificação de ID Token JWT) |

---

## Arquitetura

O projeto segue uma **arquitetura modular por feature**, onde cada domínio (`auth`, `expenses`, `goals`, `categories`, `reports`) é um Blueprint Flask independente com suas próprias rotas, serviços, repositórios e templates.

```
app/
├── auth/           # Autenticação Firebase + gestão de sessão
├── expenses/       # Movimentações financeiras (entradas e saídas)
├── goals/          # Metas de economia e alertas
├── categories/     # Categorias globais e personalizadas
├── reports/        # Relatórios e agregações
├── models/         # Modelos SQLAlchemy centralizados
└── templates/      # Base layout + componentes compartilhados
```

### Separação de responsabilidades

Cada módulo segue três camadas internas:

```
routes.py       → recebe requisições, valida via schema, chama o service
services.py     → regras de negócio, orquestração
repository.py   → queries no banco, único ponto de acesso ao SQLAlchemy
schemas.py      → validação e desserialização de entrada (Marshmallow)
```

### Abordagem híbrida SSR + API

As páginas são renderizadas server-side com dados iniciais (SSR). Filtros, atualizações de saldo e interações dinâmicas usam rotas de API JSON (`/api/*`) consumidas pelo JavaScript do cliente — sem recarregar a página.

Isso resultou em dois decorators de autenticação distintos:

- `@login_required` — para rotas de página, redireciona para `/auth/login`
- `@api_login_required` — para rotas de API, retorna `401 JSON` (evita que o `fetch()` receba HTML)

### Fluxo de autenticação

```
Cliente                    Firebase               Flask
   │                          │                     │
   ├─ loginGoogle() ─────────►│                     │
   │◄─ ID Token (JWT) ────────┤                     │
   │                                                │
   ├─ POST /auth/firebase-callback ────────────────►│
   │                               verify_id_token()│◄── Firebase Admin SDK
   │◄──────────────────── session["user_id"] criada─┤
```

O `user_id` na sessão é sempre o ID do banco local (inteiro), não o `uid` do Firebase. Isso garante que todas as queries usam a chave primária diretamente.

### Isolamento de dados por usuário

Toda query filtra por `user_id` vindo da sessão do servidor — nunca de parâmetros da requisição. Isso implementa a **RN001** e impede que um usuário acesse dados de outro mesmo interceptando e modificando requisições.

### Modelo de saldo

O sistema mantém três visões de saldo simultâneas:

- **Real** — soma de movimentações com `status='paid'`
- **Estimado** — `paid` + `pending` (exclui `cancelled`)
- **Acumulado** — saldo real de todos os meses anteriores ao consultado, limitado ao mês atual para não projetar valores futuros

### Movimentações parceladas e recorrentes

Ao cadastrar uma movimentação parcelada (`payment_type='installment'`), o sistema gera N registros individuais — um por parcela — cada um com a data do mês correspondente. Isso implementa a **RN002** (cada parcela impacta só o seu mês) e simplifica queries de relatório por período.

Movimentações recorrentes (`payment_type='recurring'`) seguem o mesmo padrão: geram registros até a data final informada, ou 12 ocorrências quando sem prazo definido.

Todos os registros de um grupo compartilham o mesmo `parent_id` (ID da primeira ocorrência), permitindo exclusão em grupo com um único endpoint.

---

## Funcionalidades

- Autenticação social com Google e Microsoft via Firebase
- Registro de entradas e saídas com categoria, natureza (fixa/variável), forma de pagamento e status
- Suporte a pagamentos à vista, parcelados e recorrentes (semanal, mensal, anual)
- Metas de economia com barra de progresso e alertas de limite de gasto
- Dashboard com saldo real, estimado e acumulado histórico — navegável por mês
- Relatórios com gráfico de linha (evolução mensal), gráfico de rosquinha (por categoria) e tabela de transações
- Filtros por período, categoria, tipo e status
- Interface responsiva com sidebar no desktop e bottom navigation no mobile

---

## Como rodar localmente

**Pré-requisitos:** Python 3.11+, conta no Firebase com projeto configurado

**1. Clone e instale as dependências**

```bash
git clone https://github.com/seu-usuario/fincontrol.git
cd fincontrol
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**2. Configure as variáveis de ambiente**

Crie um arquivo `.env` na raiz:

```env
SECRET_KEY=sua-chave-secreta
DATABASE_URL=sqlite:///app.db

# Firebase Admin SDK (backend)
FIREBASE_SERVICE_ACCOUNT_JSON=secrets/serviceAccountKey.json

# Firebase Web SDK (frontend)
FIREBASE_API_KEY=
FIREBASE_AUTH_DOMAIN=
FIREBASE_PROJECT_ID=
FIREBASE_APP_ID=
```

Coloque o arquivo `serviceAccountKey.json` (baixado do console Firebase) na pasta `secrets/`.

**3. Configure o Firebase**

No console do Firebase, em **Authentication → Settings → Authorized domains**, adicione `localhost`.

**4. Inicialize o banco e rode**

```bash
flask db upgrade
flask run
```

Acesse `http://localhost:5000`.

---

## Próximos passos

- [ ] Etapa 7 — Segurança avançada: CORS, rate limiting, headers de segurança, sanitização de inputs
- [ ] Etapa 8 — Testes unitários e de integração (services e autenticação)
- [ ] Etapa 9 — Deploy em produção com PostgreSQL e HTTPS
- [ ] Exportação de relatórios em PDF/CSV
- [ ] Notificações de vencimento de parcelas
- [ ] Suporte a múltiplas moedas