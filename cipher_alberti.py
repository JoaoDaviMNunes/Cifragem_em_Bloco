# Código de Diego Ferreira Duarte
# Adaptação por João Davi Martins Nunes
# Parte da Cifragem em Bloco

import sys
import os
from unicodedata import normalize

# ====================== FUNÇÕES AUXILIARES ======================

def ajustar_caso(letra, referencia):
    return letra.upper() if referencia.isupper() else letra.lower()

# ====================== FUNÇÕES PRINCIPAIS ======================

# Função para cifrar texto usando o método baseado na cifra de Alberti
def cifragem_alberti(conteudo, key):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'  # Alfabeto alfanumérico
    key = key.upper()  # Coloca a chave em maiúsculo
    texto_cifrado = []

    # Expande a chave para ter o mesmo tamanho do conteúdo
    chave_expandida = (key * (len(conteudo) // len(key) + 1))[:len(conteudo)]

    for i in range(len(conteudo)):
        if conteudo[i].upper() in alfabeto:
            pos_texto = alfabeto.find(conteudo[i].upper())
            pos_chave = alfabeto.find(chave_expandida[i])
            pos_cifrada = (pos_texto + pos_chave) % len(alfabeto)
            texto_cifrado.append(ajustar_caso(alfabeto[pos_cifrada], conteudo[i]))
        else:
            # Se o caractere não estiver no alfabeto, adicioná-lo sem cifragem
            texto_cifrado.append(conteudo[i])

    return ''.join(texto_cifrado)

# FUNCAO PARA DECIFRAR TEXTO
def decifragem_alberti(text, key):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    key = key.upper()
    texto_decifrado = []

    chave_expandida = (key * (len(text) // len(key) + 1))[:len(text)]

    for i in range(len(text)):
        if text[i].upper() in alfabeto:
            pos_texto = alfabeto.find(text[i].upper())
            pos_chave = alfabeto.find(chave_expandida[i])
            pos_decifrada = (pos_texto - pos_chave) % len(alfabeto)
            texto_decifrado.append(ajustar_caso(alfabeto[pos_decifrada], text[i]))
        else:
            texto_decifrado.append(text[i])

    return ''.join(texto_decifrado)