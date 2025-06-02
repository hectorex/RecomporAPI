# Resumo
A compostagem doméstica é um processo que ajuda a diminuir a emissão de gás carbônico no meio ambiente. Atualmente existem dois projetos focados em desenvolver sistemas que ajudem as pessoas a entenderem o que é compostagem e como executá-la em casa, um sistema web e outro mobile. O Projeto consiste no desenvolvimento de uma API (Application Programming Interface) para integrar e unificar esses dois sistemas. O intuito desse projeto é democratizar o uso dos sistemas, permitindo que os usuários acessem o sistema no dispositivo que eles tiverem disponível no momento. Além disso, a API garante melhor segurança dos dados e facilita o processo de atualização dos sistemas.

# Notes
funções que dependem de outra/que possuem loops grandes --> assincronas para não atrapalharem o fluxo da API e a responsividade para o user
funções que não dependem de outra --> normais/sincronas, podem ser executadas geralmente de maneira rápida por nao dependerem da resposta de outra função

Dúvidas -- 
Como será a rota de criação do usuário? 
Teremos que criar rotas de composteira de acordo com o usuário em questão? Ou a conexão user-suas_composteiras não precisa ser explícita?
Como será realizada a conexão da API com o sistema web e o sistema mobile? Iremos subir a API em algum servidor do IFRO?
E como/onde iremos realizar as requisições para a API no código do Web e do Mobile?

Fazer -- Listando Composteiras and Compostagens
Na hora de listar compostagens e composteiras, estamos imprimindo todas as composteiras e todas as compostagens da lista. Queremos imprimir somente as composteiras do usuário, e somente as compostagens de uma composteira em específico.
O jeito ideal de corrigir isso:
em composteiras, verificando qual composteira tem o ID do usuário que queremos ver as composteiras (podemos implementar no user depois)
em compostagens, verificando qual compostagem tem o ID da composteira do usuário em questão.

Fazer -- Validação de senha (??) 
Fazer um "input" pedindo para o usuário digitar a senha novamente para ver se bate com a original.
Criar uma função sem ser com rota (nao sei se pode isso) para validar a senha na hora da criação do usuário e da troca de senha.


Fazer -- link composteira - user
Requisitar estar logado para criar composteira (ou seja, ter criado um usuário e estar com ele logado [como fazer esse login?])
