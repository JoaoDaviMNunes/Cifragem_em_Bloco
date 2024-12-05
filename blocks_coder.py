# João Davi
# Computer Systems Security
# UFRGS

# ====================== IMPORTS E CONSTANTES ======================

import sys
import os
import coder_vigenere
import decoder_vigenere
import coder_alberti
import decoder_alberti
import kamasutra
from unicodedata import normalize

# ====================== FUNÇÕES AUXILIARES ======================

# Função para retirar da string os caracteres especiais e os espaços, além de colocar todas letras em maiúsculo
def processar_texto(texto):
    texto = normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII")
    texto = "".join(texto.split()).upper()
    return texto

def adiciona_padding(texto, tamanho_bloco):
    pad_tam = tamanho_bloco - (len(texto) % tamanho_bloco)
    return texto + ('X' * pad_tam)

# ====================== FUNÇÕES PRINCIPAIS ======================

# Função para realizar uma rodada de Feistel
def feistel_round(bloco, chave, cifra_func):
    # Definindo as variáveis da rede de Feistel
    meio = len(bloco) // 2
    esq = bloco[:meio]
    dir = bloco[meio:]
    
    # Encriptação no lado direito
    cifra_saida = cifra_func(esq, chave)
    
    # Operação XOR entre os resultados
    novo_dir = ''.join(
        chr((ord(r) ^ ord(c)) % 256) for r, c in zip(dir, cifra_saida)
    )
    
    return dir + novo_dir

if __name__ == "__main__":
    # Limpa a tela para que seja realizada a cifragem e a decifragem da Cifra de Vigenère
    os.system("cls" if os.name == "nt" else "clear")

    # Verifica se foi passado tudo pela linha de comando ou Terminal
    if len(sys.argv) != 4:
        print("Uso errado pelo Terminal! Forma correta do comando:")
        print("python3 blocks_coder.py <arquivo_entrada_texto_claro> <arquivo_saida_texto_cifrado> <chave_ou_arquivo>")
        sys.exit(1)

    # Coloca nas variáveis as informações obtidas pelo Terminal
    arquivo_entrada = sys.argv[1]
    arquivo_saida = sys.argv[2]
    chave_ou_arquivo = sys.argv[3]

    if not os.path.isfile(arquivo_entrada):
        print(f"Erro: O arquivo {arquivo_entrada} não existe.")
        sys.exit(1)

    try:
        # Leitura do texto claro a partir do arquivo de entrada
        with open(arquivo_entrada, 'r') as f:
            texto = f.read().strip()
        texto = processar_texto(texto)
        print(texto)

        # Obtém a chave, seja diretamente ou por um arquivo
        if os.path.isfile(chave_ou_arquivo):
            with open(chave_ou_arquivo, 'r', encoding='utf-8') as f:
                palavra_chave = f.read().strip()
        else:
            palavra_chave = chave_ou_arquivo
        palavra_chave = processar_texto(palavra_chave)

        # Definição do tamanho do bloco e divisao do texto recebido em blocos
        tamanho_bloco = 16  # 16 bytes = 128 bits

        # Adiciona padding PKCS7, caso necessário
        texto_claro = adiciona_padding(texto, tamanho_bloco)

        # Realiza a separação por blocos
        for i in range(0, len(texto_claro), tamanho_bloco):
            blocos = [texto_claro[i:i + tamanho_bloco]]

        # Cria um bloco para a cifragem
        blocos_cifrados = []

        # definição e início da operação desejada
        for i, bloco in enumerate(blocos):
            texto_cifrado = feistel_round(bloco, palavra_chave, coder_vigenere.coder_vigenere)
            texto_cifrado = feistel_round(bloco, palavra_chave, coder_vigenere.coder_vigenere)
            texto_cifrado = feistel_round(bloco, palavra_chave, coder_vigenere.coder_vigenere)
            blocos_cifrados.append(texto_cifrado)

        # Unindo a lista de blocos e colocando o texto cifrado/decifrado no arquivo de saída
        with open(arquivo_saida, 'w') as saida:
            saida.write(''.join(blocos_cifrados))
            print(f"Arquivo de saída \"{arquivo_saida}\" finalizado com sucesso!")

    except Exception as e:
        print(f"Erro: {e}")
