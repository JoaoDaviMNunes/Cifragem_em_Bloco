# João Davi
# Computer Systems Security
# UFRGS

# ====================== IMPORTS E CONSTANTES ======================

from itertools import cycle
import cipher_vigenere
import cipher_alberti
import cipher_kamasutra

def kamasutra_encrypt(text, key):
    # Implementação simplificada da cifra Kamasutra
    return text.translate(str.maketrans(key, key[::-1]))

def pad(text, block_size):
    padding_len = block_size - (len(text) % block_size)
    return text + chr(padding_len) * padding_len

def encrypt_file(input_file, output_file):
    with open(input_file, 'r') as f:
        text = f.read()
    
    block_size = 16
    text = pad(text, block_size)
    blocks = [text[i:i+block_size] for i in range(0, len(text), block_size)]
    
    keys = ['VIGENEREKEY', 'ALBERTIKEY', 'KAMASUTRAKEY']
    ciphers = [cipher_vigenere.coder_vigenere, cipher_alberti.cifragem_alberti, cipher_kamasutra.kama_cifra]
    
    encrypted_blocks = []
    for i, block in enumerate(blocks):
        cipher = ciphers[i % len(ciphers)]
        key = keys[i % len(keys)]
        encrypted_blocks.append(cipher(block, key))
    
    with open(output_file, 'w') as f:
        f.write(''.join(encrypted_blocks))

encrypt_file('entrada.txt', 'saida.txt')
