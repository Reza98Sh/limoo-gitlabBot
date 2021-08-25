import asyncio
import unittest

from gitlabAPI import get_private_projects

GITLAB_TOKEN = "" # Your gitlab personal access token


class GitlabTests(unittest.TestCase):

    name_of_first_project = '' #  Your first private project name

    def test_receive_projects(self):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(get_private_projects(GITLAB_TOKEN))
        loop.close()

        first_project_name = result[-1]['name']
        self.assertEqual(first_project_name, name_of_first_project)


if __name__ == '__main__':

    unittest.main()
