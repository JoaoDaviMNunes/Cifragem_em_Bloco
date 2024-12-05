# João Davi
# Computer Systems Security
# UFRGS

# ====================== IMPORTS ======================
import os
import sys
from unicodedata import normalize

# ====================== FUNÇÕES AUXILIARES ======================

# Ajusta o caso da letra (maiúscula ou minúscula) para corresponder à referência.
def ajustar_caso(letra, referencia):
    return letra.upper() if referencia.isupper() else letra.lower()

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

# Função principal que codifica o texto claro usando a Cifra de Vigenère
def coder_vigerene(texto_claro, palavra_chave):
    # Inicializa uma variável (como string) para armazenar o texto cifrado
    texto_cifrado = []
    
    # Expande a palavra-chave até que ela tenha o mesmo comprimento que o texto
    palavra_chave_repetida = expandir_palavra_chave(texto_claro, palavra_chave)
    indice_palavra_chave = 0
    
    # Loop que percorre cada caractere do texto claro
    for char in texto_claro:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            # ord(): função do Python que pega o valor ASCII da letra e subtrai o valor ASCII de "A" para obter um índice entre 0 e 25 (26 letras do alfabeto regular)
            posicao_texto = ord(char) - base
            posicao_palavra_chave = ord(palavra_chave_repetida[indice_palavra_chave].lower()) - ord("a")
            
            # Cifra o texto aplicando o índice da palavra-chave, e usa o mód 26 (índice entre 0 e 25))
            char_cifrado = (posicao_texto + posicao_palavra_chave) % 26
            # chr(): função do Python que converte o índice numérico de volta para uma letra maiúscula
            letra_cifrada = chr(char_cifrado + base)
            
            # Adiciona a letra cifrada ao texto cifrado
            texto_cifrado.append(letra_cifrada)
        else:
            texto_cifrado.append(char)
        indice_palavra_chave += 1
        
    return "".join(texto_cifrado)

if __name__ ==  "__main__":
    # Limpa a tela para que seja realizada a cifragem e a decifragem da Cifra de Vigenère
    os.system("cls" if os.name == "nt" else "clear")

    # Verifica se foi passado tudo pela linha de comando ou Terminal
    if len(sys.argv) < 4:
        print("Uso errado pelo Terminal! Forma correta do comando:")
        print("python3 coder-vigenere.py <arquivo_entrada_texto_claro> <arquivo_saida_texto_cifrado> <chave_ou_arquivo>")
        sys.exit(1)

    # Coloca nas variáveis as informações obtidas pelo Terminal
    arquivo_entrada = sys.argv[1]
    arquivo_saida = sys.argv[2]
    chave_ou_arquivo = sys.argv[3]

    # Leitura do texto claro a partir do arquivo de entrada
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        texto_claro = f.read()

    # Obtém a chave, seja diretamente ou por um arquivo
    if os.path.isfile(chave_ou_arquivo):
        with open(chave_ou_arquivo, 'r', encoding='utf-8') as f:
            palavra_chave = f.read().strip()
    else:
        palavra_chave = chave_ou_arquivo

    # Codifica o texto usando a Cifra de Vigenère
    texto_cifrado = coder_vigerene(texto_claro, palavra_chave)

    # Imprime na tela o texto claro
    print("Texto Claro:\t\t", texto_claro)

    # Codifica o texto claro usando a função de Cifra de Vigenère
    texto_cifrado = coder_vigerene(texto_claro, palavra_chave)
    print("Texto Cifrado:\t\t", texto_cifrado)

    # Salva o texto cifrado no arquivo de saída
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write(texto_cifrado)
    print("Texto cifrado salvo no arquivo ", arquivo_saida)