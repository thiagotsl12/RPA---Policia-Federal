import os

# Define o caminho da pasta principal
pasta_principal = '/caminho/para/pasta_principal'

# Itera sobre todos os itens na pasta principal
for item in os.listdir(pasta_principal):
    # Cria o caminho completo do item
    caminho_completo = os.path.join(pasta_principal, item)
    
    # Verifica se o item é uma pasta
    if os.path.isdir(caminho_completo):
        print(f"Encontrada pasta: {caminho_completo}")
        
        # Acessa a pasta e realiza ações
        for arquivo in os.listdir(caminho_completo):
            caminho_arquivo = os.path.join(caminho_completo, arquivo)
            if os.path.isfile(caminho_arquivo):
                print(f"Processando arquivo: {caminho_arquivo}")
                # Aqui você pode abrir o arquivo, ler seu conteúdo, etc.
                # Por exemplo, lendo o conteúdo do arquivo:
                with open(caminho_arquivo, 'r') as f:
                    conteudo = f.read()
                    print(conteudo)
            # Se for uma subpasta, você pode também iterar sobre os arquivos dentro dela
            elif os.path.isdir(caminho_arquivo):
                print(f"Encontrada subpasta: {caminho_arquivo}")
                # Ações adicionais para subpastas se necessário
