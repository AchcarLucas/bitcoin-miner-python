from essential_generators import DocumentGenerator

import coinbase
import binascii
import rpc
import tools
import config
import binascii
import time
import random

def _print(content):
    print('*' * 60 + '\n - ' + content + '\n' + '*' * 60)
    
def miner():
    # vamos obter pelo RPC do Bitcoin Core ou outro a mempool de um bloco ainda não minerado
    blockTemplate = rpc.getblocktemplate()['result']
    scriptPubKey = rpc.validateaddress(config.wallet_address)['result']['witness_program']
    
    # faz o filtro das transactions que a gente desejar
    result = coinbase.filter_transactions(blockTemplate['transactions'])
    
    # faz a subtração das informações que foram eliminadas na etapa de verificação das transações
    blockTemplate['coinbasevalue'] -= result['subtract_coinbase_fee']

    # calcula o target - qual é a dificuldade do bloco
    target_hash = tools.calc_target(blockTemplate['bits'])
    target_hash = binascii.hexlify(target_hash).decode("utf-8")
    
    _print(f'Target {target_hash} - Zeros {tools.count_left_zeros(target_hash)}')

    # criação da coinbase
    _coinbase = {}
    
    #coinbase_text: str = DocumentGenerator().sentence().encode().hex()
    coinbase_text: str = "test".encode().hex()

    _coinbase['data'] = coinbase.create_coinbase(
        coinbase_value=blockTemplate['coinbasevalue'],  
        coinbase_text=coinbase_text, 
        block_height=blockTemplate['height'],
        scriptPubKey=scriptPubKey
    )

    # criação da hash dentro da coinbase
    _coinbase['hash'] = tools.sha256_double_hash(binascii.unhexlify(_coinbase['data']))
    
    # vamos inserir o bloco nas transactions, a coinbase será a primeira transação
    blockTemplate['transactions'].insert(0, _coinbase)
    
    # var para guardar as hashs para a criação do markle root
    hashs = []
    
    # vamos agora percorrer as transações e obter as txids para a geração da markle root
    # o processo é o mesmo que a criação do markle root da witness
    for transaction in blockTemplate['transactions']:
        if transaction.get('txid') is not None:
            hashs.append(transaction['txid'])
        else:
            hashs.append(transaction['hash'])
            
    _print(f"merkle_root hashs {hashs}")
    
    # adicionamos a markleroot criada no bloco principal
    blockTemplate['merkleroot'] = tools.calc_merkle_root(hashs)

    # adicionamos o primeiro nonce
    blockTemplate['nonce'] = 0

    # aqui já temos o nosso bloco pronto para a mineração
    # já está com a nossa coinbase
    # já está com as markle root criadas
    # já está com a nonce, agora basta achar a solução
    _print(blockTemplate)
    
    targetZeros = tools.count_left_zeros(target_hash)
    
    # vamos começar a minerar o bloco, modificando apenas a nonce
    for nonce in range(0, 0xfffffffff):
        blockTemplate['nonce'] = random.randrange(0xff, 0xffffffff)
        blockHeader = tools.calc_block_header(blockTemplate)        
        blockHash = tools.sha256_double_hash(blockHeader)

        blockZeros = tools.count_left_zeros(blockHash)

        # vamos exibir apenas complexidades maiores que 5 para não ocorrer spam
        if blockZeros > 5 or nonce == 0:
            _print(f"block_hash {blockHash} - zeros {blockZeros} - reach {targetZeros} - nonce {blockTemplate['nonce']}")

        # se o bloco tiver a complexade do target, encontramos a solução, basta submeter 
        # ao bitcoin core ou outro RPC que esteja usando
        if blockZeros > targetZeros:
            _print("find an solution target")
            
            _print(f"blockHash {blockHash.hex()}")
            _print(f"submit - {blockTemplate}")
            
            rpc.submitblock(blockTemplate)
            break
   
while True:
    c_miners = 0
    _print(f"minerando ... ")
    miner()
    c_miners += 1
    time.sleep(10)
