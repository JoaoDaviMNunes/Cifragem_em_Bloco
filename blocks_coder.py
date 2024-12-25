# João Davi
# Computer Systems Security
# UFRGS

# ====================== IMPORTS E CONSTANTES ======================

import sys
import os
from itertools import cycle
import cipher_vigenere
import cipher_alberti
import cipher_kamasutra

def pad(texto, bloco_tam):
    padding_tam = bloco_tam - (len(texto) % bloco_tam)
    return texto + chr(padding_tam) * padding_tam

def cifrar_arquivo(entrada, saida, chave_ou_arquivo):
    # Abrindo o arquivo texto claro
    with open(entrada, 'r') as f:
        texto = f.read()

    # Obtendo a chave, seja diretamente ou por um arquivo
    if os.path.isfile(chave_ou_arquivo):
        with open(chave_ou_arquivo, 'r', encoding='utf-8') as f:
            palavra_chave = f.read().strip()
    else:
        palavra_chave = chave_ou_arquivo
    
    # Definindo o tamanho do bloco
    bloco_tam = 16
    texto = pad(texto, bloco_tam)
    blocos = [texto[i:i+bloco_tam] for i in range(0, len(texto), bloco_tam)]
    
    # Definindo as palavras-chaves e as cifras a serem utilizadas
    chaves = [palavra_chave, palavra_chave, palavra_chave]
    cifras = [cipher_vigenere.coder_vigenere, cipher_alberti.cifragem_alberti, cipher_kamasutra.kama_cifra]
    
    # Realizando a cifragem em bloco
    blocos_criptografados = []
    for i, bloco in enumerate(blocos):
        cifra = cifras[i % len(cifras)]
        chave = chaves[i % len(chaves)]
        blocos_criptografados.append(cifra(bloco, chave))
    
    # Escrevendo no arquivo de saída
    with open(saida, 'w') as f:
        f.write(''.join(blocos_criptografados))

if __name__ == "__main__":
    # Verificando se foi passado tudo pela linha de comando ou Terminal
    if len(sys.argv) < 4:
        print("Uso errado pelo Terminal! Forma correta do comando:")
        print("python3 coder-vigenere.py <arquivo_entrada_texto_claro> <arquivo_saida_texto_cifrado> <chave_ou_arquivo>")
        sys.exit(1)

    # Recebendo os argumentos nas variáveis e mandando para a função de criptografia
    entrada = sys.argv[1]
    saida = sys.argv[2]
    chave = sys.argv[3]
    cifrar_arquivo(entrada, saida, chave)
    print("Cifragem em bloco realizada com sucesso!")
