#!/usr/bin/env python3
import aws_cdk
import auditor
import json
import os
import utilities

auditors = utilities.get_auditors()
app = aws_cdk.App()

for auditor_name in auditors:
    auditor.Inventory(
        app, utilities.hyphenate(f'audit_{auditor_name}'),
        stack_id=auditor_name,
        actions=auditors[auditor_name].get('actions'),
        sort_key=auditors[auditor_name].get('sort_key'),
    )

app.synth()