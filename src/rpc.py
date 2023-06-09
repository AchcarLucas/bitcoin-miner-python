import tools
import coinbase
import json
import random
import base64
import urllib.request
import urllib.error
import urllib.parse

import config

from helper import _print

def request_rpc(data):
    request = urllib.request.Request(
        config.parameters["rpcurl"], 
        data, 
        {"Authorization": b"Basic " + config.auth}
    )
    
    # Send the RPC and parse response.
    with urllib.request.urlopen(request) as f:
        response = json.loads(f.read())
        
    return response
    
def get_block_template():
    rpc_id = random.getrandbits(32)
    
    data = json.dumps({
        "id": rpc_id, 
        "method": "getblocktemplate", 
        "params": [{"rules": ["segwit"]}]
    }).encode()
    
    return request_rpc(data)
    
def validate_address(address):
    rpc_id = random.getrandbits(32)
    
    data = json.dumps({
        "id": rpc_id, 
        "method": "validateaddress", 
        "params": [address]
    }).encode()
    
    return request_rpc(data)

def get_blockchain_info():
    rpc_id = random.getrandbits(32)
    
    data = json.dumps({
        "id": rpc_id, 
        "method": "getblockchaininfo", 
        "params": []
    }).encode()
    
    return request_rpc(data)

def decode_raw_transaction(data : str) -> dict:
    rpc_id = random.getrandbits(32)
    
    data = json.dumps({
        "id": rpc_id, 
        "method": "decoderawtransaction",
        "params": [data]
    }).encode()
    
    return request_rpc(data)
    
def submit_block(block: dict) -> str:
    submission = (
        coinbase.calc_block_header(block).hex() 
        + tools.get_le_var_hex(len(block['transactions']))
    )
    for tx in block['transactions']:
        submission += tx['data']
       
    _print(f"Data Submit", f"{submission}")

    rpc_id = random.getrandbits(32)
    
    data = json.dumps({
        "id": rpc_id, 
        "method": "submitblock", 
        "params": [submission]
    }).encode()
    
    auth = base64.b64encode(bytes(
        config.parameters["rpcuser"] + ":" + config.parameters["rpcpass"], 
        "utf8"
    ))
    
    request = urllib.request.Request(
        config.parameters["rpcurl"], 
        data, 
        {"Authorization": b"Basic " + auth}
    )

    # Send the RPC and parse response.
    with urllib.request.urlopen(request) as f:
        response = json.loads(f.read())
        _print(f"Response Submit", f"{response}", True)