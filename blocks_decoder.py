import sys
import os
import cipher_vigenere
import cipher_alberti
import cipher_kamasutra

# ====================== FUNÇÕES AUXILIARES ======================

# Função para remover padding composto de múltiplos de 'J's
def remover_padding(texto):
    """
    Remove padding composto apenas por 'J's no final do texto.
    """
    while texto and texto[-1] == 'J':
        texto.pop()  # Remove o último elemento se for 'J'
    return texto

# ====================== FUNÇÕES PRINCIPAIS ======================

if __name__ == "__main__":
    # Limpa a tela
    os.system("cls" if os.name == "nt" else "clear")

    # Verifica se foi passado tudo pela linha de comando ou Terminal
    if len(sys.argv) != 4:
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
        with open(arquivo_entrada, 'r', encoding='utf-8') as f:
            texto_cifrado = list(f.read().strip())  # Lê o texto e converte para lista de caracteres

        # Obtém a chave
        if os.path.isfile(chave_ou_arquivo):
            with open(chave_ou_arquivo, 'r', encoding='utf-8') as f:
                palavra_chave = list(f.read().strip())
        else:
            palavra_chave = list(chave_ou_arquivo.strip())

        # Definição do tamanho do bloco
        tamanho_bloco = 16  # 16 caracteres

        # Divide o texto em blocos de listas de caracteres
        blocos = [texto_cifrado[i:i + tamanho_bloco] for i in range(0, len(texto_cifrado), tamanho_bloco)]

        # Lista de funções de decodificação
        decoder_functions = [
            lambda bloco, chave: list(cipher_vigenere.decoder_vigenere(''.join(bloco), ''.join(chave))),
            lambda bloco, chave: list(cipher_alberti.decifra_texto(''.join(bloco), ''.join(chave))),
            lambda bloco, chave: list(cipher_kamasutra.descriptografar_arquivo(''.join(bloco), ''.join(chave))),
        ]

        # Lista para armazenar os blocos decifrados
        blocos_decifrados = []

        # Processa cada bloco
        for i, bloco in enumerate(blocos):
            decode_func = decoder_functions[i % len(decoder_functions)]
            bloco_decifrado = decode_func(bloco, palavra_chave)  # Retorna uma lista
            blocos_decifrados.append(bloco_decifrado)

        # Remove padding do último bloco
        if blocos_decifrados:
            blocos_decifrados[-1] = remover_padding(blocos_decifrados[-1])

        # Unindo os blocos decifrados e escrevendo no arquivo de saída
        with open(arquivo_saida, 'w', encoding='utf-8') as saida:
            texto_decifrado = ''.join([''.join(bloco) for bloco in blocos_decifrados])  # Concatena as listas de caracteres
            saida.write(texto_decifrado)

        print(f"Arquivo de saída \"{arquivo_saida}\" finalizado com sucesso!")

    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)
