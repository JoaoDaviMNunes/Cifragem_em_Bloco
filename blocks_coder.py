# João Davi
# Computer Systems Security
# UFRGS

# ====================== IMPORTS E CONSTANTES ======================

import sys
import os
from unicodedata import normalize
import cipher_vigenere
import cipher_alberti
import cipher_kamasutra

# ====================== FUNÇÕES AUXILIARES ======================

# Função para retirar da string os caracteres especiais e os espaços, além de colocar todas letras em maiúsculo
def processar_texto(texto):
    texto = normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII")
    texto = "".join(texto.split()).upper()
    return list(texto)  # Retorna como lista de caracteres

# Função para adicionar padding com 'J's
def adicionar_padding(texto, tamanho_bloco):
    pad_tam = tamanho_bloco - (len(texto) % tamanho_bloco)
    texto.extend(['J'] * pad_tam)  # Adiciona o padding como 'J'
    return texto

# ====================== FUNÇÕES PRINCIPAIS ======================

# Função para realizar uma rodada de Feistel
def feistel_round(bloco, chave, cifra_func):
    """
    Realiza uma rodada de Feistel:
    - Divide o bloco em partes esquerda e direita.
    - Aplica a função de cifra à metade esquerda usando a chave.
    - XOR entre o resultado e a metade direita.
    - Retorna as metades trocadas: novo_esq + novo_dir.
    """
    meio = len(bloco) // 2
    esq = bloco[:meio]
    dir = bloco[meio:]
    
    # Encriptação no lado esquerdo
    cifra_saida = cifra_func(''.join(esq), ''.join(chave))
    cifra_saida = list(cifra_saida)  # Garante que seja manipulável como lista

    # Operação XOR nos caracteres
    novo_dir = [
        chr((ord(r) ^ ord(c)) % 95 + 32) for r, c in zip(dir, cifra_saida)
    ]
    
    return dir + novo_dir  # Troca as metades

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
        with open(arquivo_entrada, 'r', encoding='utf-8') as f:
            texto = f.read().strip()
        texto = processar_texto(texto)

        # Obtém a chave, seja diretamente ou por um arquivo
        if os.path.isfile(chave_ou_arquivo):
            with open(chave_ou_arquivo, 'r', encoding='utf-8') as f:
                palavra_chave = f.read().strip()
        else:
            palavra_chave = chave_ou_arquivo
        palavra_chave = processar_texto(palavra_chave)

        # Definição do tamanho do bloco e divisão do texto recebido em blocos
        tamanho_bloco = 16  # 16 bytes = 128 bits
        texto_claro = adicionar_padding(texto, tamanho_bloco)

        # Realiza a separação por blocos
        blocos = [texto_claro[i:i + tamanho_bloco] for i in range(0, len(texto_claro), tamanho_bloco)]

        # Lista de funções de cifra a serem aplicadas em sequência
        cipher_functions = [cipher_vigenere.coder_vigenere, cipher_alberti.cifra_texto, cipher_kamasutra.criptografar_arquivo]

        # Cria um bloco para a cifragem
        blocos_cifrados = []

        # Processa cada bloco com a cifra correspondente
        for i, bloco in enumerate(blocos):
            # Escolhe a função de cifra de acordo com a ordem cíclica
            cifra_func = cipher_functions[i % len(cipher_functions)]

            # Aplica 2 rodadas de Feistel usando a cifra selecionada
            texto_cifrado = bloco
            for _ in range(2):  # 2 Feistel rounds
                texto_cifrado = feistel_round(texto_cifrado, palavra_chave, cifra_func)
            blocos_cifrados.append(''.join(texto_cifrado))

        # Unindo a lista de blocos e colocando o texto cifrado/decifrado no arquivo de saída
        with open(arquivo_saida, 'w', encoding='utf-8') as saida:
            saida.write(''.join(blocos_cifrados))
            print(f"Arquivo de saída \"{arquivo_saida}\" finalizado com sucesso!")

    except Exception as e:
        print(f"Erro: {e}")
