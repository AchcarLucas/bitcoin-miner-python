# Bitcoin Miner Python 

Esse projeto foi feito como uma forma de eu aprender um pouco mais sobre o bitcoin e suas estruturas, acabei focando bastante na parte da mineração 
pois é uma área que eu gosto muito

## 🚀 Começando

Nesse projeto, acabei usando algumas fontes de consulta, são essas:

```
- https://en.bitcoin.it/wiki/Transaction
- https://developer.bitcoin.org/reference/transactions.html
- https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki#commitment-structure
- https://coinsbench.com/building-blocks-of-bitcoin-mining-header-with-python-109bc505bdba
- https://livebook.manning.com/book/grokking-bitcoin/chapter-5/
- https://livebook.manning.com/book/grokking-bitcoin/chapter-10/1
- Livro Grokking Bitcoin
```

O livro Grokking Bitcoin e muito bom e mostra em detalhes como funciona os processos do bitcoin, desde a criação da transações, criação da mempool e a mineração, recomendo demais :)

### 📋 Pré-requisitos

Como eu fiz o projeto do zero, acabou que não necessitou a utilização de quase nenhuma biblioteca externa, são elas:

```
base64
binascii
hashlib
random
json
struct
time
```

A única instalação obrigatória é a do essential_generators

```pip install essential_generators```

### 🔧 Instalação

Como a mineração do bitcoin na mainnet (rede principal do bitcoin) é bastante dificil, podemos
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
baixa o script e execute o seguinte comando ```python3 rpcauth.py <username> <password>``` a saída já é sua rpcauth no padrão no bitcoin core.
Outra alternativa é usar o seguinte site: https://jlopp.github.io/bitcoin-core-rpc-auth-generator/ que faz a geração do rpcauth para você.

Bom, depois que você configurou o arquivo ```.conf```, salva e reinicie o bitcoin core, você irá perceber que a cor mudou para o azul, parabéns, você está na regtest.

OBS: se desejar voltar para a mainnet, basta apagar tudo do .config e reabrir o bitcoin core

Um outro detalhe, é normal o bitcoin core não conectar e aparecer uma quantidade de anos pois o único nó é ele, quando você começar a minerar, esse problema irá desaparecer

## ⚙️ Executando os testes

Dentro do bitcoin core, crie uma wallet e depois um endereço para receber as recomenpas do bloco. Depois que você criou o endereço, faça a copia da chave pública para dentro do arquivo de configuração do python ```config.py``` na parte

```
    walletAddress = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 
```

Onde está` ```xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx``` adicione sua chave pública onde será recebido os bitcoins de recompennsas por encontrar o bloco e todas as fee (taxas) de todas as transações efetuadas no bloco

Além disso, ainda na ```config.py``` na parte

``` 
"host": "127.0.0.1",
"port": "8332",
"rpcuser": "Achcar",
"rpcpass": "BCQ_DJMYDj-qhevMqthkK4suxmJq_tXht5fZxXXkoXY=",
"rpcurl": "http://127.0.0.1:8332"
```

configure o rpcuser e o rpcpass, lembrando, o rpcpass não é a codificado, é a sua rpcpass que foi usado para gerar a codificação

### 🔩 Vamos minerar!!!

Estamos quase lá, com tudo configurado, execute o mineradoor usando python miner.py dentro de src e pronto, a cada 1 segundo (se quiser gerar por um tempo maior, mude o time.sleep no arquivo principal ```miner.py```) um bloco novo será gerado, lembra o walletAddress configurado ? os bitcoins irão aparecer lá a cada novo bloco minerado, um outro detalhe, só é possível usar os bitcoins de blocos minerados após 100 confirmações, então, deixe fazer a mineração antes de fazer transações na regtest

### 👀 Condiderações finais

Agora, com essa ideia em mente, o próximo passo será a criação de um rig de mineração usando FPGA e Verilog, mas ai já são projetos futuros :)

Bom, se alguém tiver alguma dúvida ou mesmo precisa de alguma ajuda, entre em contato comigo pelo e-mail: achcarlucas@gmail.com

#### by Lucas Campos Achcar
