"""
    - https://en.bitcoin.it/wiki/Transaction
    - https://developer.bitcoin.org/reference/transactions.html
    - https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki#commitment-structure
"""

import tools
import rpc

from opcode import B_OPCODE
from helper import _print

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
        witnessMerkleRootScript = tools.get_le_hex(B_OPCODE.OP_RETURN) + "24" + "aa21a9ed" + witnessMerkleRoot
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

def witness_merkleroot(transactions):
    hashs = []
    
    for transaction in transactions:
        dataDecode = rpc.decoderawtransaction(transaction['data'])['result']
        
        _print(f"Transaction Decode", f"{dataDecode}")
        
        # percorre todos os txinwitness de todos os vin
        for vin in dataDecode.get('vin'):
            if vin.get('txid') is not None:
                hashs.append(vin.get('txid'))
    
    if len(hashs) == 0:
        return {'has_witness' : False, 'witness_merkleroot' : None}
    
    # como sabemos que temos witness, adicionar a markle witness da coinbase
    hashs.insert(0, "00" * 32)
    
    witnessMerkleroot = tools.calc_merkle_root(hashs)
    
    _print(f"Hashs Witness", f"{hashs}")
    _print(f"witness Merkleroot", f"{witnessMerkleroot}")
    
    hasWitness = len(hashs) > 0
    
    return {'has_witness' : hasWitness, 'witness_merkleroot' : witnessMerkleroot}
        