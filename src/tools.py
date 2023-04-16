import hashlib
import binascii

from helper import _print
    
def sha256_double_hash(target: str, invert : bool = True) -> str:
    sha256d_value = hashlib.sha256(hashlib.sha256(target).digest()).digest()
    
    if invert:
        sha256d_value = sha256d_value[::-1]

    return binascii.hexlify(sha256d_value).decode("utf-8")

def sha256_hash(target: str, invert : bool = True) -> str:
    sha256d_value = hashlib.sha256(target).digest()
    
    if invert:
        sha256d_value = sha256d_value[::-1]
        
    return binascii.hexlify(sha256d_value).decode("utf-8")

def calc_markle_witness(hashs: list[str]):
    # Convert transactions into big-endian bytes.
    
    _print("hash len", f"{len(hashs)}")
    
    keep_first = hashs[0]
    keep_last = hashs[-1]
    
    be_hashes = [
        bytes.fromhex(hash)[::-1]
        for hash in hashs
    ]
    
    be_hashes[0] = bytes.fromhex(keep_first)[::-1]
    be_hashes[-1] = bytes.fromhex(keep_last)[::-1]

    # We combine the hashes pairwise until there is only 1 left.
    while len(be_hashes) > 1:

        # Duplicate the last hash if the list size is odd.
        if len(be_hashes) % 2 != 0:
            be_hashes.append(be_hashes[-1])

        # Combine the hashes pairwise. 
        for i in range(len(be_hashes) // 2):
            concat_hash = be_hashes[i * 2] + be_hashes[i * 2 + 1]
            _print(f"hashs", f"{binascii.hexlify(concat_hash).decode('utf-8')}")
            be_hash = hashlib.sha256(hashlib.sha256(concat_hash).digest()).digest()
            be_hashes[i] = be_hash
            
        be_hashes = be_hashes[:len(be_hashes) // 2]
        
    _print(f"last hash", f"{binascii.hexlify(be_hashes[0]).decode('utf-8')}")
    
    witnessReservedValue = ("00" * 32)
    witnessLastHash = binascii.hexlify(be_hashes[0]).decode('utf-8') + witnessReservedValue
    
    _print(f"last hash with txid coinbase", f"{(bytes.fromhex(witnessLastHash)).hex()}")
    
    resultWitnessLastHash = sha256_double_hash(binascii.unhexlify(witnessLastHash), invert=False)
    
    _print(f"last hash", f"{(bytes.fromhex(resultWitnessLastHash)).hex()}")
    
    return resultWitnessLastHash
    
def calc_merkle_root(hashs: list[str]) -> str:
    # Convert transactions into big-endian bytes.
    be_hashes = [
        bytes.fromhex(hash)[::-1]
        for hash in hashs
    ]

    # We combine the hashes pairwise until there is only 1 left.
    while len(be_hashes) > 1:

        # Duplicate the last hash if the list size is odd.
        if len(be_hashes) % 2 != 0:
            be_hashes.append(be_hashes[-1])

        # Combine the hashes pairwise. 
        for i in range(len(be_hashes) // 2):
            concat_hash = be_hashes[i * 2] + be_hashes[i * 2 + 1]
            be_hash = hashlib.sha256(hashlib.sha256(concat_hash).digest()).digest()
            be_hashes[i] = be_hash
        be_hashes = be_hashes[:len(be_hashes) // 2]
    return be_hashes[0][::-1].hex()
    
def calc_target(bits: str) -> bytes:
    """
    Decompress the target from a compact format.
    """
    bits = bytes.fromhex(bits)

    # Extract the parts.
    byte_length = bits[0] - 3
    significand = bits[1:]

    # Scale the significand by byte_length.
    target = significand + b"\x00" * byte_length

    # Fill in the leading zeros.
    target = b"\x00" * (32 - len(target)) + target

    return target

def get_le_hex(value: int, width: int = 1) -> str:
    return value.to_bytes(width, byteorder='little').hex()

def get_le_var_hex(value: int) -> str:
    if value < 0xfd:
        return get_le_hex(value)
    if value <= 0xffff:
        return "fd" + get_le_hex(value, 2)
    if value <= 0xffffffff:
        return "fe" + get_le_hex(value, 4)
    return "ff" + get_le_hex(value, 8)

def encode_coinbase_height(height: int) -> str:
    """
    https://github.com/bitcoin/bips/blob/master/bip-0034.mediawiki
    """
    width = (height.bit_length() + 7) // 8
    return bytes([width]).hex() + get_le_hex(height, width)

def count_zeros_left(text : str):
    _count = 0
    for letter in text:
        if letter == '0':
           _count += 1
           continue
        break
    return _count