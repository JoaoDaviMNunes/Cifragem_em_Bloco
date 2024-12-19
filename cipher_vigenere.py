# João Davi
# Computer Systems Security
# UFRGS

# ====================== IMPORTS ======================
import os
from itertools import cycle
from unicodedata import normalize

# ====================== FUNÇÕES AUXILIARES ======================

def ajustar_caso(letra, referencia):
    return letra.upper() if referencia.isupper() else letra.lower()

def expandir_palavra_chave(texto, palavra_chave):
    palavra_chave_expandida = []
    indice_palavra_chave = 0
    for char in texto:
        if char.isalpha():
            palavra_chave_expandida.append(palavra_chave[indice_palavra_chave])
            indice_palavra_chave = (indice_palavra_chave + 1) % len(palavra_chave)
        else:
            palavra_chave_expandida.append(char)
    return ''.join(palavra_chave_expandida)

def pad(text, block_size):
    padding_len = block_size - (len(text) % block_size)
    return text + chr(padding_len) * padding_len

def coder_vigenere(texto_claro, palavra_chave):
    texto_cifrado = []
    palavra_chave_repetida = expandir_palavra_chave(texto_claro, palavra_chave)
    indice_palavra_chave = 0
    
    for char in texto_claro:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            posicao_texto = ord(char) - base
            posicao_palavra_chave = ord(palavra_chave_repetida[indice_palavra_chave].lower()) - ord("a")
            
            char_cifrado = (posicao_texto + posicao_palavra_chave) % 26
            letra_cifrada = chr(char_cifrado + base)
            texto_cifrado.append(letra_cifrada)
        else:
            texto_cifrado.append(char)
        indice_palavra_chave += 1
        
    return ''.join(texto_cifrado)

def unpad(text):
    padding_len = ord(text[-1])
    return text[:-padding_len]

def decoder_vigenere(texto_cifrado, palavra_chave):
    texto_decifrado = []
    palavra_chave_repetida = expandir_palavra_chave(texto_cifrado, palavra_chave)
    indice_palavra_chave = 0
    
    for char in texto_cifrado:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            posicao_texto = ord(char) - base
            posicao_palavra_chave = ord(palavra_chave_repetida[indice_palavra_chave].lower()) - ord("a")
            
            indice_decifrado = (posicao_texto - posicao_palavra_chave + 26) % 26
            letra_decifrada = chr(indice_decifrado + base)
            texto_decifrado.append(letra_decifrada)
        else:
            texto_decifrado.append(char)
        indice_palavra_chave += 1
        
    return ''.join(texto_decifrado)