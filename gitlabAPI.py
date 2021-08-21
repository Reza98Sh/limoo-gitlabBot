import aiohttp

# TODO: Add comment and docstring

async def request_projects(token: str):
    headers = {"PRIVATE-TOKEN": token}
    async with aiohttp.ClientSession(headers=headers) as session:
        gitlab_api_url = "https://gitlab.com/api/v4/projects?owned=true"
        async with session.get(gitlab_api_url) as resp:
            projects = await resp.json()

        # Connection error handling
            try:
                if resp.status == 200:
                    return projects, resp.status
                else:
                    return None, resp.status
            except aiohttp.ServerConnectionError:
                return None, None


def extract_usfull_data(projects: list) -> list:
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


async def get_private_projects(token: str):

    resp, staus = await request_projects(token)

    if staus == 200:
        projects_cleared = extract_usfull_data(resp)
        return projects_cleared
    else:
        return None


