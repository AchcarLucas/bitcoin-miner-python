from essential_generators import DocumentGenerator

import coinbase
import binascii
import rpc
import tools
import config
import binascii
import time
import random

from helper import _print

def miner():
    # vamos obter pelo RPC do Bitcoin Core ou outro a mempool de um bloco ainda não minerado
    blockTemplate = rpc.get_block_template()['result']
    scriptPubKey = rpc.validate_address(config.walletAddress)['result']['witness_program']
    
    _print(f"Miner", f"miner the block {blockTemplate['height']} ... ")
    
    # faz o filtro das transactions que a gente desejar
    result = coinbase.filter_transactions(blockTemplate['transactions'])
    # faz a subtração das informações que foram eliminadas na etapa de verificação das transações
    blockTemplate['coinbasevalue'] -= result['subtract_coinbase_fee']

    _print(f"Transactions", f"{blockTemplate['transactions']}")

    # calcula o target - qual é a dificuldade do bloco
    targetHash = tools.calc_target(blockTemplate['bits'])
    targetHash = binascii.hexlify(targetHash).decode("utf-8")
    
    _print(f"Target", f'{targetHash} with {tools.count_zeros_left(targetHash)} zeros')
    
    # vamos calcular agora o witness markle root para colocar no final da coinbase
    # essa parte é necessário para conseguirmos validar transações com Segwit (witness)
    witnessMarkleRootResult = coinbase.witness_merkleroot(blockTemplate['transactions'])

    # criação da coinbase
    coinBase = {}
    
    #coinbaseText: str = DocumentGenerator().sentence().encode().hex()
    coinbaseText: str = "test".encode().hex()

    # aqui já temos tudo que é necessário para criar a coinbase
    coinBase['data'] = coinbase.create_coinbase(
        coinbaseValue=blockTemplate['coinbasevalue'],  
        coinbaseText=coinbaseText, 
        blockHeight=blockTemplate['height'],
        scriptPubKey=scriptPubKey,
        #witnessMerkleRoot=blockTemplate['default_witness_commitment']
        witnessMerkleRoot=witnessMarkleRootResult['witness_merkleroot']
    )

    # criação da hash dentro da coinbase
    coinBase['hash'] = tools.sha256_double_hash(binascii.unhexlify(coinBase['data']))
    
    _print(f'Coin Base', f"{coinBase}")
    
    """
        vamos inserir o bloco nas transactions, a coinbase será a primeira transação
        calculamos a main marke root para adicionar dentro do bloco principal
        adicionamos o primeiro nonce
    """
    
    blockTemplate['transactions'].insert(0, coinBase)
    blockTemplate['merkleroot'] = coinbase.main_markeroot(blockTemplate['transactions'])['main_merkleroot']
    blockTemplate['nonce'] = 0

    """
        aqui já temos o nosso bloco pronto para a mineração
            - já está com a nossa coinbase
            - já está com as markle root criadas
            - já está com a nonce, agora basta achar a solução
    """
    _print(f"blockTemplate", f"{blockTemplate}")
    
    targetZeros = tools.count_zeros_left(targetHash)
    
    # vamos começar a minerar o bloco, modificando apenas a nonce
    for nonce in range(0, 0xfffffffff):
        blockTemplate['nonce'] = random.randrange(0xff, 0xffffffff)
        
        # criamos o header e depois seu duplo sha256
        blockHeader = coinbase.calc_block_header(blockTemplate)        
        blockHash = tools.sha256_double_hash(blockHeader)
        
        # verificamos a quantidade de zeros a esquerda (é a nossa dificuldade)
        blockZeros = tools.count_zeros_left(blockHash)

        # vamos exibir apenas complexidades maiores que 5 para não ocorrer spam
        if blockZeros > 5 or nonce == 0:
            _print(f"blockHash", f"{blockHash} - zeros {blockZeros} - reach {targetZeros} - nonce {blockTemplate['nonce']}")

        # se o bloco tiver a complexade do target, encontramos a solução, basta submeter 
        # ao bitcoin core ou outro RPC que esteja usando
        if blockZeros > targetZeros:
            _print("Success", "We find an solution target")
            
            _print(f"Submit", f"{blockTemplate}")
            
            rpc.submit_block(blockTemplate)
            break
   
if __name__ == "__main__":
    while True:
        minersCount = 0
        miner()
        minersCount += 1
        time.sleep(10)
