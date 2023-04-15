from essential_generators import DocumentGenerator

import coinbase
import binascii
import rpc
import tools
import config
import binascii
import time
import random
    
def miner():
    block_template = rpc.getblocktemplate()['result']
    validate_address = rpc.validateaddress(config.wallet_address)['result']
    scriptPubKey = validate_address['witness_program']
    
    result = coinbase.check_transactions(block_template['transactions'])
    
    # faz a subtração das informações que foram eliminadas na etapa de verificação das transações
    block_template['coinbasevalue'] -= result['subtract_coinbase_fee']

    target_hash = tools.calc_target(block_template['bits'])
    target_hash = binascii.hexlify(target_hash).decode("utf-8")

    print(f'Target {target_hash} - Zeros {tools.count_left_zeros(target_hash)}')

    _coinbase = {}
    #coinbase_text: str = DocumentGenerator().sentence().encode().hex()
    coinbase_text: str = "test".encode().hex()

    _coinbase['data'] = coinbase.create_coinbase(
        coinbase_value=block_template['coinbasevalue'],  
        coinbase_text=coinbase_text, 
        block_height=block_template['height'],
        scriptPubKey=scriptPubKey, 
    )

    _coinbase['hash'] = tools.sha256_double_hash(binascii.unhexlify(_coinbase['data']))
    
    block_template['transactions'].insert(0, _coinbase)
    
    hashs = []
    
    for transaction in block_template['transactions']:
        if transaction.get('txid') is not None:
            hashs.append(transaction['txid'])
        else:
            hashs.append(transaction['hash'])
            
    print("*" * 60)
    print(f"merkle_root hashs {hashs}")
    print("*" * 60)
    
    block_template['merkleroot'] = tools.calc_merkle_root(hashs)

    block_template['nonce'] = 0

    print("*" * 60)
    print(block_template)
    print("*" * 60)
    print("*" * 60)
    
    target_zeros = tools.count_left_zeros(target_hash)
    
    for nonce in range(0, 0xfffffffff):
        block_template['nonce'] = random.randrange(0xff, 0xffffffff)
        block_header = tools.calc_block_header(block_template)        
        block_hash = tools.sha256_double_hash(block_header)

        block_zeros = tools.count_left_zeros(block_hash)

        if block_zeros > 5 or nonce == 0:
            print(f"block_hash {block_hash} - zeros {block_zeros} - reach {target_zeros} - nonce {block_template['nonce']}")

        if block_zeros > target_zeros:
            print("achou!")
            print("*"*60) 
            print(f"block_header {block_header.hex()}")
            print("*"*60)
            print(f"submit - {block_template}")
            print("*" * 60)
            rpc.submitblock(block_template)
            break
   
while True:
    c_miners = 0
    print(f"minerando ... ")
    miner()
    c_miners += 1
    print(f"minerado {c_miners} ")
    time.sleep(10)
