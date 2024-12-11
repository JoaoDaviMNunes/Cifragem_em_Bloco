# Código de Diego Ferreira Duarte
# Adaptação por João Davi Martins Nunes
# Parte da Cifragem em Bloco

import sys
import os
from unicodedata import normalize

# ====================== FUNÇÕES PRINCIPAIS ======================

# Função para cifrar texto usando o método baseado na cifra de Alberti
def cifra_texto(conteudo, key):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'  # Alfabeto alfanumérico
    key = key.upper()  # Coloca a chave em maiúsculo
    texto_cifrado = []

    # Expande a chave para ter o mesmo tamanho do conteúdo
    chave_expandida = (key * (len(conteudo) // len(key) + 1))[:len(conteudo)]

    for i in range(len(conteudo)):
        if conteudo[i] in alfabeto:
            pos_texto = alfabeto.find(conteudo[i])
            pos_chave = alfabeto.find(chave_expandida[i])
            pos_cifrada = (pos_chave - pos_texto) % len(alfabeto)
            texto_cifrado.append(alfabeto[pos_cifrada])
        else:
            # Se o caractere não estiver no alfabeto, adicioná-lo sem cifragem
            texto_cifrado.append(conteudo[i])

    return texto_cifrado

# FUNCAO PARA DECIFRAR TEXTO
def decifra_texto(texto, chave):
    # Exemplo de decodificação com cifra de Alberti
    texto_decifrado = []  # Lista de caracteres decifrados

    for i in range(len(texto)):
        # Exemplo de decodificação
        texto_decifrado.append(chr((ord(texto[i]) - ord(chave[i % len(chave)])) % 256))

    return texto_decifrado


