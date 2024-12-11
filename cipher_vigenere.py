# João Davi
# Computer Systems Security
# UFRGS

# ====================== IMPORTS ======================
import os
import sys
from unicodedata import normalize

# ====================== FUNÇÕES AUXILIARES ======================

# Ajusta o caso da letra (maiúscula ou minúscula) para corresponder à referência.
def ajustar_caso(letra, referencia):
    return letra.upper() if referencia.isupper() else letra.lower()

# Função auxiliar para expandir a palavra-chave até o tamanho do texto
def expandir_palavra_chave(texto, palavra_chave):
    # Inicializa a variável (como string) que será usada para a palavra-chave expandida
    palavra_chave_expandida = []
    # Índice para acompanhar a posição atual na palavra-chave
    indice_palavra_chave = 0
    
    # Loop para repetir a palavra-chave, até que ela tenha o mesmo tamanho do texto
    for char in texto:
        if char.isalpha():
            # Adiciona a letra atual da palavra-chave na palavra-chave expandida
            palavra_chave_expandida.append(palavra_chave[indice_palavra_chave])
            # Incrementa o índice da palavra-chave e reinicia ao início dela, se necessário
            indice_palavra_chave = (indice_palavra_chave + 1) % len(palavra_chave)
        else:
            palavra_chave_expandida.append(char)
        
    return palavra_chave_expandida

# ====================== FUNÇÕES PRINCIPAIS ======================

# Função principal que codifica o texto claro usando a Cifra de Vigenère
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
        
    return texto_cifrado

def decoder_vigerene(texto_cifrado, palavra_chave):
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
        
    return texto_decifrado