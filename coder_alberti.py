import sys

# FUNCAO PARA CIFRAR TEXTO
def cifra_texto(text, key):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # Verifica se o conteúdo é bytes e converte para string
    if isinstance(text, bytes):
        conteudo = text.decode('utf-8')
    else:
        conteudo = text

    key = key.upper()                               # COLOCA A CHAVE TUDO EM MAIUSCULO
    texto_cifrado = []
    
    chave_expandida = (key * (len(conteudo) // len(key) + 1))[:len(conteudo)]

    for i in range(len(conteudo)):
        if conteudo[i] in alfabeto:
            pos_texto = alfabeto.find(conteudo[i])
            pos_chave = alfabeto.find(chave_expandida[i])
            pos_cifrada = (pos_chave - pos_texto) % len(alfabeto)
            texto_cifrado.append(alfabeto[pos_cifrada])
        else:
            # Se o caractere não estiver no alfabeto, adicioná-lo sem cifragem
            texto_cifrado.append(conteudo[i])


    return "".join(texto_cifrado)


#############################################
# FUNÇÃO PARA MOSTRAR MANUAL
def manual():
    print("Formas de uso: python Cifra_Texto.py <Chave> <Arquivo com texto a Cifrar>")
    sys.exit(1)


#############################################

# FUNÇÃO MAIN
if __name__ == "__main__":
    if len(sys.argv) < 3:
        manual()
    
    chave = sys.argv[1]
    arquivo_texto = sys.argv[2]

    resposta_texto_cifrado = cifra_texto(arquivo_texto, chave)
    print("O Texto cifrado eh: " + resposta_texto_cifrado)

    with open("TEXTO_CIFRADO.txt", 'w') as arquivo_saida:
        arquivo_saida.write(resposta_texto_cifrado)

    print("Texto cifrado salvo em 'TEXTO_CIFRADO.txt'")

