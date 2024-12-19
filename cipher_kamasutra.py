# Código de Pedro Lucas Moraes de Souza Rosa
# Adaptação por João Davi Martins Nunes
# Parte da Cifragem em Bloco

def criar_tabela_substituicao():
    alfabeto = 'abcdefghijklmnopqrstuvwxyz'
    primeira_metade = alfabeto[:13]
    segunda_metade = alfabeto[13:]

    tabela_criptografia = {}
    tabela_descriptografia = {}

    for i in range(len(primeira_metade)):
        tabela_criptografia[primeira_metade[i]] = segunda_metade[i]
        tabela_criptografia[segunda_metade[i]] = primeira_metade[i]
        tabela_descriptografia[segunda_metade[i]] = primeira_metade[i]
        tabela_descriptografia[primeira_metade[i]] = segunda_metade[i]
    
    return tabela_criptografia, tabela_descriptografia

def kama_cifra(text, key):
    tabela_criptografia, _ = criar_tabela_substituicao()
    texto_criptografado = []

    for char in text:
        if char in tabela_criptografia:
            texto_criptografado.append(tabela_criptografia[char])
        else:
            texto_criptografado.append(char)
    
    return ''.join(texto_criptografado)


def kama_decifra(text, key):
    _, tabela_descriptografia = criar_tabela_substituicao()
    texto_descriptografado = []

    for char in text:
        if char in tabela_descriptografia:
            texto_descriptografado.append(tabela_descriptografia[char])
        else:
            texto_descriptografado.append(char)
    
    return ''.join(texto_descriptografado)