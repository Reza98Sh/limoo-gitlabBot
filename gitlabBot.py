
import contextlib
import asyncio
import aiohttp
import re

from limoo import LimooDriver

BOT_NAME = 'gitlab_bot'
PASSWORD = 'rhy4er6wfjmsgtofrmum'

async def get_private_projects(token: str) -> list:

    headers = {"PRIVATE-TOKEN": token}
    async with aiohttp.ClientSession(headers=headers) as session:
        gitlab_api_url = "https://gitlab.com/api/v4/projects?owned=true"
        async with session.get(gitlab_api_url) as resp:
            projects = await resp.json()

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

        msg = event['data']['message']['text']
        validation = is_msg_valid(msg)

        if validation:
            projects = await get_private_projects(msg[-20:])

            project_names = ''
            for project in projects:
                project_names += project['name'] + '\n'

            await ld.messages.create(
                event['data']['workspace_id'],
                event['data']['message']['conversation_id'],
                project_names,
                thread_root_id=thread_root_id or message_id,
                direct_reply_message_id=thread_root_id and message_id)
        else:
            invalid_input_msg = "فرمت دستور ارسالی صحیح نیست.\n \
                                برای ارسال دستور از فرمت زیر استفاده کنید: \n \
                                /گیتلب <Access Token>"
            invalid_input_msg = re.sub('\s{2}', '\n', invalid_input_msg)
            await ld.messages.create(
                event['data']['workspace_id'],
                event['data']['message']['conversation_id'],
                invalid_input_msg,
                thread_root_id=thread_root_id or message_id,
                direct_reply_message_id=thread_root_id and message_id)


async def listen(ld):

    forever = asyncio.get_running_loop().create_future()
    ld.set_event_handler(lambda event: asyncio.create_task(respond(event)))

    await forever


async def main():

    global ld, self
    async with contextlib.AsyncExitStack() as stack:
        ld = LimooDriver('web.limoo.im', BOT_NAME, PASSWORD)
        stack.push_async_callback(ld.close)

        self = await ld.users.get()
        await listen(ld)


if __name__ == '__main__':

    asyncio.run(main())
