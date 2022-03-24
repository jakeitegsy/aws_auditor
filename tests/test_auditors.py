import tests.utilities
import utilities

class TestAuditors(tests.utilities.TestTemplates):

    def test_auditors(self):
        for auditor in utilities.get_auditors():
            with self.subTest(i=auditor):
                self.assert_templates_equal(
                    utilities.hyphenate(f'audit-{auditor}')
                )
