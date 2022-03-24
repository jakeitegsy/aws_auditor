import unittest
import os


class TestBuildDeploy(unittest.TestCase):

    @staticmethod
    def get_commit_message():
        return input("Enter commit message: ")

    def test_commit_message(self):
        os.system(f'git commit -am "{self.get_commit_message()}"')