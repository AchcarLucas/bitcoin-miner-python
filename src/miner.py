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
from config import HAS_TIME_SLEEP

def miner():
    # vamos obter pelo RPC do Bitcoin Core ou outro a mempool de um bloco ainda não minerado
    blockTemplate = rpc.get_block_template()['result']
    scriptPubKey = rpc.validate_address(config.walletAddress)['result']['witness_program']
    
    _print(f"Miner", f"miner the block {blockTemplate['height']} ... ", True)
    
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
    
    # aqui temos um extranonce para podermos trabalhar, caso a nonce chegar ao fim dos 0x7fffffff
    # alteramos essa parte
    coinbaseText: str = ("/achcar-miner/" + DocumentGenerator().sentence()).encode().hex()

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
    _print(f"Transactions", f"{len(blockTemplate['transactions'])}", True)
    
    targetZeros = tools.count_zeros_left(targetHash)
    
    lastTime = 0
    hashsPerSecond = 0
    hasFound = False
    alreadyMiner = False
    
    verifyWithSecond = 10.0
    
    # vamos começar a minerar o bloco, modificando apenas a nonce
    for nonce in range(0, 0x7fffffff):
        blockTemplate['nonce'] = nonce
        
        # criamos o header e depois seu duplo sha256
        blockHeader = coinbase.calc_block_header(blockTemplate)        
        blockHash = tools.sha256_double_hash(blockHeader)
        
        # verificamos a quantidade de zeros a esquerda (é a nossa dificuldade)
        blockZeros = tools.count_zeros_left(blockHash)

        # vamos exibir apenas complexidades maiores que 5 para não ocorrer spam
        if blockZeros > 5 or nonce == 0:
            _print(f"blockHash", f"{blockHash} - zeros {blockZeros} - reach {targetZeros} - nonce {blockTemplate['nonce']}", True)
            
        # exibir a quantidade de hashs por segundo do nosso minerador
        if (time.time() - lastTime) > verifyWithSecond:
            # vamos verificar se o bloco já foi minerado, se sim, vamos sair do for para ele tentar o outro bloco
            blockchain_info = rpc.get_blockchain_info()['result']
            
            # se o bloco da informação for maior que o da altura minerado menos 1, então, basta sair, pois o 
            # bloco já foi minerado
            if(blockchain_info['blocks'] > blockTemplate['height'] - 1):
                _print(f"Stop Miner", f"Block {blockTemplate['height']} already miner", True)
                alreadyMiner = True
                break
            
            _print(f"Hash Rate", f"{hashsPerSecond / verifyWithSecond} Hashs/s - Current Nonce {hex(nonce)}", True)
            hashsPerSecond = 0
            lastTime = time.time()

        # se o bloco tiver a complexade do target, encontramos a solução, basta submeter 
        # ao bitcoin core ou outro RPC que esteja usando
        if blockZeros > targetZeros:
            rpc.submit_block(blockTemplate)
            
            hasFound = True
            
            _print("Success", "We find an solution target", True)
            _print(f"Submit", f"{blockTemplate}", True)
            
            break
        
        hashsPerSecond += 1
        
    if not hasFound and not alreadyMiner:
        _print("Warning", "Exhausted nonce - try create new basecoin with new informations", True)
   
if __name__ == "__main__":
    while True:
        minersCount = 0
        miner()
        minersCount += 1
        if HAS_TIME_SLEEP:
            time.sleep(10)
