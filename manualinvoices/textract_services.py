import boto3
import json
from django.conf import settings
import os

class TextractInvoiceExtractor:
    def __init__(self):
        self.client = boto3.client(
            'textract',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

    def extract_data(self, file_path):
        with open(file_path, 'rb') as file:
            response = self.client.analyze_document(
                Document={'Bytes': file.read()},
                FeatureTypes=['FORMS', 'TABLES']
            )

        extracted_data = {
            'InvoiceDetails': {},
            'SupplierInfo': {},
            'BillingDetails': {},
            'ItemDetails': [],
            'BankDetails': {},
            'Summary': {}
        }

        block_map = {block['Id']: block for block in response['Blocks']}
        key_map = {}
        value_map = {}

        for block in response['Blocks']:
            if block['BlockType'] == 'KEY_VALUE_SET':
                if 'KEY' in block['EntityTypes']:
                    key_map[block['Id']] = block
                if 'VALUE' in block['EntityTypes']:
                    value_map[block['Id']] = block

        for key_id, key_block in key_map.items():
            value_id = self._find_value_for_key(key_block, value_map)
            key_text = self._get_text(key_block, block_map)
            value_text = self._get_text(value_map.get(value_id), block_map)

            if key_text and value_text:
                self._classify_data(key_text, value_text, extracted_data)

        for block in response['Blocks']:
            if block['BlockType'] == 'TABLE':
                table_data = self._extract_table(block, block_map)
                extracted_data['ItemDetails'].append(table_data)

        # Extract key fields directly for simplified access
        key_fields = {
            "Invoice Number": extracted_data['InvoiceDetails'].get("INVOICE NO.", "N/A"),
            "Invoice Date": extracted_data['InvoiceDetails'].get("ISSUE DATE", "N/A"),
            "Total Amount": extracted_data['Summary'].get("TOTAL", "N/A")
        }

        return {"key_fields": key_fields, "line_items": extracted_data['ItemDetails']}

    def _find_value_for_key(self, key_block, value_map):
        for relationship in key_block.get('Relationships', []):
            if relationship['Type'] == 'VALUE':
                for value_id in relationship['Ids']:
                    if value_id in value_map:
                        return value_id
        return None

    def _get_text(self, block, block_map):
        text = ''
        if 'Relationships' in block:
            for rel in block['Relationships']:
                if rel['Type'] == 'CHILD':
                    for child_id in rel['Ids']:
                        word_block = block_map[child_id]
                        if word_block['BlockType'] == 'WORD':
                            text += word_block['Text'] + ' '
                        elif word_block['BlockType'] == 'LINE':
                            text += word_block['Text'] + ' '  # Capture full lines too
        return text.strip()

    def _extract_table(self, table_block, block_map):
        table_data = []
        for relationship in table_block['Relationships']:
            if relationship['Type'] == 'CHILD':
                for cell_id in relationship['Ids']:
                    cell_block = block_map[cell_id]
                    if cell_block['BlockType'] == 'CELL':
                        cell_text = self._get_text(cell_block, block_map)
                        table_data.append(cell_text)
        return table_data

    def _classify_data(self, key, value, extracted_data):
        key_lower = key.lower()
        if 'invoice no' in key_lower or 'invoice' in key_lower:
            extracted_data['InvoiceDetails']['INVOICE NO.'] = value
        elif 'issue date' in key_lower or 'date' in key_lower:
            extracted_data['InvoiceDetails']['ISSUE DATE'] = value
        elif 'total' in key_lower:
            extracted_data['Summary']['TOTAL'] = value
        elif 'gstin' in key_lower or 'pan' in key_lower:
            extracted_data['SupplierInfo'][key] = value
        elif 'billing' in key_lower or 'shipping' in key_lower:
            extracted_data['BillingDetails'][key] = value
        elif 'account' in key_lower or 'bank' in key_lower:
            extracted_data['BankDetails'][key] = value
        else:
            extracted_data['ItemDetails'].append({key: value})  