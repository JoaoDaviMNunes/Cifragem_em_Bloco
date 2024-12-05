# João Davi
# Computer Systems Security
# UFRGS

# ====================== IMPORTS ======================
import os
import sys
from unicodedata import normalize

# ====================== FUNÇÕES AUXILIARES ======================

# Remove quebras de linha e converte o texto para maiúsculas.
# Preserva caracteres especiais e espaços.
def processar_texto(texto):
    return texto.replace("\n", "")

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
        
    return "".join(palavra_chave_expandida)

# ====================== FUNÇÕES PRINCIPAIS ======================

# Função para decodificar uma mensagem cifrada usando a Cifra de Vigenère
def decoder_vigerene(texto_cifrado, palavra_chave):
    # Inicializa uma variável (como string) para armazenar o texto decifrado
    texto_decifrado = []
    
    # Expande a palavra-chave para que tenha o mesmo comprimento que o texto cifrado
    palavra_chave_repetida = expandir_palavra_chave(texto_cifrado, palavra_chave)
    indice_palavra_chave = 0
    
    # Loop que percorre cada caractere do texto cifrado
    for char in texto_cifrado:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            # Converte a letra em seu índice ASCII, subtraindo o índice ASCII da palavra-chave para "reverter" a cifra e obter a palavra original
            posicao_texto = ord(char) - base
            posicao_palavra_chave = ord(palavra_chave_repetida[indice_palavra_chave].lower()) - ord("a")
            
            # Decifra o texto cifrado aplicando a subtração e usa o mód 26 (índice entre 0 e 25)
            indice_decifrado = (posicao_texto - posicao_palavra_chave + 26) % 26
            letra_decifrada = chr(indice_decifrado + base)
            
            # Adiciona a letra decifrada ao texto decifrado
            texto_decifrado.append(letra_decifrada)
        else:
            texto_decifrado.append(char)
        indice_palavra_chave += 1
        
    return "".join(texto_decifrado)

if __name__ ==  "__main__":
    # Limpa a tela para que seja realizada a cifragem e a decifragem da Cifra de Vigenère
    os.system("cls" if os.name == "nt" else "clear")

    # Verifica se foi passado tudo pela linha de comando ou Terminal
    if len(sys.argv) < 4:
        print("Uso errado pelo Terminal! Forma correta do comando:")
        print("python3 decoder-vigenere.py <arquivo_entrada_texto_cifrado> <arquivo_saida_texto_claro> <chave_ou_arquivo>")
        sys.exit(1)

    # Coloca nas variáveis as informações obtidas pelo Terminal
    arquivo_entrada = sys.argv[1]
    arquivo_saida = sys.argv[2]
    chave_ou_arquivo = sys.argv[3]

    # Leitura do texto cifrado a partir do arquivo de entrada
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        texto_cifrado = f.read()
    #texto_cifrado = processar_texto(texto_cifrado)

    # Obtenção da chave, seja diretamente ou a partir de um arquivo
    if os.path.isfile(chave_ou_arquivo):
        with open(chave_ou_arquivo, 'r', encoding='utf-8') as f:
            palavra_chave = f.read().strip()
    else:
        palavra_chave = chave_ou_arquivo
    #palavra_chave = processar_texto(palavra_chave)

    # Imprime na tela o texto cifrado
    print("Texto Cifrado:\t\t", texto_cifrado)

    # Decodifica o texto cifrado usando a função inversa da Cifra de Vigenère
    texto_decifrado = decoder_vigerene(texto_cifrado, palavra_chave)
    print("Texto Decifrado:\t\t", texto_decifrado)

    # Salva o texto decifrado no arquivo de saída
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write(texto_decifrado)
    print("Texto decifrado salvo no arquivo ", arquivo_saida)
