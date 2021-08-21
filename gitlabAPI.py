import aiohttp


async def request_projects(token: str):
    """ Download user project metadata with gitlab API """

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


def extract_desired_data(projects: list) -> list:
    """ Extract desired data about private projects and save it in list """

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

    # Get response and status code of request
    resp, staus = await request_projects(token)

    # Server response
    if staus == 200:
        projects_cleared = extract_desired_data(resp)
        return projects_cleared
    else:
        return None


