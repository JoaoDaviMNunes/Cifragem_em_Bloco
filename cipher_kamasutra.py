# Código de Pedro Lucas Moraes de Souza Rosa
# Adaptação por João Davi Martins Nunes
# Parte da Cifragem em Bloco

def criar_tabela_substituicao():
    # Cria um dicionário com os pares de substituição (cada letra será substituida pela sua correspondente)
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

# Ajuste no uso de tabela de substituição sem chave extra
def criptografar_arquivo(texto, chave):
    tabela_criptografia, _ = criar_tabela_substituicao()
    texto_criptografado = []

    for char in texto:
        if char in tabela_criptografia:
            texto_criptografado.append(tabela_criptografia[char])
        else:
            texto_criptografado.append(char)
    
    return texto_criptografado


def descriptografar_arquivo(texto, chave):
    # Obtém as tabelas de substituição
    _, tabela_descriptografia = criar_tabela_substituicao()

    try:
        # Cria uma lista para armazenar os caracteres descriptografados.
        texto_descriptografado = []
        
        for char in texto:
            # Se o caractere estiver na tabela de substituição, faz a troca. 
            if char in tabela_descriptografia:
                texto_descriptografado.append(tabela_descriptografia[char])
            else:
                # Se não estiver na tabela (números, espaços, etc), mantém o caractere original.
                texto_descriptografado.append(char)
        
        return texto_descriptografado

    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")
