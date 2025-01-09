from itertools import cycle
import sys
import os

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

def unpad(text):
    padding_len = ord(text[-1])
    return text[:-padding_len]

# ====================== FUNÇÕES PRINCIPAIS ======================

# Função para cifrar texto usando o método baseado na cifra de Alberti
def cifragem_alberti(conteudo, key):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'  # Alfabeto alfanumérico
    key = key.upper()  # Coloca a chave em maiúsculo
    texto_cifrado = []

    # Expande a chave para ter o mesmo tamanho do conteúdo
    chave_expandida = expandir_palavra_chave(conteudo, key)

    for i in range(len(conteudo)):
        if conteudo[i].upper() in alfabeto:
            pos_texto = alfabeto.find(conteudo[i].upper())
            pos_chave = alfabeto.find(chave_expandida[i].upper())
            pos_cifrada = (pos_texto + pos_chave) % len(alfabeto)
            texto_cifrado.append(ajustar_caso(alfabeto[pos_cifrada], conteudo[i]))
        else:
            # Se o caractere não estiver no alfabeto, adicioná-lo sem cifragem
            texto_cifrado.append(conteudo[i])

    return ''.join(texto_cifrado)

# Função para decifrar texto usando o método baseado na cifra de Alberti
def decifragem_alberti(text, key):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    key = key.upper()
    texto_decifrado = []

    chave_expandida = expandir_palavra_chave(text, key)

    for i in range(len(text)):
        if text[i].upper() in alfabeto:
            pos_texto = alfabeto.find(text[i].upper())
            pos_chave = alfabeto.find(chave_expandida[i].upper())
            pos_decifrada = (pos_texto - pos_chave) % len(alfabeto)
            texto_decifrado.append(ajustar_caso(alfabeto[pos_decifrada], text[i]))
        else:
            texto_decifrado.append(text[i])

    return ''.join(texto_decifrado)

def criar_tabela_substituicao():
    alfabeto = 'abcdefghijklmnopqrstuvwxyz'
    primeira_metade = alfabeto[:13]
    segunda_metade = alfabeto[13:]

    tabela_criptografia = {}
    tabela_descriptografia = {}

    for i in range(len(primeira_metade)):
        tabela_criptografia[primeira_metade[i]] = segunda_metade[i]
        tabela_criptografia[segunda_metade[i]] = primeira_metade[i]
        tabela_descriptografia[segunda_metade[i]] = primeira_metade[i]
        tabela_descriptografia[primeira_metade[i]] = segunda_metade[i]
    
    return tabela_criptografia, tabela_descriptografia

def kama_cifra(text, key):
    tabela_criptografia, _ = criar_tabela_substituicao()
    texto_criptografado = []

    for char in text:
        if char in tabela_criptografia:
            texto_criptografado.append(tabela_criptografia[char])
        else:
            texto_criptografado.append(char)
    
    return ''.join(texto_criptografado)

def kama_decifra(text, key):
    _, tabela_descriptografia = criar_tabela_substituicao()
    texto_descriptografado = []

    for char in text:
        if char in tabela_descriptografia:
            texto_descriptografado.append(tabela_descriptografia[char])
        else:
            texto_descriptografado.append(char)
    
    return ''.join(texto_descriptografado)

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

# ==============================================

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
    cifras = [decoder_vigenere, decifragem_alberti, kama_decifra]
    
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
