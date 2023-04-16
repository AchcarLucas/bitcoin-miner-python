# Bitcoin Miner Python

Esse projeto foi feito como uma forma de eu aprender um pouco mais sobre o bitcoin e suas estruturas, acabei focando bastante na parte da mineração 
pois é uma área que eu gosto muito

## 🚀 Começando

Essas instruções permitirão que você obtenha uma cópia do projeto em operação na sua máquina local para fins de desenvolvimento e teste.

Consulte **[Implantação](#-implanta%C3%A7%C3%A3o)** para saber como implantar o projeto.

### 📋 Pré-requisitos

Como eu fiz o projeto do zero, acabou que não necessitou a utilização de nenhuma biblioteca externa, apenas as bibliotecas internas
já foram suficientes, são elas:

```
base64
binascii
hashlib
random
json
struct
time
```

### 🔧 Instalação

Como a mineração do bitcoin na mainnet (rede principal do bitcoin) é bastante dificil de minerar, podemos
criar uma rede de teste, chamamos essa rede de regtest, só existe um único problema nela, ou talvez não seja
um problema :) a regtest não simula dificuldade, qualquer bloco pode ser minerado com poucas iterações

Bom, inicie baixando o bitcoin core no site https://bitcoin.org/en/bitcoin-core/, vamos precisar dele
para criar o regtest e ter acesso ao RPC para algumas funções auxiliares

Quando você baixar e abrir, não é necessário baixar todos os blocos da mainnet (rede principal),
basta ir em ```Definições - Opções - Abrir Arquivo de Configuração``` e dentro desse arquivo
coloque esse script

```
regtest=1

[regtest]
server=1
connect=127.0.0.1
port=18444

rpcconnect=127.0.0.1
rpcport=8332

debug=1

rpcauth=USER_RPC:PASSWORD_RPC

whitelist=127.0.0.1
testactivationheight=segwit@432
```

Esse script ativa o regtest e ainda habilita o RPC

Em ```USER_RPC``` e ```PASSWORD_RPC``` você irá configurar seu usuário e senha do RPC

O nome de usuário é simples, não existe nenhuma codificação, já a senha, pode ser gerada usando o seguinte script ```https://github.com/bitcoin/bitcoin/blob/master/share/rpcauth/rpcauth.py```,
baixa o script e execute o seguinte comando ```python3 rpcauth.py <username> <password>``` a saída já é sua rpcauth no padrão no bitcoin core
outra alternativa é usar o seguinte site: https://jlopp.github.io/bitcoin-core-rpc-auth-generator/ que faz a geração do  rpcauth para você.

Bom, depois que você configurou o arquivo .config, salva e reinicie o bitcoin  core, você irá perceber que a cor mudou para o azul, parabéns, você está na regtest

## ⚙️ Executando os testes

Dentro do bitcoin core, crie uma wallet e depois um endereço em receber, faça a copia da chave pública para dentro do arquivo de configuração do python ```config.py``` na parte

```
    walletAddress = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 
```

Onde está` ```xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx``` adicione sua chave pública onnde será recebido os bitcoins de recompennsas por encontrar o bloco e todas as fee (taxas) que
das transações que você efetuou no bloco

Além disso, ainda na ````config.py``` na parte

```` 
"host": "127.0.0.1",
"port": "8332",
"rpcuser": "Achcar",
"rpcpass": "BCQ_DJMYDj-qhevMqthkK4suxmJq_tXht5fZxXXkoXY=",
"rpcurl": "http://127.0.0.1:8332"
````

configure o rpcuser e o rpcpass, lembrando, o rpcpass não é a codificado, é a sua rpcpass que foi usado para gerar a codificação

### 🔩 Analise os testes de ponta a ponta

Com tudo configurado, execute o mineradoor usando python miner.py dentro de src, a cada 1 segundo (se quiser gerar por um teempo maior, mude o time.sleep no arquivo principal ```miner.py```) um bloco novo será gerado

### ⌨️ E testes de estilo de codificação

Explique que eles verificam esses testes e porquê.

```
Dar exemplos
```

## 📦 Implantação

Adicione notas adicionais sobre como implantar isso em um sistema ativo

## 🛠️ Construído com

Mencione as ferramentas que você usou para criar seu projeto

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - O framework web usado
* [Maven](https://maven.apache.org/) - Gerente de Dependência
* [ROME](https://rometools.github.io/rome/) - Usada para gerar RSS

## 🖇️ Colaborando

Por favor, leia o [COLABORACAO.md](https://gist.github.com/usuario/linkParaInfoSobreContribuicoes) para obter detalhes sobre o nosso código de conduta e o processo para nos enviar pedidos de solicitação.

## 📌 Versão

Nós usamos [SemVer](http://semver.org/) para controle de versão. Para as versões disponíveis, observe as [tags neste repositório](https://github.com/suas/tags/do/projeto). 

## ✒️ Autores

Mencione todos aqueles que ajudaram a levantar o projeto desde o seu início

* **Um desenvolvedor** - *Trabalho Inicial* - [umdesenvolvedor](https://github.com/linkParaPerfil)
* **Fulano De Tal** - *Documentação* - [fulanodetal](https://github.com/linkParaPerfil)

Você também pode ver a lista de todos os [colaboradores](https://github.com/usuario/projeto/colaboradores) que participaram deste projeto.

## 📄 Licença

Este projeto está sob a licença (sua licença) - veja o arquivo [LICENSE.md](https://github.com/usuario/projeto/licenca) para detalhes.

## 🎁 Expressões de gratidão

* Conte a outras pessoas sobre este projeto 📢;
* Convide alguém da equipe para uma cerveja 🍺;
* Um agradecimento publicamente 🫂;
* etc.


---
⌨️ com ❤️ por [Armstrong Lohãns](https://gist.github.com/lohhans) 😊