#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import json
import dockerfile_apps

with open('setup/init.json') as json_file:
    init_data = json.load(json_file)

app = init_data.get("app")
version = init_data.get("app_version")

if app == None or version == None:
    import pprint
    pprint.pprint(app)
    pprint.pprint(version)
    print("Invalid value: init.json")
    exit(1)
else:
    return_code = dockerfile_apps.write_dockerfile(app, version)
    exit(return_code)
