# Post Flow

O **Post Flow** é um sistema de postagens para simular funcionalidades de um “correio”. Ele permite cadastrar, listar, atualizar e deletar postagens, além de gerenciar usuários, status e endereços (estes ainda não totalmente implementados).

## Sumário

- [Visão Geral](#visão-geral)  
- [Tecnologias Utilizadas](#tecnologias-utilizadas)  
- [Pré-requisitos](#pré-requisitos)  
- [Instalação e Configuração](#instalação-e-configuração)  
- [Execução em Ambiente de Desenvolvimento](#execução-em-ambiente-de-desenvolvimento)  
- [Regras de Negócio](#regras-de-negócio)  
  - [Usuários](#usuários)  
  - [Status](#status)  
  - [Postagens](#postagens)  
  - [Endereços](#endereços)  
- [Documentação da API](#documentação-da-api)  
- [Testes com Postman](#testes-com-postman)  

---

## Visão Geral

Este projeto tem como objetivo criar um sistema de postagens (como se fosse um serviço de correio), oferecendo recursos de criação, listagem, atualização e exclusão de postagens. Além disso, existem regras de negócio que definem como usuários, status e endereços devem ser tratados, incluindo permissões de acesso e gerenciamento.

---

## Tecnologias Utilizadas

- **Backend**  
  - [Django](https://www.djangoproject.com/)  
  - [Django REST Framework](https://www.django-rest-framework.org/)  
  - [PostgreSQL](https://www.postgresql.org/)  
  - [Redis](https://redis.io/)  
  - [Celery](https://docs.celeryproject.org/en/stable/)

- **Infraestrutura**  
  - [Docker](https://www.docker.com/)  
  - [Docker Compose](https://docs.docker.com/compose/)  
  - *Nginx* (planejado, mas não implementado)  
  - *Gunicorn* (planejado, mas não implementado)

---

## Pré-requisitos

Antes de iniciar, garanta que você tenha instalado em sua máquina:
1. [Docker](https://docs.docker.com/get-docker/)  
2. [Docker Compose](https://docs.docker.com/compose/install/)  
3. [Git](https://git-scm.com/downloads)

---

## Instalação e Configuração

1. **Clone o repositório**  
   ```bash
   git clone https://github.com/giovanniacg/post-flow
   ```

2. **Entre na pasta do projeto**  
   ```bash
   cd post-flow
   ```

3. **Crie o arquivo `.env`**  
   Na raiz do projeto, crie um arquivo `.env` com as mesmas variáveis de ambiente do arquivo `.env.dev`. Exemplo:
   ```env
   SECRET_KEY=secret
   DEBUG=True
   ALLOWED_HOSTS=*

   POSTGRES_DB=postflow
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_HOST=db
   POSTGRES_PORT=5432

   REDIS_HOST=redis
   REDIS_PORT=6379

   CELERY_BROKER_URL=redis://redis:6379/0
   ```

4. **Verifique os comandos disponíveis**  
   Rode o comando de ajuda do Makefile para ver todas as opções de execução:
   ```bash
   make help
   ```

---

## Execução em Ambiente de Desenvolvimento

Para rodar o projeto em um ambiente de desenvolvimento:

1. **Suba os containers**  
   ```bash
   make dev
   ```
   Isso irá criar e inicializar os containers Docker para o backend, banco de dados, Redis e Celery.

2. **Popule o banco de dados**  
   Assim que a aplicação estiver em execução, abra um novo terminal e rode:
   ```bash
   make populate-db
   ```
   Esse comando cria dados iniciais de exemplo no banco.

3. **Crie um usuário admin**  
   Se desejar criar um usuário admin para acessar o Django Admin:
   ```bash
   make create-admin
   ```
   use as credenciais:
    - **Usuário:** admin
    - **Senha:** admin

4. **Acesse a aplicação**  
   Após esse processo, a aplicação estará disponível em:
   ```
   http://localhost:8000/
   ```

---

## Regras de Negócio

O sistema define permissões e comportamentos específicos para cada entidade:

### Usuários

- **Create**  
  Qualquer pessoa pode se cadastrar no sistema.
- **List**  
  Apenas usuários com permissão de administrador (Admin) podem listar todos os usuários.
- **Read**  
  Apenas o próprio usuário ou um Admin pode visualizar os dados de um usuário.
- **Update**  
  Apenas o próprio usuário ou um Admin pode atualizar seus dados.
- **Delete**  
  Apenas o próprio usuário ou um Admin pode deletar sua conta.

### Status

- **Create**  
  Apenas Admins podem criar novos status.
- **List**  
  Apenas usuários logados podem listar todos os status.
- **Read**  
  Apenas usuários logados podem visualizar os dados de um status.
- **Update**  
  Apenas Admins podem atualizar os dados de um status.
- **Delete**  
  Apenas Admins podem deletar um status.

### Postagens

- **Create**  
  Apenas usuários logados podem criar postagens.
- **List**  
  - Admins visualizam todas as postagens.  
  - Usuários logados visualizam apenas suas próprias postagens.
- **Read**  
  Apenas o dono da postagem ou um Admin pode visualizar os detalhes de uma postagem.
- **Update**  
  Apenas um Admin pode atualizar os dados de uma postagem.
- **Delete**  
  Apenas um Admin pode deletar uma postagem.
- **Cache**  
  A listagem de postagens utiliza cache de 5 minutos.
- **Assíncrono**  
  A atualização de status de uma postagem é feita de forma assíncrona por meio do Celery.

### Endereços (Não implementado nesta versão)
- **Create**  
  Apenas usuários logados podem criar endereços.
- **List**  
  - Admins visualizam todos os endereços.  
  - Usuários logados visualizam apenas seus próprios endereços.
- **Read**  
  Apenas o dono do endereço ou um Admin pode visualizar os dados de um endereço.
- **Update**  
  Apenas um Admin pode atualizar os dados de um endereço.
- **Delete**  
  Apenas um Admin pode deletar um endereço.

---

## Documentação da API

A documentação interativa da API (gerada via Django REST Framework) fica disponível em:
```
http://localhost:8000/
```
Assim que o contêiner estiver em execução, você poderá navegar pelos endpoints e ver detalhes de cada rota.

---

## Testes com Postman

Para testar os endpoints de forma prática, você pode utilizar o [Postman](https://www.postman.com/) e importar o arquivo:
```
api_postman_collections.json
```
Esse arquivo contém exemplos de requisições e configurações para facilitar seus testes.