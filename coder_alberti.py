import sys


# FUNCAO PARA CIFRAR TEXTO
def cifra_texto(text, key):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'    # ALFABETO ALFANUMÉRICO PARA SUPORTE A CHAVES COM NÚMEROS
    with open(text, 'r') as arquivo_texto:          # ABRE O ARQUIVO
        conteudo = arquivo_texto.read().upper()     # COPIA O CONTEUDO DO ARQUIVO DE TEXTO PARA A VARIAVEL CONTEUDO E COLOCA TUDO PARA MAIUSCULO
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
    


    return ''.join(texto_cifrado)


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

