from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import json
import re
import os

from chamadaDocIntelligence import analyze_document
from ObtemPais import obter_pais_por_cidade
from formularioPF import preencheForms

def main():

    diretorio_pdf = "C:\\Deloitte\\RPA - Policia Federal\\Documentos\\RE_Document Inteligence\\"
    arquivos_pdf = [f for f in os.listdir(diretorio_pdf) if f.endswith('.pdf')]

    for pdf_file in arquivos_pdf:
        file_path = os.path.join(diretorio_pdf, pdf_file)
        #print(file_path)
        nome_arquivo = os.path.splitext(pdf_file)[0]  # Utiliza o nome do arquivo sem extensão como model_id
        #print(nome_arquivo)
        if 'passaporte' in str(nome_arquivo).lower():
            model_id = "RPAPOLICIAFEDERAL"
        elif 'pedido' in str(nome_arquivo).lower():
            model_id = "RPAPOLICIAFEDERALPEDVISTO"
        elif 'visto' in str(nome_arquivo).lower():
            model_id = "FieldsVisto"    

        result = analyze_document(file_path, model_id)

        field_values = {}

        def store_field_values(analysis_result):
            for field in analysis_result["fields"]:
                if isinstance(field["value"], list):
                    field_values[field["name"]] = []
                    for item in field["value"]:
                        item_values = {}
                        for key, val in item.items():
                            item_values[key] = val
                        field_values[field["name"]].append(item_values)
                else:
                    field_values[field["name"]] = field["value"]

        store_field_values(result)

        
        field_value_str = str(field_values)
        #print(field_value_str)

        if model_id == "RPAPOLICIAFEDERALPEDVISTO":
            nome = re.search(r'(?<=NOME\':\s\').*(?=\',\s\'SEXO)', field_value_str).group(0)
            print(nome)
            sexo = re.search(r'(?<=SEXO\':\s\').*(?=\',\s\'NASCIDO EM)', field_value_str).group(0)
            print(sexo)
            nascido_em = re.search(r'(?<=NASCIDO EM\':\s\').*(?=\',\s\'NACIONALIDADE)', field_value_str).group(0)
            print(nascido_em)
            nacionalidade = re.search(r'(?<=NACIONALIDADE\':\s\').*(?=\',\s\'PAI)', field_value_str).group(0)
            print(nacionalidade)
            pai = re.search(r'(?<=PAI\':\s\').*(?=\',\s\'MAE)', field_value_str).group(0)
            print(pai)
            mae = re.search(r'(?<=MAE\':\s\').*(?=\',\s\'ESTADO CIVIL)', field_value_str).group(0)
            print(mae)
            estado_civil = re.search(r'(?<=ESTADO CIVIL\':\s\').*(?=\'\}\])', field_value_str).group(0)
            print(estado_civil)
        elif model_id == "RPAPOLICIAFEDERAL":
            dt_nascimento = re.search(r'(?<=Date of birth\':\s\').*(?=\',\s\'Sex)', field_value_str).group(0)
            print(dt_nascimento)
            numero_passaporte = re.search(r'(?<=Passaport number\':\s\').*(?=\'\}\])', field_value_str).group(0)
            print(numero_passaporte)
            pais_expedidor = re.search(r'(?<=authority\':\s\').*(?=\',\s\'Type)', field_value_str).group(0)
            print(pais_expedidor)
        elif model_id == "FieldsVisto":
            dt_concessao = re.search(r'(?<=DATA CONCESSAO\':\s\').*(?=\',\s\'CIDADE)', field_value_str).group(0)
            print(dt_concessao)
            cidade = re.search(r'(?<=CIDADE\':\s\').*(?=\'\}\])', field_value_str).group(0)
            print(cidade)


    cidade_nasc = re.search(r'(.*(?=\,\s\w+\,))', nascido_em).group(0)
    print(cidade_nasc)
    pais_nasc = re.search(r'[^,]*$', nascido_em).group(0).strip()
    print(pais_nasc)
    sobrenome = re.search(r'\s+(.*)', nome).group(0).strip()
    print(sobrenome)
    nome = re.search(r'\w+(?=\s)', nome).group(0).strip()
    print(nome)
    pais = obter_pais_por_cidade(cidade, sua_chave_api)
    if pais:
        print(pais)
    pais_passaporte = obter_pais_por_cidade(pais_expedidor, sua_chave_api)
    if pais_expedidor:
        print(pais_expedidor)


    formulario = preencheForms(cidade_nasc, pais_nasc, nome, sobrenome, sexo, nascido_em, nacionalidade, pai, mae, 
                               estado_civil,dt_nascimento, numero_passaporte, pais_passaporte, dt_concessao, cidade, pais)        
    if formulario:
        print(formulario)


if __name__ == "__main__":
    sua_chave_api = ""
    main()
