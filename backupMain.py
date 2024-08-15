import re
import os
import mapeamentoPais

from chamadaDocIntelligence import analyze_document
from ObtemPais import obter_pais_por_cidade
from formularioPF import preencheForms

def main():
    diretorio_pdf = "C:\\Deloitte\\RPA - Policia Federal\\Documentos\\RE_Document Inteligence\\"
    arquivos_pdf = [f for f in os.listdir(diretorio_pdf) if f.endswith('.pdf')]

    for pdf_file in arquivos_pdf:
        file_path = os.path.join(diretorio_pdf, pdf_file)
        nome_arquivo = os.path.splitext(pdf_file)[0]

        if 'passaporte' in nome_arquivo.lower():
            model_id = "RPAPOLICIAFEDERAL"
        elif 'pedido' in nome_arquivo.lower():
            model_id = "RPAPOLICIAFEDERALPEDVISTO2"
        elif 'visto' in nome_arquivo.lower():
            model_id = "FieldsVisto2"    

        result = analyze_document(file_path, model_id)
        field_values = {}

        def store_field_values(analysis_result):
            for field in analysis_result["fields"]:
                if isinstance(field["value"], list):
                    field_values[field["name"]] = []
                    for item in field["value"]:
                        item_values = {key: val for key, val in item.items()}
                        field_values[field["name"]].append(item_values)
                else:
                    field_values[field["name"]] = field["value"]

        store_field_values(result)

        field_value_str = str(field_values)
        print(field_value_str)

        if model_id == "RPAPOLICIAFEDERALPEDVISTO2":
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
            estado_civil = re.search(r'(?<=ESTADO CIVIL\':\s\').*(?=\',\s\'Data nascimento)', field_value_str).group(0)
            print(estado_civil)
            if re.search(r'\(a\)', estado_civil):
                estado_civil = re.search(r'\w+(?=\()', estado_civil).group(0)
                print(estado_civil)
            dt_nascimento = re.search(r'(?<=Data nascimento\':\s\').*(?=\',\s\'Pais expedidor)', field_value_str).group(0)
            print(dt_nascimento)
            pais_expedidor = re.search(r'(?<=Pais expedidor\':\s\').*(?=\'\}\])', field_value_str).group(0)
            print(pais_expedidor)
            pais_expedidor = mapeamentoPais.obter_pais_com_acento(pais_expedidor)
            print(pais_expedidor)

        elif model_id == "RPAPOLICIAFEDERAL":
            numero_passaporte = re.search(r'(?<=Passaport number\':\s\').*(?=\'\}\])', field_value_str).group(0)
            print(numero_passaporte)

        elif model_id == "FieldsVisto2":
            dt_concessao = re.search(r'(?<=DATA CONCESSAO\':\s\').*(?=\',\s\'CIDADE)', field_value_str).group(0)
            print(dt_concessao)
            numero_visto = re.search(r'(?<=numero visto\':\s\').*(?=\'\}\])', field_value_str).group(0)
            print(numero_visto)

            meses = {
                "JAN": "01", "FEV": "02", "FEB": "02", "MAR": "03",
                "ABR": "04", "APR": "04", "MAI": "05", "MAY": "05",
                "JUN": "06", "JUL": "07", "AGO": "08", "AUG": "08",
                "SET": "09", "SEP": "09", "OUT": "10", "OCT": "10",
                "NOV": "11", "DEZ": "12", "DEC": "12"
            }

            match = re.search(r"(\d{2})\s([A-Z]{3})\/([A-Z]{3})\s(\d{4})", dt_concessao.upper())

            if match:
                dia = match.group(1)
                mes_abr = match.group(2)
                ano = match.group(4)
                mes = meses[mes_abr]
                dt_concessao = f"{dia}/{mes}/{ano}"
                print(dt_concessao)

            cidade = re.search(r'(?<=CIDADE\':\s\').*(?=\',\s\'numero visto)', field_value_str).group(0)
            print(cidade)

    cidade_nasc = re.search(r'^[^,]+', nascido_em).group(0)
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

    if pais == "Estados Unidos da América":
        pais = "Estados Unidos"
        print(pais)

    formulario = preencheForms(
        cidade_nasc, pais_nasc, nome, sobrenome, sexo, nascido_em, nacionalidade, pai, mae,
        estado_civil, dt_nascimento, numero_passaporte, pais_passaporte, dt_concessao,
        cidade, pais, numero_visto, pais_expedidor
    )
    if formulario:
        print(formulario)

if __name__ == "__main__":
    sua_chave_api = "fd5d9ed8ef6443378287b9838f16ce34"
    main()
