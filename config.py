import base64

# Define parameters for the RPC.
parameters = {
    "host": "127.0.0.1",
    "port": "8332",
    "rpcuser": "Achcar",
    "rpcpass": "BCQ_DJMYDj-qhevMqthkK4suxmJq_tXht5fZxXXkoXY=",
    "rpcurl": "http://127.0.0.1:8332"
}

wallet_address = "bcrt1quxf69e6pwjxkq9cm8pyk7dju636w8r873pncg2"

# 70c37d1341f3b46588ac 

auth = base64.b64encode(bytes(parameters["rpcuser"] + ":" + parameters["rpcpass"], "utf8"))