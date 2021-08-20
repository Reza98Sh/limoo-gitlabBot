import requests
import json
import contextlib
import asyncio
import re

from limoo import LimooDriver
from pprint import pprint

MY_GITLAB = "e5HSLHCaGewoJ5bfSNAH"


def getPrivateProjects(token: str):

    projects = requests.get("https://gitlab.com/api/v4/projects?owned=true",
                            headers={"PRIVATE-TOKEN": token}).json()

    projects_cleared = []

    for project in projects:
        p = {}
        if project['pages_access_level'] == 'private':

            p['name'] = project['name']
            p['created_at'] = project['created_at'][0:10]
            p['stars'] = project['star_count']
            p['forks'] = project['forks_count']
            p['description'] = project['description']

            projects_cleared.append(p)

    return projects_cleared


def is_msg_valid(msg: str) -> bool:
    pattern = re.compile("(^/گیتلب [\d|a-z|A-Z]{20}$)")
    res = pattern.findall(msg)
    if res:
        return True
    else:
        return False


async def respond(event):
    if (event['event'] == 'message_created'
        and not (event['data']['message']['type']
                 or event['data']['message']['user_id'] == self['id'])):

        message_id = event['data']['message']['id']
        thread_root_id = event['data']['message']['thread_root_id']
        direct_reply_message_id = event['data']['message']['thread_root_id'] \
            and event['data']['message']['id']

        validation = is_msg_valid(event['data']['message']['text'])
        

        await ld.messages.create(
            event['data']['workspace_id'],
            event['data']['message']['conversation_id'],
            event['data']['message']['text'],
            thread_root_id=thread_root_id or message_id,
            direct_reply_message_id=thread_root_id and message_id)


async def listen(ld):

    forever = asyncio.get_running_loop().create_future()
    ld.set_event_handler(lambda event: asyncio.create_task(respond(event)))

    await forever


async def main():
    global ld, self
    async with contextlib.AsyncExitStack() as stack:
        ld = LimooDriver('web.limoo.im', 'gitlab_bot', 'rhy4er6wfjmsgtofrmum')
        stack.push_async_callback(ld.close)

        self = await ld.users.get()
        await listen(ld)


asyncio.run(main())
