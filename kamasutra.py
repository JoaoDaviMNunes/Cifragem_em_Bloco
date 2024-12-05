def criar_tabela_substituicao():
    # Cria um dicionário com os pares de substituição (cada letra será substituida pela sua correspondente)
    # Ex: 'a' será substituida por 'n', 'b' por 'o', e assim por diante. 
    alfabeto = 'abcdefghijklmnopqrstuvwxyz'
    primeira_metade = alfabeto[:13]
    segunda_metade = alfabeto[13:]

    # Cria dois dicionários: um para criptografar e outro para decriptar. 

    tabela_criptografia = {}
    tabela_descriptografia = {}

    # Preenche as tabelas com os pares de substituição.

    for i in range(len(primeira_metade)):
        tabela_criptografia[primeira_metade[i]] = segunda_metade[i]
        tabela_criptografia[segunda_metade[i]] = primeira_metade[i]
        tabela_descriptografia[segunda_metade[i]] = primeira_metade[i]
        tabela_descriptografia[primeira_metade[i]] = segunda_metade[i]
    
    return tabela_criptografia, tabela_descriptografia

def criptografar_arquivo(nome_arquivo_entrada, nome_arquivo_saida):
    # Obtém as tabelas de substituição

    tabela_criptografia, _ = criar_tabela_substituicao()

    try:
        # Abre o arquivo de entrada para leitura.
        with open(nome_arquivo_entrada, 'r', encoding='utf-8') as arquivo_entrada:
            texto = arquivo_entrada.read().lower()

        # Realiza a criptografia caractere por caractere.
        texto_criptografado = ''
        
        for char in texto:
            # Se o caractere estiver na tabela de substituição, faz a troca. 
            if char in tabela_criptografia:
                texto_criptografado += tabela_criptografia[char]
            else:
                # Se não estiver na tabela (números, espaços, etc), mantém o caractere original
                texto_criptografado += char

        # Salva o texto criprografado em um novo arquivo
        with open(nome_arquivo_saida, 'w', encoding='utf-8') as arquivo_saida:
            arquivo_saida.write(texto_criptografado)

        print(f"Arquivo criptografado com sucesso! Salvo como: {nome_arquivo_saida}")
    
    except FileExistsError:
        print(f"Erro: o arquivo {nome_arquivo_entrada} não foi encontrado.")
    except Exception:
        print(f"Ocorreu um erro: {str(e)}")

def descriptografar_arquivo(nome_arquivo_entrada, nome_arquivo_saida):
    # Obtém as tabelas de substituição

    _, tabela_descriptografia = criar_tabela_substituicao()

    try:
        # Abre o arquivo criptografado para leitura. 

        with open(nome_arquivo_entrada, 'r', encoding='utf-8') as arquivo_entrada:
            texto = arquivo_entrada.read().lower()

        # Realiza a descriptografia caractere por caractere.
        texto_descriptografado = ''
        for char in texto:
            # Se o caractere estivber na tabela de substituição, faz a troca. 
            if char in tabela_descriptografia:
                texto_descriptografado += tabela_descriptografia[char]
            else:
                # Se não estiver na tabela (números, espaços, etc), mantém o caractere original.
                texto_descriptografado += char
        
        # Salva o texto descriptografado em um novo arquivo. 
        with open(nome_arquivo_saida, 'w', encoding='utf-8') as arquivo_saida:
            arquivo_saida.write(texto_descriptografado)
            print(f"Arquivo descriptografado com sucesso! Salvar como: {nome_arquivo_saida}")
    
    except FileNotFoundError:
        print(f" Erro: o arquivo {nome_arquivo_saida} não foi encontrado.")

    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")

# Usando o programa. 
if __name__ == "__main__":
    
    # Menu simples para o usuário escolher a operação. 
    print("Este programa utiliza a Cifra KamaSutra!!")
    print("1 - Criptografar um arquivo")
    print("2 - Descriptografar um arquivo")
    opcao = input("Escolha uma opção (1 ou 2): ")

    # Solicita os nomes dos arquivos

    arquivo_entrada = input(" Digite o nome de arquivo de entrada: ")
    arquivo_saida = input(" Digite o nome do arquivo de saída: ")

    # Executa a operação escolhida. 

    if opcao == "1":
        criptografar_arquivo(arquivo_entrada, arquivo_saida)
    elif opcao == "2":
        descriptografar_arquivo(arquivo_entrada,arquivo_saida)
    else:
        print("Opção invalida")