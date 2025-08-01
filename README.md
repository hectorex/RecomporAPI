<p align="center">
<img loading="lazy" src="http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge"/>
</p>

# Projeto Recompor - API 


<p align="justify"> 
Este projeto tem como objetivo desenvolver uma API (Application Programming Interface) para a integrar e unificar o sistema Web e o sistema Mobile que constituem o projeto Recompor, o qual tem como intuito desenvolver estes softwares para que ajudem as pessoas a entenderem o que é compostagem e como executá-la em casa, além do auxílio no gerenciamento dessa atividade.  
</p>

## Documentação da API

### User Routes

```http
  POST /criar_usuario
```
#### Função 
Criação de um novo usuário.

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `username` | `string` | Unique e Obrigatório |
| `password`   | `string` | Unique = False          |
| `email`   | `string` |  Unique = True         |
| `created_at`   | `datetime` | init = False         |
| `id`   | `string` |**Primary Key** , init= False       |
#### return **user**

#

```http
  DELETE /users/{user_id}
```
#### |---------------- Em construção ----------------|
#### Função 
Deletar um usuário existente do banco.

#

### Composteira Routes

```http
  POST /criar_composteira
```
#### Função 
Criação de uma nova composteira.

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `nome` | `string` | Nome da Composteira |
| `tipo`   | `string` | Terra ou Recipiente        |
| `minhocas`   | `boolean` |  Tem ou Não tem         |
| `data_constru`   | `string` | Data que construiu        |
| `regiao`   | `string` |Região do Brasil|
| `tamanho`   | `float` |Tamanho em metros        |
| `created_at`   | `datetime` | init = False         |
| `user_id`   | `string` | **Foreign Key**          |
| `id`   | `string` | **Primary Key** , init= False        |
#### return **composteira**

### Compostagem Routes

```http
  POST /criar_composteira
```
#### Função 
Criação de uma nova compostagem.

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `nome` | `string` | Nome da Compostagem |
| `data_compostagem`   | `string` | Data da Compostagem        |
| `quantReduo`   | `float` |  Quantidade de resíduo em KG      |
| `frequencia`   | `string` |Diária; Semanal; Mensal.        |
| `previsao`   | `string` |init = False, quando a Compostagem estará pronta.|
| `composteira_id`   | `string` | **Foreign Key**          |
| `id`   | `string` | **Primary Key** , init= False        |
#### return **Compostagem**


## Rodando os testes localmente

**Comandos**

Se ainda precisar criar as tabelas do banco de dados, rode

```bash
  alembic --autogenerate -m "create tables"
```
```bash
  alembic upgrade head
```

Com as tabelas criadas, vá para a pasta "poetry_recomporapi"
```bash
  cd .\poetry_recomporapi\
```

Após isso, inicie a aplicação

```bash
uvicorn API.main:app
```

Agora, para testar o banco de dados, crie um **novo terminal** (com a aplicação ainda rodando no outro) e vá novamente para a **pasta "poetry_recomporapi"**, com o comando apresentado acima.
Em seguida, rode
```bash
  python -m sqlite3 database.db
```
Pronto, já podemos fazer requisições para o banco
```bash
select * from {nome da tabela};
```
**obs. 1:** O atual nome da tabela de users, composteira e compostagem, respectivamente são "users_table", "composteiras_table" e "compostagens_table".

**obs. 2:** Não se esqueça do ponto e vírgula, se não a saída será "...".

Para sair, use 
```bash
.quit
```

## Autores

#### Desenvolvedores
Celso Hector -  [@hectorex](https://github.com/hectorex)

Luiz Felipe -  [@mnzlipe](https://github.com/mnzlipe)

#### Orientadores
Willians Pereira- [@twillpear](https://github.com/willpear)

Daniela Toda - [@danielatoda](https://github.com/danielatoda)

Camila Serrão - [@teachercamila](https://github.com/teachercamila)

