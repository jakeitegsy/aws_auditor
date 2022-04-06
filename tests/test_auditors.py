import tests.utilities
import utilities
import unittest

class TestAuditors(tests.utilities.TestTemplates):

    # @unittest.skip
    def test_auditors(self):
        for auditor in utilities.get_auditors():
            with self.subTest(i=auditor):
                self.assert_templates_equal(
                    utilities.hyphenate(f'audit-{auditor}')
                )
