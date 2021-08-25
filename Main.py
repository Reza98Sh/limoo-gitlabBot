import contextlib
import asyncio
import re

from gitlabAPI import get_private_projects
from limoo import LimooDriver

BOT_NAME = ''  # limoo bot name
PASSWORD = ''  # password of the bot


def is_msg_valid(msg: str):
    """ Check the validity of the input message format """

    pattern = re.compile("(^/گیتلب [\da-zA-Z]{20}$)")
    res = pattern.findall(msg)
    if res:
        return True
    else:
        return False


def check_input_msg_type(event) -> bool:
    """
    make sure that the created message is not a system message and
    that it was not created by us. Non-system messages have "null" as their "type".
    (We only process events that inform us of new messages being created.)
    """

    if (event['event'] == 'message_created'
            and
            not (event['data']['message']['type']
                 or
                 event['data']['message']['user_id'] == self['id'])):

        return True
    else:
        return False


def reformat_projects_data(projects: list) -> str:
    """ Reform data to the desired string to display in the output response """

    projects_data = ''
    for project in projects:
        projects_data += project['name'] + "\n" + \
                         "Created at: " + project['created_at'] + "\n" + \
                         "Stars: " + str(project['stars']) + "\t" + \
                         "Forks: " + str(project['forks']) + "\n" + \
                         "Description: " + "\n\t" + project['description'] + "\n" + \
                         "______________________________ " + "\n"

    return projects_data


async def print_resp_msg(event, msg):
    """
    If the received message is part of a thread, it will have
    thread_root_id set and we need to reuse that thread_root_id so that
    our message ends up in the same thread. We also set
    direct_reply_message_id to the id of the message so our message is
    sent as a reply to the received message. If however, the received
    message does not have thread_root_id set, we will create a new thread
    by setting thread_root_id to the id of the received message. In this
    case, we must set direct_reply_message_id to None.
    """

    message_id = event['data']['message']['id']
    thread_root_id = event['data']['message']['thread_root_id']
    direct_reply_message_id = event['data']['message']['thread_root_id'] \
                              and event['data']['message']['id']

    # print response message
    await ld.messages.create(
        event['data']['workspace_id'],
        event['data']['message']['conversation_id'],
        msg,
        thread_root_id=thread_root_id or message_id,
        direct_reply_message_id=thread_root_id and message_id
    )


async def resp_for_valid_msg(event, input_msg):
    """ Response for valid syntax message """

    personal_access_token = input_msg[-20:]
    projects = await get_private_projects(personal_access_token)

    if projects is None:
        # Input message format is correct but recived token is not valid
        invalid_token_resp = "توکن ارسال شده صحیح نمی باشد."
        await print_resp_msg(event, invalid_token_resp)

    else:
        # Personal access token is valid
        project_names = reformat_projects_data(projects)
        await print_resp_msg(event, project_names)


async def resp_for_unvalid_msg(event):
    """ Response for unvalid syntax message """

    invalid_msg_resp = "فرمت دستور ارسالی صحیح نیست.\n \
                        برای ارسال دستور از فرمت زیر استفاده کنید: \n \
                        (تعداد کاراکترهای توکن باید برابر ۲۰ باشد) \n \
                        /گیتلب <Access Token>"

    invalid_msg_resp = re.sub('\s{2}', '\n', invalid_msg_resp)
    await print_resp_msg(event, invalid_msg_resp)


async def respond(event):
    """ Respond for the events """

    if check_input_msg_type(event):

        input_msg = event['data']['message']['text']
        validation = is_msg_valid(input_msg)
        if validation:
            await resp_for_valid_msg(event, input_msg)
        else:
            await resp_for_unvalid_msg(event)


async def listen(ld):
    forever = asyncio.get_running_loop().create_future()
    # The given event_handler will be called on the event loop thread for each
    # event received from the WebSocket. Also it must be a normal function and
    # not a coroutine therefore we create our own task so that our coroutine
    # gets executed.
    ld.set_event_handler(lambda event: asyncio.create_task(respond(event)))

    await forever


async def main():
    global ld, self

    async with contextlib.AsyncExitStack() as stack:
        ld = LimooDriver('web.limoo.im', BOT_NAME, PASSWORD)
        stack.push_async_callback(ld.close)
        # Calling ld.users.get without any arguments gets information
        # about the currently logged in user
        self = await ld.users.get()
        await listen(ld)


if __name__ == '__main__':
    
    assert BOT_NAME and PASSWORD, "Change BOT_NAME and PASSWORD values in the code!"

    asyncio.run(main())
    
        
