#!/usr/bin/env python3
from invoke import task
from invoke import Collection
import template.tasks
import database.tasks
import DormancyBase.tasks
import os

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
dist_path = "dist"
git_url = "git@github.com:dormancybase/dormancybase.github.io"
main_branch = "master"
deploy_branch = "gh-pages"

ns = Collection()
@task()
def test(ctx):
    ctx.run("echo \"main - OK\"")
ns.add_task(test)

ns.add_collection(template.tasks, 'template')
ns.add_collection(database.tasks, 'database')
ns.add_collection(DormancyBase.tasks, 'site')
