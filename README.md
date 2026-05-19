<h1 align="center">API VidaPlus - Sistema de gestão hospitalar</h1>
## 📑 Tabela de conteúdos

- [Sobre o projeto](#sobre-o-projeto)
  - [Principais Recursos](#principais-recursos)
  - [Autenticação](#autenticacao)
  - [Endpoints](#endpoints)
- [Como executar o projeto](#como-executar-o-projeto)
  - [Pré-requisitos](#pre-requisitos)
  - [Executando o Docker](#rodando-o-docker)
- [Tecnologias](#tecnologias)
- [Como contribuir no projeto](#como-contribuir)
- [Autor](#autor)

---

## 💻 Sobre o projeto <a name="sobre-o-projeto"></a>

A **API VidaPlus** é uma solução desenvolvida para gerenciar hospitais e serviços de saúde, permitindo o controle de pacientes, profissionais, consultas, prontuários, prescrições, exames e leitos. Construída com **FastAPI**, a API oferece endpoints organizados, seguros e documentados para facilitar a integração com sistemas externos e o desenvolvimento de aplicações web e mobile.

### Principais Recursos
- **Pacientes:** Cadastro, consulta, atualização e remoção de pacientes.
- **Profissionais:** Gerenciamento de profissionais de saúde, permissões e autenticação.
- **Consultas:** Agendamento, listagem, atualização e cancelamento de consultas.
- **Prontuários:** Criação e acesso a históricos médicos dos pacientes.
- **Prescrições:** Registro e controle de prescrições médicas.
- **Exames:** Solicitação, acompanhamento e resultados de exames.
- **Leitos:** Gerenciamento de ocupação e disponibilidade de leitos hospitalares.
- **Estoque:** Gerenciamento de toda a parte de estoques hospitalares.

### Autenticação <a name="autenticacao"></a>
A API utiliza autenticação baseada em JWT (JSON Web Token). Para acessar endpoints protegidos, é necessário obter um token de acesso realizando login com credenciais válidas.


### Endpoints <a name="endpoints"></a>

Os endpoints estão organizados por recurso, seguindo o padrão REST:

- `/pacientes/`
- `/profissionais/`
- `/consultas/`
- `/prontuario/`
- `/prescricoes/`
- `/exame/`
- `/leitos/`
- `/Estoque/`

Cada endpoint suporta operações de **CRUD** (Create, Read, Update, Delete), com validação de permissões e regras de negócio.

---

## 🚀 Como executar o projeto <a name="como-executar-o-projeto"></a>

### 🛠 Pré-requisitos <a name="pre-requisitos"></a>

Todo esse projeto é gerenciado pelo Poetry, a versão usada durante o momento da escrita é 2.1.2:
```bash
pipx install poetry==2.1.2
pipx inject poetry poetry-plugin-shell
```

A versão usada do python é a versão 3.13.2:
```bash
pyenv local 3.13.2
```

para configurar todo o ambiente basta executar:
```bash
poetry install
```

para configurar todo o ambiente basta executar:
```bash
poetry shell
```

### Sobre os comandos <a name="rodando-o-docker"></a>

Os comandos para executar funções como deploy, servidor local, geração de slides, etc. Estão todas sendo feitas pelo taskipy:
```bash
task --list
serve       Executa o servidor local do mkdocs
deploy      Faz o deploy da página em produção
```

Para executar qualquer comando, basta usar: task <comando>, como por exemplo task serve.

---

## 🐳 Rodando o projeto com Docker <a name="rodando-o-docker"></a>

Para rodar o projeto com Docker, siga os passos abaixo:

### 1. Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) instalado na sua máquina.

### 2. Build da imagem

No diretório raiz do projeto, execute:

```bash
docker build -t vidaplus-api .
```

### 3. Executando o container
Para executar o container, use o seguinte comando:

```bash
docker run -d --name vidaplus-api -p 8000:8000 vidaplus-api
```

### 4. Acessando a API
A API estará disponível em `http://localhost:8000`. Você pode acessar a documentação interativa da API em `http://localhost:8000/docs`.

---

## 🛠 Tecnologias <a name="tecnologias"></a>

O projeto foi desenvolvido com as seguintes tecnologias:

- **Python 3.13**
- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **Pydantic**
- **PyJWT**
- **Alembic**
- **pytest**

---

## 💪 Como contribuir no projeto <a name="como-contribuir"></a>

1. Faça um **fork** do repositório.
2. Crie uma branch: `git checkout -b minha-feature`
3. Faça suas alterações e salve com um commit: `git commit -m "feat: minha nova funcionalidade"`
4. Envie para o repositório: `git push origin minha-feature`

---

## 🦸 Autor <a name="autor"></a>

Desenvolvido por **[Rauane Lima](https://github.com/lrauane)**
