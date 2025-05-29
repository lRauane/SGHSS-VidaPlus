<h1 align="center">VidaPlus - Sistema de gestão hospitalar</h1>

## 📑 Tabela de conteúdos

- [Sobre o projeto](#sobre-o-projeto)
- [Como executar o projeto](#como-executar-o-projeto)
  - [Pré-requisitos](#pre-requisitos)
  - [Rodando o Docker](#rodando-o-docker)
- [Tecnologias](#tecnologias)
- [Como contribuir no projeto](#como-contribuir)
- [Autor](#autor)
- [Licença](#licenca)

---

## 💻 Sobre o projeto <a name="sobre-o-projeto"></a>

📊 O **VidaPlus** é um sistema de Gestão Hospitalar e de Serviços de Saúde desenvolvido para otimizar e modernizar o gerenciamento de instituições de saúde. A plataforma oferece recursos para o controle eficiente de pacientes, profissionais, consultas, prontuários, prescrições, exames e leitos, promovendo maior segurança, agilidade e integração entre os setores. Construído com tecnologias modernas como FastAPI, o VidaPlus visa facilitar a rotina administrativa e clínica, proporcionando uma experiência intuitiva tanto para gestores quanto para profissionais da saúde.



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

### 📊 Sobre os comandos <a name="rodando-o-docker"></a>

Os comandos para executar funções como deploy, servidor local, geração de slides, etc. Estão todas sendo feitas pelo taskipy:
```bash
task --list
serve       Executa o servidor local do mkdocs
deploy      Faz o deploy da página em produção
```

Para executar qualquer comando, basta usar: task <comando>, como por exemplo task serve.

---

### 📊 Rodando o Docker <a name="rodando-o-docker"></a>



---

## 🛠 Tecnologias <a name="tecnologias"></a>

O projeto foi desenvolvido com as seguintes tecnologias:

- **Python 3.12**
- **PostgreSQL 16**
- **fastAPI** (Servidor de aplicação)
- **pydantic** (Schemas para validar entrada e saída da aplicação)
- **sqlalchemy** (ORM para interagir com o banco de dados)
- **pydantic-settings** (Para ler o arquivo .env com tipagem)
- **alembic** (Para gerar e gerir migrações no banco de dados)
- **pyjwt** (Gerar, validar e decodificar JWTs)
- **pwdlib** (Gerar e validar hash de senhas)

Dependências de desenvolvimento:

- **pytest** (Servidor de aplicação)
- **pydantic** (Schemas para validar entrada e saída da aplicação)
- **sqlalchemy** (ORM para interagir com o banco de dados)
- **pydantic-settings** (Para ler o arquivo .env com tipagem)
- **alembic** (Para gerar e gerir migrações no banco de dados)
- **pyjwt** (Gerar, validar e decodificar JWTs)
- **pwdlib** (Gerar e validar hash de senhas)
- **unicorn** (Monitoramento e logs)

---

## 💪 Como contribuir no projeto <a name="como-contribuir"></a>

1. Faça um **fork** do repositório.
2. Crie uma branch: `git checkout -b minha-feature`
3. Faça suas alterações e salve com um commit: `git commit -m "feat: minha nova funcionalidade"`
4. Envie para o repositório: `git push origin minha-feature`

---

## 🦸 Autor <a name="autor"></a>

Desenvolvido por **[Rauane Lima](https://github.com/lrauane)** 🚀
