import unittest
import json
import os


class TestAuditor(unittest.TestCase):

    def test_auditors(self):
        os.system('cdk ls')
        self.assertEqual(1, 1)