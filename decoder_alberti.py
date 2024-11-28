import sys

# FUNCAO PARA DECIFRAR TEXTO
def decifra_texto(text, key):
    try:
        alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        
        # Verifica se o conteúdo é bytes e converte para string
        if isinstance(text, bytes):
            conteudo_cifrado = text.decode('utf-8')
        else:
            conteudo_cifrado = text

        key = key.upper()                                       # COLOCA A CHAVE TUDO EM MAIUSCULO
        texto_decifrado = []
        
        chave_expandida = (key * (len(conteudo_cifrado) // len(key) + 1))[:len(conteudo_cifrado)]

        for i in range(len(conteudo_cifrado)):
            if conteudo_cifrado[i] in alfabeto:
                pos_cifrada = alfabeto.index(conteudo_cifrado[i])
                pos_chave = alfabeto.index(chave_expandida[i])
                pos_decifrada = (pos_chave - pos_cifrada) % len(alfabeto)
                texto_decifrado.append(alfabeto[pos_decifrada])
            else:
                # Adiciona caracteres não alfabéticos sem decifragem
                texto_decifrado.append(conteudo_cifrado[i])
    except FileNotFoundError:
        print("TEXTO OU CHAVE ERRADA")
        sys.exit(1)
    except ValueError:
        print("TEXTO OU CHAVE ERRADA")
        sys.exit(1)

    return ''.join(texto_decifrado)


#############################################
# FUNÇÃO PARA MOSTRAR MANUAL
def manual():
    print("Formas de uso: python decifra_Texto.py <Chave usada para cifrar> <Arquivo com texto a Decifrar>")
    sys.exit(1)


#############################################

# FUNÇÃO MAIN
if __name__ == "__main__":
    if len(sys.argv) < 3:
        manual()
    
    chave = sys.argv[1]
    arquivo_texto_cifrado = sys.argv[2]

    resposta_texto_decifrado = decifra_texto(arquivo_texto_cifrado, chave)
    print("O Texto decifrado eh: " + resposta_texto_decifrado)


#    with open("TEXTO_CIFRADO.txt", 'w') as arquivo_saida:
#        arquivo_saida.write(resposta_texto_decifrado)

#    print("Texto decifrado salvo em 'TEXTO_DECIFRADO.txt'")

