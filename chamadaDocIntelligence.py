from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import json
import re


def analyze_document(file_path, model_id, endpoint="https://projetotouchless.cognitiveservices.azure.com/", key="5b995d2fb12d4933b7bc4e2b87e8a9f7"):
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(file_path, "rb") as f:
        poller = document_analysis_client.begin_analyze_document(
            model_id=model_id, document=f
        )

    result = poller.result()

    analysis_result = {
        "fields": [],
        "lines": [],
        "selection_marks": []
    }

    def table_to_json(name, field):
        matriz = []
        for line in field.value:
            dici = {}
            line = line.to_dict()
            for key, value in line['value'].items():
                dici[key] = value['value']
            matriz.append(dici)
        analysis_result["fields"].append({
            "name": name,
            "type": field.value_type,
            "value": matriz,
            "confidence": field.confidence
        })

    for idx, document in enumerate(result.documents):
        for name, field in document.fields.items():
            if field.value:
                if field.value_type == 'list':
                    table_to_json(name, field)
                    continue
            field_value = field.value if field.value else field.content
            analysis_result["fields"].append({
                "name": name,
                "type": field.value_type,
                "value": field_value,
                "confidence": field.confidence
            })

    # Iterate over tables, lines, and selection marks on each page
    for page in result.pages:
        for line in page.lines:
            try:
                content = line.content
            except UnicodeEncodeError:
                content = line.content.encode('utf-8', 'ignore').decode('utf-8')
            analysis_result["lines"].append({
                "page": page.page_number,
                "content": content
            })
        if page.selection_marks:
            for selection_mark in page.selection_marks:
                analysis_result["selection_marks"].append({
                    "page": page.page_number,
                    "state": selection_mark.state,
                    "confidence": selection_mark.confidence
                })

    return analysis_result


