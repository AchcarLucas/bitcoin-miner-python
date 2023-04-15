import tools
from opcode import B_OPCODE

"""
# https://developer.bitcoin.org/reference/transactions.html

01000000 .............................. Version

01 .................................... Number of inputs
| 00000000000000000000000000000000
| 00000000000000000000000000000000 ...  Previous outpoint TXID
| ffffffff ............................ Previous outpoint index
|
| 29 .................................. Bytes in coinbase
| |
| | 03 ................................ Bytes in height
| | | 4e0105 .......................... Height: 328014
| |
| | 062f503253482f0472d35454085fffed
| | f2400000f90f54696d65202620486561
| | 6c74682021 ........................ Arbitrary data
| 00000000 ............................ Sequence

01 .................................... Output count
| 2c37449500000000 .................... Satoshis (25.04275756 BTC)
| 1976a914a09be8040cbf399926aeb1f4
| 70c37d1341f3b46588ac ................ P2PKH script
| 00000000 ............................ Locktime

"""

# 19 76a914 a09be8040cbf399926aeb1f470c37d1341f3b465 88ac
# 19 76a914 93dfc045fcb43d7b0f1b5d327b0adc53e31ed9b9 + 88ac

def create_coinbase(
    coinbase_value: int, 
    coinbase_text: str, 
    block_height: int,
    scriptPubKey: str,
    witness_merkleroot : str = ""
) -> str:
    coinbase_script = tools.encode_coinbase_height(block_height) + coinbase_text

    #pubkey_script = "76a914" + scriptPubKey + "88ac"
    pubkey_script = (tools.get_le_hex(B_OPCODE.OP_DUP) 
                    + tools.get_le_hex(B_OPCODE.OP_HASH160) 
                    + tools.get_le_hex(len(scriptPubKey) // 2) 
                    + scriptPubKey 
                    + tools.get_le_hex(B_OPCODE.OP_EQUALVERIFY) 
                    + tools.get_le_hex(B_OPCODE.OP_CHECKSIG))
    
    return (
        "0200000001" + "0" * 64 + "ffffffff"
        + str(tools.get_le_var_hex(len(coinbase_script) // 2))
        + coinbase_script + "00000000" + "01" 
        + str(tools.get_le_hex(coinbase_value, 8))
        + str(tools.get_le_var_hex(len(pubkey_script) // 2))
        + pubkey_script
        + "00000000"
    )
    
# se ainda existir transactions faltando assinatura, não vamos tentar
def check_transactions(transactions):
    subtract_coinbase_fee = 0
    
    print(f"transactions {transactions}")
    
    transaction_to_delete = []
    
    for transaction in transactions:
        has_remove = False

        # não queremos transações que não deram fee
        if transaction['fee'] == 0:
            has_remove = True
            
        if has_remove:
            subtract_coinbase_fee += transaction['fee']
            transaction_to_delete.append(transaction)
        
    for delete_transaction in transaction_to_delete:
        transactions.remove(delete_transaction)
    
    return {'subtract_coinbase_fee' : subtract_coinbase_fee}

def witness_merkleroot(transactions):
    pass