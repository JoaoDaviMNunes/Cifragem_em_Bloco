from itertools import cycle
import cipher_vigenere
import cipher_alberti
import cipher_kamasutra

def kamasutra_decrypt(text, key):
    # Implementação simplificada da cifra Kamasutra
    return text.translate(str.maketrans(key[::-1], key))

def unpad(text):
    padding_len = ord(text[-1])
    return text[:-padding_len]

def decrypt_file(input_file, output_file):
    with open(input_file, 'r') as f:
        text = f.read()
    
    block_size = 16
    blocks = [text[i:i+block_size] for i in range(0, len(text), block_size)]
    
    keys = ['VIGENEREKEY', 'ALBERTIKEY', 'KAMASUTRAKEY']
    ciphers = [cipher_vigenere.decoder_vigenere, cipher_alberti.decifragem_alberti, cipher_kamasutra.kama_decifra]
    
    decrypted_blocks = []
    for i, block in enumerate(blocks):
        cipher = ciphers[i % len(ciphers)]
        key = keys[i % len(keys)]
        decrypted_blocks.append(cipher(block, key))
    
    decrypted_text = unpad(''.join(decrypted_blocks))
    
    with open(output_file, 'w') as f:
        f.write(decrypted_text)

decrypt_file('saida.txt', 'final.txt')
