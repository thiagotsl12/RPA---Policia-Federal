from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from os import getenv
import sys
import io
import json


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
 
endpoint = "https://timbroocr.cognitiveservices.azure.com/"
key = "50719944ab614a25b04f691975530281"
 
if len(sys.argv) != 3:
    print("Usage: python script.py <file_path> <model_id>")
    sys.exit(1)
 
file_path = sys.argv[1]
model_id = sys.argv[2]
 
 
document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)
 
with open(file_path, "rb") as f:
    poller = document_analysis_client.begin_analyze_document(
        model_id=model_id, document=f
    )
result = poller.result()
 
def table_to_json(name, field):
    matriz = []
    for line in field.value:
        dici = {}
        line = line.to_dict()
        for key, value in line['value'].items():
            dici[key] = value['value']
        matriz.append(dici)
    print(
        f"......found {name} field of type {field.value_type} with value '{json.dumps(matriz)}' and with confidence {field.confidence}"
    )

for idx, document in enumerate(result.documents):
    for name, field in document.fields.items():
        if field.value:
            if field.value_type == 'list':
                table_to_json(name, field)
                continue
        field_value = field.value if field.value else field.content
        print(
            f"......found {name} field of type {field.value_type} with value '{field_value}' and with confidence {field.confidence}"
        )
 
# iterate over tables, lines, and selection marks on each page
for page in result.pages:
    print(f"\nLines found on page {page.page_number}")
    for line in page.lines:
        try:
            print(f"...Line '{line.content}'")
        except UnicodeEncodeError:
            print(f"...Line '{line.content.encode('utf-8', 'ignore').decode('utf-8')}'")
    if page.selection_marks:
        print(f"\nSelection marks found on page {page.page_number}")
        for selection_mark in page.selection_marks:
            print(
                f"...Selection mark is '{selection_mark.state}' and has a confidence of {selection_mark.confidence}"
            )
print("-----------------------------------")