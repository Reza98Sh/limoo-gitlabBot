
import contextlib
import asyncio
import re

from gitlabAPI import get_private_projects
from limoo import LimooDriver

BOT_NAME = 'gitlab_bot'
PASSWORD = 'rhy4er6wfjmsgtofrmum'


def is_msg_valid(msg: str):
    pattern = re.compile("(^/گیتلب [\da-zA-Z]{20}$)")
    res = pattern.findall(msg)
    if res:
        return True
    else:
        return False


def check_input_msg_type(event) -> bool:
    if (event['event'] == 'message_created'
            and
        not (event['data']['message']['type'] or event['data']['message']['user_id'] == self['id'])):

        return True
    else:
        return False


def get_project_names(projects: list) -> str:

    project_names = ''
    for project in projects:
        project_names += project['name'] + '\n'

    return  project_names


async def respond(event):

    if check_input_msg_type(event):

        message_id = event['data']['message']['id']
        thread_root_id = event['data']['message']['thread_root_id']
        direct_reply_message_id = event['data']['message']['thread_root_id'] \
            and event['data']['message']['id']

        input_msg = event['data']['message']['text']
        validation = is_msg_valid(input_msg)
        if validation:
            personal_access_token = input_msg[-20:]
            projects = await get_private_projects(personal_access_token)
            if projects is None:
                invalid_token_msg = "توکن ارسال شده صحیح نمی باشد."
                await ld.messages.create(
                    event['data']['workspace_id'],
                    event['data']['message']['conversation_id'],
                    invalid_token_msg,
                    thread_root_id=thread_root_id or message_id,
                    direct_reply_message_id=thread_root_id and message_id)
            else:
                project_names = get_project_names(projects)

                await ld.messages.create(
                    event['data']['workspace_id'],
                    event['data']['message']['conversation_id'],
                    project_names,
                    thread_root_id=thread_root_id or message_id,
                    direct_reply_message_id=thread_root_id and message_id)
        else:
            invalid_input_msg = "فرمت دستور ارسالی صحیح نیست.\n \
                                برای ارسال دستور از فرمت زیر استفاده کنید: \n \
                                (تعداد کاراکترهای توکن باید برابر ۲۰ باشد) \n \
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
