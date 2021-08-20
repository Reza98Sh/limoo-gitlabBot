import requests
import json
from pprint import pprint


def getPrivateProjects(token):
    
    projects = requests.get("https://gitlab.com/api/v4/projects?owned=true",
                        headers={"PRIVATE-TOKEN":token}).json()

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



pprint(getPrivateProjects("e5HSLHCaGewoJ5bfSNAH"))



