# LanchoneteAPI

API REST desenvolvida em **Python com Flask** para gerenciamento de uma rede de lanchonetes com múltiplas unidades.

O sistema centraliza usuários, funcionários, cardápios, estoques, pedidos, pagamentos, promoções, programa de pontos e relatórios. Cada unidade possui seu próprio estoque, enquanto a administração global pode consultar e alterar dados de todas as unidades.

---

## Funcionalidades

### Autenticação e autorização

- Cadastro e login de usuários.
- Autenticação com JWT.
- Controle de acesso por perfil.
- Proteção de rotas por meio do decorator `perfil_required`.
- Alteração de dados cadastrais pelo próprio usuário.
- Ativação e desativação lógica de cadastros.

### Perfis de acesso

| Perfil | Permissões principais |
|---|---|
| `CLIENTE` | Consultar cardápio, criar pedido, editar pedido antes do pagamento, pagar, consultar histórico e pontos |
| `ATENDENTE` | Consultar e atualizar pedidos da própria unidade |
| `COZINHEIRO` | Visualizar pedidos ativos e alterar etapas de preparo |
| `GERENCIA` | Gerenciar estoque, funcionários, promoções e relatórios da própria unidade |
| `ADMINISTRADOR` | Acesso global a usuários, unidades, produtos, estoques, promoções e relatórios |

### Unidades e estoque

- Cadastro de unidades.
- Associação de funcionários a uma unidade.
- Estoque independente por unidade.
- Mesmo produto disponível em várias unidades.
- Controle de quantidade e disponibilidade.
- Atualização de preço em todos os estoques relacionados ao mesmo produto.
- Devolução de itens ao estoque em cancelamentos.
- Cardápio filtrado por unidade.

### Pedidos

- Criação de pedidos com múltiplos itens.
- Cálculo de subtotal e total com `Decimal`.
- Aplicação de promoções.
- Aplicação de desconto com pontos.
- Atualização de quantidade antes do pagamento.
- Remoção de item antes do pagamento.
- Histórico de pedidos do cliente.
- Listagem de pedidos por unidade e por data.
- Preservação dos dados do item comprado no histórico.

### Fluxo de status

O pedido percorre etapas controladas:

```text
AGUARDANDO_PAGAMENTO
        ↓
AGUARDANDO_CONFIRMACAO
        ↓
EM_PREPARO
        ↓
PRONTO
        ↓
AGUARDANDO_ENTREGADOR
        ↓
FINALIZADO
```

Também podem existir os status:

```text
PAGAMENTO_RECUSADO
CANCELADO
```

### Pagamentos

- Mock de pagamento.
- Suporte a diferentes métodos.
- Aprovação automática ou simulada.
- Código único da transação.
- Atualização do status do pedido.
- Bloqueio de pagamento por usuário diferente do dono do pedido.

### Promoções

- Promoção por produto.
- Promoção por unidade ou global.
- Desconto percentual.
- Desconto por valor fixo.
- Quantidade mínima.
- Período de validade.
- Ativação e desativação.
- Aplicação automática no cálculo do pedido.

### Programa de pontos

- Acúmulo de pontos em pedidos finalizados.
- Registro de pontos ganhos e utilizados.
- Saldo disponível no usuário.
- Conversão de pontos em desconto.
- Regra atual:

```text
5 pontos = R$ 0,50
1 ponto  = R$ 0,10
```

O resgate é permitido somente quando o cliente possui mais de **R$ 5,00** em desconto acumulado.

### Relatórios

- Total vendido por unidade.
- Total vendido no dia.
- Quantidade de pedidos.
- Ticket médio.
- Produto mais vendido por unidade.
- Produto mais vendido globalmente.
- Histórico de alterações de preço.

---

## Tecnologias

- Python 3.12
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-Migrate
- Alembic
- Flask-JWT-Extended
- PostgreSQL
- Psycopg2
- Supabase
- Python Dotenv

---

## Arquitetura

O projeto segue uma organização em camadas:

```text
LanchoneteAPI/
│
├── app/
│   ├── models/
│   ├── repositories/
│   ├── services/
│   ├── routes/
│   ├── util/
│   ├── database.py
│   └── __init__.py
│
├── migrations/
├── .env
├── .env.example
├── .gitignore
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

### Responsabilidade das camadas

| Camada | Responsabilidade |
|---|---|
| `models` | Mapeamento das tabelas e relacionamentos |
| `repositories` | Consultas e operações com o banco |
| `services` | Regras de negócio e validações |
| `routes` | Endpoints HTTP e respostas JSON |
| `util` | Decorators e funções auxiliares |

---

## Requisitos

Antes de executar o projeto, instale:

- Python 3.12 ou superior
- PostgreSQL local ou projeto no Supabase
- Git

---

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/ju-c-santos/LanchoneteAPI.git 
cd LanchoneteAPI
```

### 2. Crie o ambiente virtual

```bash
python -m venv .venv
```

### 3. Ative o ambiente virtual

No PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

No Prompt de Comando:

```cmd
.venv\Scripts\activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## Variáveis de ambiente

Crie o arquivo `.env` com base no `.env.example`.

```env
DATABASE_URL=
SECRET_KEY=
JWT_SECRET_KEY=
```

Exemplo de conexão local:

```env
DATABASE_URL=postgresql://postgres:SENHA@localhost:5432/lanchonete
```

Exemplo de conexão com Supabase:

```env
DATABASE_URL=postgresql://USUARIO:SENHA@HOST:5432/postgres
```

> Nunca envie o arquivo `.env` para o GitHub.

O `.gitignore` deve conter:

```gitignore
.env
.venv/
__pycache__/
*.py[cod]
```

---

## Banco de dados

### Aplicar migrations existentes

```bash
flask db upgrade
```

### Criar uma nova migration

```bash
flask db migrate -m "descricao da alteracao"
```

### Verificar a revisão atual

```bash
flask db current
```

### Ver o histórico

```bash
flask db history
```

### Voltar uma migration

```bash
flask db downgrade -1
```

> Alterações em ENUMs do PostgreSQL podem exigir edição manual da migration.

---

## Executando a aplicação

Com o ambiente virtual ativado:

```bash
python run.py
```

A API ficará disponível em:

```text
http://127.0.0.1:5000
```

---

## Autenticação

Após o login, envie o token no cabeçalho:

```http
Authorization: Bearer SEU_ACCESS_TOKEN
```

O token armazena o ID do usuário e o perfil utilizado pelo controle de acesso.

---

## Exemplos de endpoints

Os caminhos abaixo representam os principais recursos da API. Ajuste-os conforme as rotas atualmente registradas no projeto.

### Usuários

```http
POST   /register
POST   /login
PATCH  /usuarios/alteracao/{usuario_id}
```

### Funcionários

```http
POST   /admin/register/funcionarios
PATCH  /admin/funcionarios/cargo/{funcionario_id}
PATCH  /admin/funcionarios/unidade/{funcionario_id}
```

### Estoque e cardápio

```http
GET    /unidades/{unidade_id}/menu
PATCH  /admin/estoques/{estoque_id}/quantidade
```

### Pedidos

```http
POST   /pedidos
GET    /pedidos/historico
GET    /admin/pedidos
PATCH  /pedidos/{pedido_id}/itens/{item_id}
DELETE /pedidos/{pedido_id}/itens/{item_id}
```

### Pagamento

```http
POST   /pedidos/{pedido_id}/pagamento
```

### Promoções

```http
POST   /admin/promocoes
GET    /admin/promocoes
GET    /promocoes
PATCH  /admin/promocoes/{promocao_id}
```

---

## Exemplo de criação de pedido

```json
{
  "unidade_id": 1,
  "observacao": "Sem cebola",
  "entrega": false,
  "local_pedido": "WEBSITE",
  "usar_pontos": false,
  "itempedido": [
    {
      "produto_id": 3,
      "quantidade": 2
    },
    {
      "produto_id": 7,
      "quantidade": 1
    }
  ]
}
```

---

## Regras importantes

- O cliente só pode alterar pedidos em `AGUARDANDO_PAGAMENTO`.
- O cliente só pode pagar um pedido que pertence à própria conta.
- O funcionário acessa apenas os dados da própria unidade.
- O administrador possui acesso global.
- Produtos e estoques utilizados em pedidos não devem ser apagados fisicamente.
- Exclusão lógica deve ser priorizada com campos como `is_active`, `ativa` ou `cadastro_ativo`.
- Operações relacionadas devem utilizar uma única transação com `commit()` no final e `rollback()` em caso de erro.
- Valores monetários devem utilizar `Decimal` ou `Numeric`, evitando `float` para cálculos financeiros.

---

## Segurança

- Senhas devem ser armazenadas somente como hash.
- Credenciais devem permanecer no `.env`.
- Tokens JWT devem possuir tempo de expiração.
- Rotas administrativas devem validar o perfil.
- O ID do usuário deve ser obtido pelo JWT sempre que possível.
- O backend deve validar unidade, quantidade, status e propriedade do pedido.

---

## Testes

As rotas podem ser testadas com:

- Postman
- Insomnia
- Thunder Client

Cabeçalhos comuns:

```http
Content-Type: application/json
Authorization: Bearer SEU_ACCESS_TOKEN
```

---

## Melhorias futuras

- Testes automatizados com Pytest.
- Documentação com Swagger ou OpenAPI.
- Integração com gateway de pagamento real.
- Notificações em tempo real.
- Dashboard web para gestão.
- Controle de movimentação de estoque.
- Cupons de desconto.
- Upload de imagens dos produtos.
- Logs e auditoria administrativa.
- Deploy automatizado.

---

## Autora

Desenvolvido por **Juliana Conceição**.

Projeto criado para estudo e desenvolvimento de uma API REST multicamadas com Flask, PostgreSQL e Supabase.
