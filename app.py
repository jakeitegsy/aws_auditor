#!/usr/bin/env python3
import aws_cdk
import auditor
import os
import utilities

auditors = utilities.get_auditors()
app = aws_cdk.App()

for auditor_name in auditors:
    name = f'audit_{auditor_name}'
    auditor.Inventory(
        app, utilities.hyphenate(name),
        auditor_name=name,
        actions=auditors[auditor_name].get('actions'),
        sort_key=auditors[auditor_name].get('sort_key'),
    )

app.synth()