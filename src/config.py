import base64

# Define parameters for the RPC.
parameters = {
    "host": "127.0.0.1",
    "port": "8332",
    "rpcuser": "Achcar",
    "rpcpass": "BCQ_DJMYDj-qhevMqthkK4suxmJq_tXht5fZxXXkoXY=",
    "rpcurl": "http://127.0.0.1:8332"
}

walletAddress = "bcrt1quxf69e6pwjxkq9cm8pyk7dju636w8r873pncg2" 

auth = base64.b64encode(bytes(parameters["rpcuser"] + ":" + parameters["rpcpass"], "utf8"))