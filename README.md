# 🎫 Sistema de Chamados — Versão Anterior

Aplicação web para abertura, encaminhamento e acompanhamento de chamados internos, desenvolvida com Python, Flask e SQLite.

O usuário registra uma solicitação e a direciona ao setor responsável. O técnico acompanha os chamados recebidos, informa quando o atendimento está em andamento e registra a solução ao finalizar.

> **Este projeto antecede o sistema atualmente desenvolvido.**
>
> Conheça a versão mais recente: [Sistema de Chamados com Assistente Virtual](https://github.com/LovanGoulart/sistema-chamados).

## Contexto e objetivo

Desenvolvi esta primeira versão para organizar solicitações internas e facilitar o acompanhamento dos atendimentos.

O sistema foi útil para centralizar a descrição dos problemas, identificar o setor responsável e permitir que o solicitante acompanhasse o andamento do chamado.

A experiência com essa aplicação ajudou a identificar necessidades que orientaram o desenvolvimento de uma versão posterior, com mais funcionalidades.

## Situação do projeto

**Versão anterior, utilizada antes do sistema atual.**

Este repositório documenta uma etapa da evolução do projeto. Para conhecer a versão mais recente, consulte:

[github.com/LovanGoulart/sistema-chamados](https://github.com/LovanGoulart/sistema-chamados)

## Principais funcionalidades

- Cadastro e login de usuários.
- Identificação do setor no cadastro.
- Abertura de chamados.
- Direcionamento da solicitação ao setor responsável.
- Registro de descrição, local e prioridade.
- Consulta dos chamados realizados pelo usuário.
- Consulta dos chamados recebidos para atendimento.
- Atualização do chamado para em andamento.
- Registro da solução.
- Finalização do atendimento.
- Consulta de informações sobre conclusão e técnico responsável.

## Fluxo de atendimento

1. O usuário cria uma conta e entra no sistema.
2. Registra o problema e informa os dados da solicitação.
3. Direciona o chamado ao setor responsável.
4. O técnico consulta as solicitações recebidas.
5. Ao iniciar o atendimento, o técnico marca o chamado como em andamento.
6. Após resolver o problema, registra a solução e finaliza o chamado.
7. O solicitante acompanha as atualizações na área de seus chamados.

## Participantes do atendimento

| Participante | Atividades |
|---|---|
| Solicitante | Abrir solicitações e acompanhar os chamados realizados. |
| Técnico do setor | Consultar chamados recebidos, atualizar o andamento e registrar a solução. |

## 📸 Demonstração do sistema

Clique nas imagens para abrir os arquivos originais.

### Primeiro acesso

Página inicial com as opções de entrar no sistema ou criar uma conta.

<a href="primeiro%20acesso.png">
  <img src="primeiro%20acesso.png" alt="Página inicial do sistema de chamados anterior" width="900">
</a>

### Cadastro de usuário

Formulário para cadastrar nome, e-mail, senha e setor.

<a href="tela%20de%20cadastro.png">
  <img src="tela%20de%20cadastro.png" alt="Cadastro de usuário com identificação do setor" width="900">
</a>

### Chamados realizados

Área para acompanhar as solicitações abertas pelo usuário, com status, prioridade, descrição, local e informações de conclusão.

<a href="chamados%20realizados.png">
  <img src="chamados%20realizados.png" alt="Acompanhamento dos chamados realizados pelo usuário" width="900">
</a>

### Chamados recebidos

Listagem utilizada no atendimento, com informações da solicitação e ações para atualizar o andamento ou finalizar.

<a href="chamados%20recebidos.png">
  <img src="chamados%20recebidos.png" alt="Chamados recebidos para atendimento técnico" width="900">
</a>

### Registro da solução

Tela para consultar a descrição do problema, informar a solução e finalizar o atendimento.

<a href="solu%C3%A7%C3%A3o%20do%20chamado.png">
  <img src="solu%C3%A7%C3%A3o%20do%20chamado.png" alt="Registro da solução e finalização do chamado" width="900">
</a>

## Evolução do projeto

Esta versão concentrou-se no fluxo essencial de atendimento:

- Registrar a solicitação.
- Encaminhar ao setor.
- Acompanhar o andamento.
- Registrar a solução.
- Finalizar o chamado.

O projeto posterior ampliou essa proposta com novos recursos de gestão e assistência ao usuário.

Para avaliar meu trabalho mais recente nessa área, acesse o [Sistema de Chamados com Assistente Virtual](https://github.com/LovanGoulart/sistema-chamados).

## Tecnologias

| Camada | Tecnologias |
|---|---|
| Backend | Python e Flask |
| Persistência | SQLAlchemy e Flask-SQLAlchemy |
| Banco de dados | SQLite |
| Autenticação | Sessões do Flask e hash de senhas com Werkzeug |
| Interface | Templates HTML e CSS |
| Templates | Jinja2 |
| Versionamento | Git e GitHub |

## Organização do código

A aplicação está localizada na pasta `chamados/sistema`.

```text
chamados/
├── requirements.txt
└── sistema/
    ├── app.py
    ├── static/
    │   └── style.css
    └── templates/
        ├── inicio.html
        ├── login.html
        ├── register.html
        ├── dashboard.html
        ├── novo.html
        ├── meus.html
        ├── todos.html
        └── resolver.html
```

- **app.py:** configuração, modelos e rotas da aplicação.
- **static/style.css:** estilos da interface.
- **templates:** páginas de acesso, abertura, acompanhamento e resolução dos chamados.

## Aspectos técnicos do projeto

- Persistência de usuários e chamados em SQLite.
- Associação das solicitações aos setores responsáveis.
- Acompanhamento das etapas do atendimento.
- Registro da solução vinculada ao chamado.
- Autenticação com verificação de senha em hash.
- Renderização de páginas com Flask e Jinja2.

## Execução local

### 1. Clonar o repositório

```bash
git clone https://github.com/LovanGoulart/Sistema-de-Chamados.git
cd Sistema-de-Chamados
```

### 2. Criar um ambiente virtual

```bash
python -m venv .venv
```

### 3. Ativar o ambiente virtual

**Windows — Git Bash:**

```bash
source .venv/Scripts/activate
```

**Windows — Prompt de Comando:**

```bat
.venv\Scripts\activate.bat
```

**Linux ou macOS:**

```bash
source .venv/bin/activate
```

### 4. Instalar as dependências

```bash
python -m pip install Flask Flask-SQLAlchemy
```

### 5. Iniciar a aplicação

```bash
python chamados/sistema/app.py
```

### 6. Acessar no navegador

```text
http://localhost:5000
```

A execução direta possui inicialização das tabelas no código.

### Observação sobre esta versão

O arquivo `chamados/requirements.txt` precisa de revisão, pois contém um comando de instalação em vez de uma lista de dependências. Por esse motivo, as instruções acima utilizam a instalação direta dos pacotes.

A aplicação inicia com depuração habilitada. Essa configuração é destinada ao desenvolvimento e deve ser revisada antes de qualquer publicação.

## Autor

Desenvolvido por **Lovan Goulart** como primeira versão de uma solução para organização de chamados internos.

[Perfil no GitHub](https://github.com/LovanGoulart)
