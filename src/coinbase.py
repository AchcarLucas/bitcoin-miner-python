"""
    - Alguns links que me ajudaram bastante nesse projeto!!!!
        - https://en.bitcoin.it/wiki/Transaction
        - https://developer.bitcoin.org/reference/transactions.html
        - https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki#commitment-structure
        - https://coinsbench.com/building-blocks-of-bitcoin-mining-header-with-python-109bc505bdba
        - https://livebook.manning.com/book/grokking-bitcoin/chapter-5/
        - https://livebook.manning.com/book/grokking-bitcoin/chapter-10/1
        - Book Grokking Bitcoin (Help me so much)
"""
import tools
import rpc
import struct

from helper import _print, _empty
from opcode_bitcoin import B_OPCODE

def create_coinbase(
    coinbaseValue: int, 
    coinbaseText: str, 
    blockHeight: int,
    scriptPubKey: str,
    witnessMerkleRoot : str = None
) -> str:
    coinbaseScript = tools.encode_coinbase_height(blockHeight) + coinbaseText
    pubkeyScript = (tools.get_le_hex(B_OPCODE.OP_DUP) 
                    + tools.get_le_hex(B_OPCODE.OP_HASH160) 
                    + tools.get_le_hex(len(scriptPubKey) // 2) 
                    + scriptPubKey
                    + tools.get_le_hex(B_OPCODE.OP_EQUALVERIFY) 
                    + tools.get_le_hex(B_OPCODE.OP_CHECKSIG))
    
    # se não tivermos witness, temos apenas 1 output
    output = 0x01
    
    if witnessMerkleRoot is not None:
        witnessMerkleRootScript = tools.get_le_hex(B_OPCODE.OP_RETURN) + tools.get_le_hex(B_OPCODE.OP_PUSHBYTES_36) + "aa21a9ed" + witnessMerkleRoot
        # - witnessMerkleRootScript = witnessMerkleRoot
        # se considerar o witness, vamos ter 2 output
        output += 0x01
    
    # Criando a coinbase
    data = (
        # primeira input
        tools.get_le_hex(0x2, 0x04) + tools.get_le_var_hex(0x01) + "00" * 32 + tools.get_le_hex(0xffffffff, 0x04)
        + str(tools.get_le_var_hex(len(coinbaseScript) // 2))
        + coinbaseScript + tools.get_le_hex(0x0, 0x04)
        
        # quantidade de output na transação da coinbase
        + tools.get_le_hex(output)
        
        # nosso primeiro output (nosso reward + fee)
        + str(tools.get_le_hex(coinbaseValue, 8))
        + str(tools.get_le_var_hex(len(pubkeyScript) // 2))
        + pubkeyScript
    )
    
    # se existir o Markle Root do Witness, adiciona na coinbase
    if witnessMerkleRoot is not None:
        data += (
                # nosso segundo output (witness)
                str(tools.get_le_hex(0, 8))
                + str(tools.get_le_var_hex(
                            (len(witnessMerkleRootScript) // 2))
                      )
                + witnessMerkleRootScript
                )
        
    # if non-zero and sequence numbers are < 0xFFFFFFFF: block height or timestamp when transaction is final
    data += tools.get_le_hex(0x0, 0x04)
        
    return data

def calc_block_header(block: dict) -> bytes:
    return (
        struct.pack("<L", block["version"])
        + bytes.fromhex(block["previousblockhash"])[::-1]
        + bytes.fromhex(block["merkleroot"])[::-1]
        + struct.pack("<L", block["curtime"])
        + bytes.fromhex(block["bits"])[::-1]
        + struct.pack("<L", block["nonce"])
    )
    
# se ainda existir transactions faltando assinatura, não vamos tentar
def filter_transactions(transactions):
    subtractCoinbaseFee = 0
    
    transactionToDelete = []
    
    for transaction in transactions:
        hasRemove = False

        # não queremos transações que não deram fee
        if transaction['fee'] == 0:
            hasRemove = True
            
        if hasRemove:
            subtractCoinbaseFee += transaction['fee']
            transactionToDelete.append(transaction)
        
    for delete_transaction in transactionToDelete:
        transactions.remove(delete_transaction)
    
    return {'subtract_coinbase_fee' : subtractCoinbaseFee}

def main_markeroot(transactions):
     # var para guardar as hashs para a criação do markle root
    hashs = []
    
    # vamos agora percorrer as transações e obter as txids para a geração da markle root
    # o processo é o mesmo que a criação do markle root da witness
    for transaction in transactions:
        if transaction.get('txid') is not None:
            hashs.append(transaction['txid'])
        else:
            hashs.append(transaction['hash'])
            
    _print(f"Hashs txid", f"{hashs}")
    
    return {'main_merkleroot' : tools.calc_merkle_root(hashs)}

"""
    Cria a witness commitment para a coinbase
"""
def witness_merkleroot(transactions):
    hashs = []
    
    for transaction in transactions:
        hashs.append(transaction['hash'])
    
    if len(hashs) == 0:
        return {'has_witness' : False, 'witness_merkleroot' : None}
    
    # como sabemos que temos witness, adicionar a markle witness da coinbase
    # o da coinbase é o primeiro da lista
    hashs.insert(0, "00" * 32)
    
    witnessMerkleroot = tools.calc_markle_witness(hashs)
    
    _print(f"Hashs Witness", f"{hashs}")
    _print(f"Witness Merkleroot", f"{witnessMerkleroot}")
    
    hasWitness = len(hashs) > 0
    
    return {'has_witness' : hasWitness, 'witness_merkleroot' : witnessMerkleroot}