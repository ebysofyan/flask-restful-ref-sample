import json
import os
from typing import List

from fabric import SerialGroup
from fabric.tasks import task

user = os.environ.get("PRODUCTION_SERVER_USER", "")
connect_kwargs = {"key_filename": "~/keyfile.pem"}
try:
    hosts_str = os.environ.get("PRODUCTION_SERVER_HOSTS", "[]")
    hosts: List[str] = json.loads(hosts_str)
except Exception as e:
    print("...", str(e))
    hosts = []


@task
def deploy(ctx, *args, **kwargs):
    if len(hosts) > 0:
        group = SerialGroup(*hosts, user=user, connect_kwargs=connect_kwargs)
        group.run("sh ~/deployment-script.sh")
    else:
        raise Exception("Hosts should contain at least 1 arg")
