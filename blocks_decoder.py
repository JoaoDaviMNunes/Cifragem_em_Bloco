from itertools import cycle
import cipher_vigenere
import cipher_alberti
import cipher_kamasutra
import sys
import os

# Retirando o padding
def unpad(texto):
    padding_tam = ord(texto[-1])
    return texto[:-padding_tam]

# Decriptografando o texto
def decifra_arquivo(entrada, saida, chave_ou_arquivo):
    # Abrindo o arquivo texto cifrado
    with open(entrada, 'r') as f:
        texto = f.read()

    # Obtendo a chave, seja diretamente ou por um arquivo
    if os.path.isfile(chave_ou_arquivo):
        with open(chave_ou_arquivo, 'r', encoding='utf-8') as f:
            palavra_chave = f.read().strip()
    else:
        palavra_chave = chave_ou_arquivo
    
    # Definindo o tamanho do bloco
    tam_bloco = 16
    blocos = [texto[i:i+tam_bloco] for i in range(0, len(texto), tam_bloco)]
    
    # Definindo as chaves e as cifras
    chaves = [palavra_chave, palavra_chave, palavra_chave]
    cifras = [cipher_vigenere.decoder_vigenere, cipher_alberti.decifragem_alberti, cipher_kamasutra.kama_decifra]
    
    # Realizando a descriptografia em blocos
    blocos_decifrados = []
    for i, bloco in enumerate(blocos):
        cifra = cifras[i % len(cifras)]
        chave = chaves[i % len(chaves)]
        blocos_decifrados.append(cifra(bloco, chave))
    
    texto_decifrado = unpad(''.join(blocos_decifrados))
    
    with open(saida, 'w') as f:
        f.write(texto_decifrado)

if __name__ == "__main__":
    # Verifica se foi passado tudo pela linha de comando ou Terminal
    if len(sys.argv) < 4:
        print("Uso errado pelo Terminal! Forma correta do comando:")
        print("python3 blocks_decoder.py <arquivo_entrada_texto_cifrado> <arquivo_saida_texto_decifrado> <chave_ou_arquivo>")
        sys.exit(1)

    # Recebendo os argumentos nas variáveis e mandando para a função de descriptografia
    entrada = sys.argv[1]
    saida = sys.argv[2]
    chave = sys.argv[3]
    decifra_arquivo(entrada, saida, chave)
    print("Decifragem em bloco realizada com sucesso!")
