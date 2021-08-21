import asyncio
import unittest

from gitlabAPI import get_private_projects

MY_GITLAB_TOKEN = "e5HSLHCaGewoJ5bfSNAH"

BOT_NAME = 'gitlab_bot'
PASSWORD = 'rhy4er6wfjmsgtofrmum'


# TODO: Add test for limoo response

class GitlabTests(unittest.TestCase):


    def test_receive_projects(self):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(get_private_projects(MY_GITLAB_TOKEN))
        loop.close()

        first_project_name = result[-1]['name']
        self.assertEqual(first_project_name, 'project01')


if __name__ == '__main__':

    unittest.main()

