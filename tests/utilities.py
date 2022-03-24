import unittest
import json
import os
import time
import datetime

true = True
false = False

def log(message):
    result = f"{datetime.datetime.now()}::{message}\n"
    print(result)
    return result

def log_performance(result):
    os.makedirs('logs', exist_ok=True)
    with open('logs/performance.log', 'a') as writer:
        writer.write(result)

def time_it(function, *args, description='run process', **kwargs):
    start_time = time.time()
    function(*args, **kwargs)
    result = f'Time taken to {description}::  {time.time() - start_time:.4f} seconds'
    log_performance(log(result))


class TestTemplates(unittest.TestCase):

    maxDiff = None

    def assert_template_equal(self, stack_name):
        os.system('clear')
        time_it(os.system, f'cdk ls {stack_name} --version-reporting=false --path-metadata=false --asset-metadata=false', description=f'synthesize stack: {stack_name}')
        with open(f'cdk.out/{stack_name}.template.json') as template:
            with open(f'tests/templates/{stack_name}.template.json') as fixture:
                return self.assertEqual(json.load(template), json.load(fixture))