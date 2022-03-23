#!/usr/bin/env python3
import aws_cdk
import auditor
import json
import os

app = aws_cdk.App()

with open('auditors.json') as file:
    auditors = json.load(file)

for auditor_name in auditors:
    print(f'audit_{auditor_name}')
    print(auditors[auditor_name]['actions'])
    auditor.Inventory(
        app, auditor_name,
        auditor_name=auditor_name,
        actions=auditors[auditor_name].get('actions'),
        sort_key=auditors[auditor_name].get('sort_key'),
    )

app.synth()