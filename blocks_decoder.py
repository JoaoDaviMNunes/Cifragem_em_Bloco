# João Davi
# Computer Systems Security
# UFRGS

# ====================== IMPORTS E CONSTANTES ======================

import sys
import os
import coder_vigenere
import coder_alberti
import coder_ADFGVX
import decoder_vigenere
import decoder_alberti
import decoder_ADFGVX
from unicodedata import normalize

# ====================== FUNÇÕES AUXILIARES ======================

# Função para retirar os caracteres especiais e os espaços, além de colocar todas letras em maiúsculo
def processar_texto(texto):
    texto = normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII")
    texto = "".join(texto.split()).upper()
    return texto

# Função para remover padding PKCS#7 do último bloco
def remove_padding(texto):
    tamanho_pad = texto[-1]
    if all(p == tamanho_pad for p in texto[-tamanho_pad:]):
        return texto[:-tamanho_pad]
    raise ValueError("Padding inválido!")

# ====================== FUNÇÕES PRINCIPAIS ======================

if __name__ == "__main__":
    # Limpa a tela
    os.system("cls" if os.name == "nt" else "clear")

    # Verifica se foi passado tudo pela linha de comando ou Terminal
    if len(sys.argv) < 4:
        print("Uso errado pelo Terminal! Forma correta do comando:")
        print("python3 blocks_decoder.py <arquivo_entrada_texto_cifrado> <arquivo_saida_texto_decifrado> <chave_ou_arquivo>")
        sys.exit(1)

    # Coloca nas variáveis as informações obtidas pelo Terminal
    arquivo_entrada = sys.argv[1]
    arquivo_saida = sys.argv[2]
    chave_ou_arquivo = sys.argv[3]

    if not os.path.isfile(arquivo_entrada):
        print(f"Erro: O arquivo {arquivo_entrada} não existe.")
        sys.exit(1)

    try:
        # Leitura do texto cifrado a partir do arquivo de entrada
        with open(arquivo_entrada, 'rb') as f:
            texto_cifrado = f.read()

        # Obtém a chave, seja diretamente ou por um arquivo
        if os.path.isfile(chave_ou_arquivo):
            with open(chave_ou_arquivo, 'r', encoding='utf-8') as f:
                palavra_chave = f.read().strip()
        else:
            palavra_chave = chave_ou_arquivo
        palavra_chave = processar_texto(palavra_chave)

        # Definição do tamanho do bloco
        tamanho_bloco = 16  # 16 bytes = 128 bits

        # Divide o texto em blocos
        blocos = [texto_cifrado[i:i + tamanho_bloco] for i in range(0, len(texto_cifrado), tamanho_bloco)]

        # Lista para armazenar os blocos decifrados
        blocos_decifrados = []

        # Processa cada bloco com o decodificador correspondente
        for i, bloco in enumerate(blocos):
            bloco_str = bloco.decode('latin1')  # Decodifica o bloco de bytes para string
            if i % 3 == 0:
                bloco_decifrado = decoder_vigenere.decoder_vigenere(bloco_str, palavra_chave)
            elif i % 3 == 1:
                bloco_decifrado = decoder_vigenere.decoder_vigenere(bloco_str, palavra_chave)
            elif i % 3 == 2:
                bloco_decifrado = decoder_vigenere.decoder_vigenere(bloco_str, palavra_chave)
            blocos_decifrados.append(bloco_decifrado.encode('latin1'))  # Recodifica para bytes

        # Remove padding do último bloco
        if blocos_decifrados:
            blocos_decifrados[-1] = remove_padding(blocos_decifrados[-1])

        # Unindo a lista de blocos decifrados e escrevendo no arquivo de saída
        with open(arquivo_saida, 'wb') as saida:
            saida.write(b''.join(blocos_decifrados))

        print("Arquivo de saída criado com sucesso!")

    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)
