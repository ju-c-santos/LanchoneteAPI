# 🍔 LanchoneteAPI

API REST desenvolvida em **Python + Flask** para gerenciamento interno de uma rede de lanchonetes.

O projeto utiliza arquitetura em camadas, autenticação com JWT, controle de acesso por perfil, PostgreSQL, gerenciamento de estoque por unidade, pedidos multicanal, promoções, programas de pontos e integração de pagamento mock.

---

## 📚 Documentação Swagger / OpenAPI

A documentação pública da API está disponível pelo GitHub Pages:

### 🔗 [Acessar documentação Swagger](https://ju-c-santos.github.io/LanchoneteAPI/#/Autenticação/realizarLogin)

A documentação permite consultar:

- endpoints disponíveis;
- métodos HTTP;
- parâmetros de rota e filtros;
- corpos das requisições;
- códigos de resposta;
- exemplos de sucesso e erro;
- autenticação JWT;
- schemas utilizados pela API.

> Para executar endpoints protegidos pelo Swagger, realize o login, copie o token JWT e utilize o botão **Authorize**.

---

## 🎯 Objetivo do projeto

A LanchoneteAPI foi criada para representar o back-end de uma rede de lanchonetes, centralizando regras de negócio relacionadas a:

- usuários e autenticação;
- funcionários e perfis de acesso;
- unidades;
- produtos;
- estoque por unidade;
- cardápio;
- pedidos;
- pagamentos;
- promoções;
- fidelização por pontos;
- consultas gerenciais.

A aplicação foi organizada seguindo a separação:

```text
Route
  ↓
Service
  ↓
Repository
  ↓
Model
  ↓
PostgreSQL
```

---

## 🧱 Arquitetura

O projeto segue uma arquitetura em camadas.

### Routes

Responsáveis por:

- receber requisições HTTP;
- recuperar parâmetros, query params e JSON;
- identificar o usuário autenticado;
- chamar os Services;
- retornar a resposta HTTP.

### Services

Responsáveis por:

- regras de negócio;
- validações;
- permissões;
- conversão de dados;
- orquestração das operações.

### Repositories

Responsáveis por:

- consultas ao banco;
- filtros;
- paginação;
- persistência;
- atualização e remoção de registros.

### Models

Responsáveis pela representação das entidades do banco utilizando SQLAlchemy.

---

## 🛠️ Tecnologias utilizadas

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
- Swagger UI
- OpenAPI 3.1
- Postman
- Git / GitHub
- GitHub Pages

---

# 🔐 Autenticação e autorização

A API utiliza **JWT (JSON Web Token)**.

Após o login, o token deve ser enviado nas rotas protegidas:

```http
Authorization: Bearer SEU_TOKEN_JWT
```

Exemplo de login:

```http
POST /login
```

```json
{
  "usuario": "cliente@email.com",
  "senha": "123456"
}
```

Os endpoints protegidos também utilizam controle de acesso por perfil.

Perfis utilizados pelo sistema:

```text
CLIENTE
ATENDENTE
COZINHEIRO
GERENCIA
ADMINISTRADOR
GESTAO
```

Exemplo no Flask:

```python
@perfil_required("ADMINISTRADOR", "GERENCIA", "GESTAO")
```

---

# 👤 Usuários

O sistema possui funcionalidades para:

- cadastro;
- login por e-mail ou CPF;
- atualização cadastral;
- ativação e desativação de cadastro;
- consulta de saldo de pontos;
- exclusão de usuário;
- controle de acesso por perfil.

Exemplos:

```http
POST /usuario/register
POST /login
PATCH /usuario/alteracao/{usuarioId}
GET /usuario/consulta/saldo
DELETE /usuario/{usuarioId}/delete
```

---

# 👨‍🍳 Funcionários

Funcionários são associados a uma unidade da rede e possuem permissões conforme o cargo/perfil.

Entre as operações disponíveis estão:

- cadastro de funcionário;
- alteração de cargo;
- alteração de unidade;
- ativação e desativação de férias;
- consulta de funcionários;
- remoção.

---

# 🏪 Unidades

Cada unidade possui seus próprios registros operacionais e seu próprio estoque.

Entre as operações disponíveis estão:

- cadastro;
- consulta;
- atualização;
- ativação/desativação;
- associação de funcionários;
- estoque independente.

Exemplo:

```http
POST /admin/register/unidade
```

---

# 📦 Produtos e estoque

Um mesmo produto pode existir em estoques de diferentes unidades.

Exemplo conceitual:

```text
Produto: X-Burger

Unidade 1
Quantidade: 30
Preço: R$ 20,00

Unidade 2
Quantidade: 12
Preço: R$ 22,00
```

Assim, a disponibilidade e quantidade pertencem ao estoque da respectiva unidade.

O sistema permite:

- cadastro de produtos;
- associação de produtos ao estoque;
- entrada e saída de quantidade;
- alteração de preço;
- consulta de estoque;
- consulta de cardápio por unidade;
- filtragem e paginação.

---

# 🍽️ Cardápio por unidade

O cardápio é consultado a partir do estoque da unidade.

Exemplo:

```http
GET /unidade/{unidadeId}/menu
```

A consulta pode utilizar filtros como nome, categoria, disponibilidade, preço e ordenação.

---

# 🛒 Pedidos

O pedido contém informações como:

- cliente;
- unidade;
- itens;
- quantidades;
- preço unitário;
- subtotal;
- total;
- status;
- entrega;
- pontos;
- canal de origem.

## Canais de pedido

Os pedidos podem ser originados por:

```text
APP
TOTEM
BALCAO
PICKUP
WEB
```

O canal é armazenado no domínio do pedido e pode ser utilizado em filtros de consulta.

Exemplo:

```http
?canalPedido=TOTEM
```

---

## 🔄 Fluxo de status do pedido

Fluxo principal:

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

Também existem os estados:

```text
PAGAMENTO_RECUSADO
CANCELADO
```

---

# 💳 Pagamentos

O projeto utiliza um serviço de pagamento **mock**, sem integração com pagamento financeiro real.

O fluxo representa:

```text
Pedido
  ↓
Solicitação de pagamento
  ↓
Pagamento mock
  ↓
Resultado
  ↓
Atualização do pedido
```

Métodos representados no domínio incluem:

```text
DINHEIRO
DEBITO
CREDITO
PIX
VALE
```

---

# 🎁 Promoções

A API possui suporte a promoções e campanhas.

Tipos de desconto:

```text
PERCENTUAL
VALOR_FIXO
```

As consultas de promoções permitem filtros como:

```text
promocaoId
nomePromocao
produtoId
tipoPromocao
dataInicio
dataFim
valorMin
valorMax
ativa
ordenacao
page
limit
```

---

# ⭐ Programa de fidelidade

Clientes podem acumular e utilizar pontos conforme as regras definidas no sistema.

Exemplo de consulta:

```http
GET /usuario/consulta/saldo
```

A resposta pode apresentar informações como:

```json
{
  "pontosDisponiveis": 30,
  "valorDesconto": "3.00",
  "podeUtilizar": false
}
```

---

# 📊 Consultas e relatórios

A API possui consultas voltadas à operação e gestão, incluindo:

- histórico de pedidos;
- pedidos do dia;
- pedidos em aberto;
- faturamento;
- total vendido;
- produtos vendidos;
- produto mais vendido;
- histórico de alteração de preços;
- filtros por unidade, usuário, status, canal, período e valor.

As consultas utilizam paginação quando necessário.

---

# ⚠️ Padrão de erros

A API utiliza um formato padronizado para erros.

Exemplo:

```json
{
  "error": "PEDIDO_NAO_ENCONTRADO",
  "message": "O pedido informado não foi encontrado.",
  "details": [
    {
      "field": "pedidoId",
      "issue": "Não existe pedido com o ID informado."
    }
  ],
  "timestamp": "2026-08-09T18:00:00-03:00",
  "path": "/pedidos/10",
  "requestId": "uuid-da-requisicao"
}
```

Principais códigos HTTP utilizados:

| Código | Significado |
|---|---|
| `200` | Requisição realizada com sucesso |
| `201` | Recurso criado com sucesso |
| `400` | Requisição malformada |
| `401` | Token ausente, inválido ou expirado |
| `403` | Usuário autenticado sem permissão |
| `404` | Recurso não encontrado |
| `409` | Conflito com o estado atual ou regra de negócio |
| `422` | Dados ou parâmetros inválidos |
| `500` | Erro interno do servidor |

---

# 🚀 Como executar o projeto

## 1. Pré-requisitos

É necessário ter instalado:

- Python 3.12 ou superior;
- Git;
- PostgreSQL ou acesso a um banco PostgreSQL/Supabase.

---

## 2. Clone o repositório

```bash
git clone https://github.com/ju-c-santos/LanchoneteAPI.git
cd LanchoneteAPI
```

---

## 3. Crie o ambiente virtual

```bash
python -m venv .venv
```

No PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

No CMD:

```cmd
.venv\Scripts\activate
```

---

## 4. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 5. Configure as variáveis de ambiente

Crie um arquivo `.env` baseado no `.env.example`.

Exemplo:

```env
DATABASE_URL=postgresql://usuario:senha@host:porta/banco
SECRET_KEY=sua_chave_secreta
JWT_SECRET_KEY=sua_chave_jwt_segura
```

> Não envie o arquivo `.env` para o GitHub e não exponha senhas ou chaves reais.

---

## 6. Atualize o banco

```bash
flask db upgrade
```

Comandos úteis:

```bash
flask db current
flask db history
flask db migrate -m "descricao da migration"
flask db upgrade
flask db downgrade -1
```

---

## 7. Execute a aplicação

```bash
python run.py
```

A API local ficará disponível em:

```text
http://127.0.0.1:5000
```

---

# 📖 Swagger local

Com a aplicação Flask em execução:

```text
http://127.0.0.1:5000/docs/
```

## Swagger público

A documentação também está publicada no GitHub Pages:

### 🔗 https://ju-c-santos.github.io/LanchoneteAPI/#/Autenticação/realizarLogin

---

# 🧪 Testes com Postman

O projeto possui coleção e ambiente do Postman para reprodução dos testes.

Arquivos:

```text
LanchoneteAPI_Postman_Collection.json
LanchoneteAPI_Postman_Environment.json
```

No Postman:

1. importe a coleção;
2. importe o ambiente;
3. selecione o ambiente `LanchoneteAPI - Local`;
4. configure as credenciais dos perfis utilizados;
5. execute os logins para gerar os tokens;
6. execute os cenários de teste.

Variáveis utilizadas incluem:

```text
{{baseUrl}}

{{clienteToken}}
{{adminToken}}
{{funcionarioToken}}

{{usuarioId}}
{{unidadeId}}
{{funcionarioId}}
{{produtoId}}
{{estoqueId}}
{{promocaoId}}
{{pedidoId}}
{{itemPedidoId}}
```

A coleção possui cenários positivos e negativos para validar os principais fluxos da aplicação.

> Atenção ao executar a coleção completa: existem endpoints que podem alterar ou excluir registros.

---

# 🧪 Exemplos de testes

### Login

```http
POST /login
```

### Consultar menu

```http
GET /unidade/{unidadeId}/menu
```

### Consultar promoções

```http
GET /admin/promocoes?page=1&limit=20
```

### Consultar pedidos em aberto

```http
GET /funcionarios/pedidos/em_aberto?page=1&limit=20
```

### Consultar saldo

```http
GET /usuario/consulta/saldo
```

---

# 🔒 Segurança

O projeto utiliza:

- hash de senha;
- JWT;
- autorização por perfil;
- variáveis de ambiente;
- respostas de erro padronizadas;
- controle de acesso às rotas administrativas;
- identificação de requisições por `requestId`.

Segredos e credenciais não devem ser versionados no Git.

---

# 🗄️ Banco de dados

Banco utilizado:

```text
PostgreSQL
```

O projeto utiliza SQLAlchemy para ORM e Alembic/Flask-Migrate para controle de migrations.

O banco pode ser hospedado no Supabase.

---

# 🌐 Documentação e acesso

| Recurso | Acesso |
|---|---|
| API local | `http://127.0.0.1:5000` |
| Swagger local | `http://127.0.0.1:5000/docs` |
| Swagger público | [GitHub Pages](https://ju-c-santos.github.io/LanchoneteAPI/#/Autenticação/realizarLogin) |
| Especificação | `docs/openapi.yaml` |
| Coleção Postman | `LanchoneteAPI_Postman_Collection.json` |
| Ambiente Postman | `LanchoneteAPI_Postman_Environment.json` |

---

# 📌 Observação

O Swagger publicado no GitHub Pages disponibiliza a documentação da API de forma pública.

A execução pelo botão **Try it out** depende de o servidor Flask configurado em `servers` no OpenAPI estar acessível.

---

_Juliana Conceição_

Projeto desenvolvido para estudo e aplicação prática de desenvolvimento back-end com Flask, APIs REST, banco de dados relacional, autenticação, documentação OpenAPI e testes de API.
