import base64

# se DEBUG estiver em False, será exibido as informações apenas necessário
DEBUG = False

# se HAS_TIME_SLEEP estiver ativado, a cada novo bloco encontrado ou a cada nonce 
# esgotado, será dado um tempo para tentar novamente, se HAS_TIME_SLEEP for false
# esse tempo não existirá
HAS_TIME_SLEEP = True

# Define os parâmetros do RPC
parameters = {
    "host": "127.0.0.1",
    "port": "8332",
    "rpcuser": "Achcar",
    "rpcpass": "BCQ_DJMYDj-qhevMqthkK4suxmJq_tXht5fZxXXkoXY=",
    "rpcurl": "http://127.0.0.1:8332"
}

# Endereço da sua wallet para ganhar a recompensa do bitcoin e os fee
walletAddress = "tb1qzjylm68ntpyyvcgxcs5wcfytx4dcmwxhx9dg7h" 

# autenticação do RPC do Bitcoin core
auth = base64.b64encode(bytes(parameters["rpcuser"] + ":" + parameters["rpcpass"], "utf8"))