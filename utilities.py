import json

def hyphenate(value):
    return value.replace('_', '-')

def get_auditors():
    with open('auditors.json') as file:
        return json.load(file)