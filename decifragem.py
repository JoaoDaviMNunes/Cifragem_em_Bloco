import sys
import os

# ====================== FUNÇÕES AUXILIARES ======================

def ajustar_caso(letra, referencia):
    return letra.upper() if referencia.isupper() else letra.lower()

def unpad(data):
    padding_length = data[-1]
    return data[:-padding_length]

# ====================== DESCRIPTOGRAFIA ======================

# Função para decifrar texto usando o método baseado na cifra de Alberti
def decifragem_alberti(texto, chave):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    chave = chave.upper()
    texto_decifrado = []
    chave_expandida = (chave * (len(texto) // len(chave) + 1))[:len(texto)]

    for i in range(len(texto)):
        if texto[i].upper() in alfabeto:
            pos_texto = alfabeto.find(texto[i].upper())
            pos_chave = alfabeto.find(chave_expandida[i])
            pos_decifrada = (pos_texto - pos_chave) % len(alfabeto)
            texto_decifrado.append(ajustar_caso(alfabeto[pos_decifrada], texto[i]))
        else:
            texto_decifrado.append(texto[i])

    return ''.join(texto_decifrado)

# Função para decifrar usando a cifra de Kamasutra
def kama_decifra(texto):
    alfabeto = 'abcdefghijklmnopqrstuvwxyz'
    primeira_metade = alfabeto[:13]
    segunda_metade = alfabeto[13:]
    tabela_descriptografia = {segunda_metade[i]: primeira_metade[i] for i in range(13)}
    tabela_descriptografia.update({primeira_metade[i]: segunda_metade[i] for i in range(13)})

    texto_decifrado = []

    for char in texto:
        texto_decifrado.append(tabela_descriptografia.get(char, char))

    return ''.join(texto_decifrado)

# Função para decifrar usando a cifra de Vigenere
def decoder_vigenere(texto, chave):
    texto_decifrado = []
    chave_expandida = (chave * (len(texto) // len(chave) + 1))[:len(texto)]

    for i, char in enumerate(texto):
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            pos_texto = ord(char) - base
            pos_chave = ord(chave_expandida[i].lower()) - ord('a')
            char_decifrado = (pos_texto - pos_chave + 26) % 26
            texto_decifrado.append(chr(char_decifrado + base))
        else:
            texto_decifrado.append(char)

    return ''.join(texto_decifrado)

# Função para aplicar XOR
def decifragem_xor(bloco, chave):
    return bytes([b ^ chave[i % len(chave)] for i, b in enumerate(bloco)])

# Rodadas de Feistel (decifragem)
def rodadas_feistel_decifra(bloco, chave):
    metade = len(bloco) // 2
    direita = bloco[:metade]
    esquerda = bloco[metade:]

    for _ in range(2):
        nova_esquerda = bytes([e ^ k for e, k in zip(direita, esquerda)])
        direita, esquerda = nova_esquerda, direita

    return direita + esquerda

# ====================== PROCESSAMENTO ======================

def decifra_arquivo(entrada, saida, chave_ou_arquivo):
    with open(entrada, 'rb') as f:
        texto_cifrado = f.read()

    if os.path.isfile(chave_ou_arquivo):
        with open(chave_ou_arquivo, 'r', encoding='utf-8') as f:
            chave = f.read().strip()
    else:
        chave = chave_ou_arquivo

    bloco_tam = 16
    blocos = [texto_cifrado[i:i + bloco_tam] for i in range(0, len(texto_cifrado), bloco_tam)]
    blocos_decifrados = []

    for bloco in blocos:
        bloco = rodadas_feistel_decifra(bloco, chave.encode())
        bloco = kama_decifra(bloco.decode(errors='ignore')).encode()
        bloco = decifragem_xor(bloco, chave.encode())
        bloco = decifragem_alberti(bloco.decode(errors='ignore'), chave).encode()
        bloco = decifragem_xor(bloco, chave.encode())
        bloco = decoder_vigenere(bloco.decode(errors='ignore'), chave).encode()
        blocos_decifrados.append(bloco)

    texto_decifrado = unpad(b''.join(blocos_decifrados))

    with open(saida, 'wb') as f:
        f.write(texto_decifrado)

# ===================== EXECUÇÃO =====================
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso incorreto! Formato:")
        print("python3 decifragem.py <entrada> <saída> <chave ou arquivo de chave>")
        sys.exit(1)

    entrada = sys.argv[1]
    saida = sys.argv[2]
    chave = sys.argv[3]
    decifra_arquivo(entrada, saida, chave)
    print("Decifragem realizada com sucesso!")
