# João Davi
# Computer Systems Security
# UFRGS

# ====================== IMPORTS E CONSTANTES ======================

import sys
import os
import coder_vigenere
import decoder_vigenere
from unicodedata import normalize

# ====================== FUNÇÕES AUXILIARES ======================

# Função para retirar da string os caracteres especiais e os espaços, além de colocar todas letras em maiúsculo
def processar_texto(texto):
    texto = normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII")
    texto = "".join(texto.split()).upper()
    return texto

# Função para dividir o texto de entrada em blocos, verificando a necessidade de padding (PKCS#7), e retorna uma lista de blocos
def divisao_em_blocos(arquivo_entrada, tamanho_bloco):
    # Abre o arquivo no modo de leitura em binário
    with open(arquivo_entrada, 'rb') as arquivo:
        texto = arquivo.read()


# ====================== FUNÇÕES PRINCIPAIS ======================

if __name__ ==  "__main__":
    # Limpa a tela para que seja realizada a cifragem e a decifragem da Cifra de Vigenère
    os.system("cls" if os.name == "nt" else "clear")

    # Verifica se foi passado tudo pela linha de comando ou Terminal
    if len(sys.argv) < 5:
        print("Uso errado pelo Terminal! Forma correta do comando:")
        print("python3 main.py <arquivo_entrada_texto_claro> <arquivo_saida_texto_cifrado> <chave_ou_arquivo> <comando>")
        print("Comando = \"cifragem\" ou \"decifragem\".")
        sys.exit(1)

    # Coloca nas variáveis as informações obtidas pelo Terminal
    arquivo_entrada = sys.argv[1]
    arquivo_saida = sys.argv[2]
    chave_ou_arquivo = sys.argv[3]
    comando_codificacao = sys.argv[4]

    # Leitura do texto claro a partir do arquivo de entrada
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        texto_claro = f.read()
    texto_claro = processar_texto(texto_claro)

    # Obtém a chave, seja diretamente ou por um arquivo
    if os.path.isfile(chave_ou_arquivo):
        with open(chave_ou_arquivo, 'r', encoding='utf-8') as f:
            palavra_chave = f.read().strip()
    else:
        palavra_chave = chave_ou_arquivo
    palavra_chave = processar_texto(palavra_chave)

    # Definição do tamanho do bloco e divisao do texto recebido em blocos
    tamanho_bloco = 16          # 16 bytes = 128 bits
    blocos = divisao_em_blocos(texto_claro)

    # definição e início da operação desejada
    if comando_codificacao == "cifragem":
        for i in range(len(blocos)):
            if i%3 == 0:
                blocos[i] = coder_vigenere.coder_vigerene(blocos[i], palavra_chave)
            elif i%3 == 1:
                blocos[i] = coder_vigenere.coder_vigerene(blocos[i], palavra_chave)
            if i%3 == 2:
                blocos[i] = coder_vigenere.coder_vigerene(blocos[i], palavra_chave)
    elif comando_codificacao == "decifragem":
        for i in range(len(blocos)):
            if i%3 == 0:
                blocos[i] = decoder_vigenere.decoder_vigerene(blocos[i], palavra_chave)
            elif i%3 == 1:
                blocos[i] = coder_vigenere.coder_vigerene(blocos[i], palavra_chave)
            if i%3 == 2:
                blocos[i] = coder_vigenere.coder_vigerene(blocos[i], palavra_chave)

    else:
        print("Comando errado! Comando = \"cifragem\" ou \"decifragem\".")
        print("Forma correta e completa do comando pelo Terminal:")
        print("python3 main.py <arquivo_entrada_texto_claro> <arquivo_saida_texto_cifrado> <chave_ou_arquivo> <comando>")
        sys.exit(1)

    # Unindo a lista de blocos e colocando o texto cifrado/decifrado no arquivo de saída
    with open(arquivo_saida, 'w', encoding='utf-8') as saida:
        texto = " ".join(map(str, blocos))
        saida.write(texto)
        print("Arquivo de saída criado com sucesso!")




