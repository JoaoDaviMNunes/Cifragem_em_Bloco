# João Davi
# Computer Systems Security
# UFRGS

# ====================== IMPORTS E CONSTANTES ======================

import sys
import os
from itertools import cycle
from math import ceil

# ====================== FUNÇÕES AUXILIARES ======================

def ajustar_caso(letra, referencia):
    return letra.upper() if referencia.isupper() else letra.lower()

def aplicar_xor(byte1, byte2):
    return byte1 ^ byte2

def pad(data, block_size):
    padding_length = block_size - (len(data) % block_size)
    return data + bytes([padding_length] * padding_length)

def unpad(data):
    padding_length = data[-1]
    return data[:-padding_length]

# ====================== CIFRAGENS ======================

# Cifra de Alberti
def cifragem_alberti(conteudo, chave):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    chave = chave.upper()
    texto_cifrado = []
    chave_expandida = (chave * (len(conteudo) // len(chave) + 1))[:len(conteudo)]

    for i in range(len(conteudo)):
        if conteudo[i].upper() in alfabeto:
            pos_texto = alfabeto.find(conteudo[i].upper())
            pos_chave = alfabeto.find(chave_expandida[i])
            pos_cifrada = (pos_texto + pos_chave) % len(alfabeto)
            texto_cifrado.append(ajustar_caso(alfabeto[pos_cifrada], conteudo[i]))
        else:
            texto_cifrado.append(conteudo[i])

    return ''.join(texto_cifrado)

# Cifra de Kamasutra
def criar_tabela_substituicao():
    alfabeto = 'abcdefghijklmnopqrstuvwxyz'
    primeira_metade = alfabeto[:13]
    segunda_metade = alfabeto[13:]
    tabela_criptografia = {}

    for i in range(len(primeira_metade)):
        tabela_criptografia[primeira_metade[i]] = segunda_metade[i]
        tabela_criptografia[segunda_metade[i]] = primeira_metade[i]

    return tabela_criptografia

def kama_cifra(texto):
    tabela_criptografia = criar_tabela_substituicao()
    texto_criptografado = []

    for char in texto:
        if char in tabela_criptografia:
            texto_criptografado.append(tabela_criptografia[char])
        else:
            texto_criptografado.append(char)

    return ''.join(texto_criptografado)

# Cifra de Vigenere
def expandir_palavra_chave(texto, chave):
    chave_expandida = []
    indice = 0

    for char in texto:
        if char.isalpha():
            chave_expandida.append(chave[indice % len(chave)])
            indice += 1
        else:
            chave_expandida.append(char)

    return ''.join(chave_expandida)

def coder_vigenere(texto, chave):
    texto_cifrado = []
    chave_expandida = expandir_palavra_chave(texto, chave)

    for i, char in enumerate(texto):
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            posicao_texto = ord(char) - base
            posicao_chave = ord(chave_expandida[i].lower()) - ord('a')
            char_cifrado = (posicao_texto + posicao_chave) % 26
            texto_cifrado.append(chr(char_cifrado + base))
        else:
            texto_cifrado.append(char)

    return ''.join(texto_cifrado)

# Cifra XOR
def cifragem_xor(bloco, chave):
    return bytes([aplicar_xor(bloco[i], chave[i % len(chave)]) for i in range(len(bloco))])

# Rodadas de Feistel
def rodadas_feistel(bloco, chave):
    metade = len(bloco) // 2
    esquerda = bloco[:metade]
    direita = bloco[metade:]

    for _ in range(2):
        nova_direita = bytes([aplicar_xor(e, k) for e, k in zip(esquerda, direita)])
        esquerda, direita = direita, nova_direita

    return esquerda + direita

# ====================== PROCESSAMENTO ======================

def cifrar_arquivo(entrada, saida, chave_ou_arquivo):
    with open(entrada, 'rb') as f:
        texto = f.read()

    if os.path.isfile(chave_ou_arquivo):
        with open(chave_ou_arquivo, 'r', encoding='utf-8') as f:
            palavra_chave = f.read().strip()
    else:
        palavra_chave = chave_ou_arquivo

    bloco_tam = 16
    texto = pad(texto, bloco_tam)
    blocos = [texto[i:i + bloco_tam] for i in range(0, len(texto), bloco_tam)]

    chaves = [palavra_chave.encode()] * len(blocos)
    blocos_cifrados = []

    for i, bloco in enumerate(blocos):
        bloco = coder_vigenere(bloco.decode(errors='ignore'), palavra_chave).encode()
        bloco = cifragem_xor(bloco, chaves[i])
        bloco = cifragem_alberti(bloco.decode(errors='ignore'), palavra_chave).encode()
        bloco = cifragem_xor(bloco, chaves[i])
        bloco = kama_cifra(bloco.decode(errors='ignore')).encode()
        bloco = rodadas_feistel(bloco, chaves[i])

        blocos_cifrados.append(bloco)

    with open(saida, 'wb') as f:
        f.write(b''.join(blocos_cifrados))

# ===================== EXECUÇÃO =====================
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso incorreto! Formato:")
        print("python3 cifragem.py <entrada> <saída> <chave ou arquivo de chave>")
        sys.exit(1)

    entrada = sys.argv[1]
    saida = sys.argv[2]
    chave = sys.argv[3]
    cifrar_arquivo(entrada, saida, chave)
    print("Cifragem realizada com sucesso!")
