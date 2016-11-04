#!/usr/bin/env python3
from invoke import task
import os

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
LOG_FILE = os.path.join(ROOT_PATH, "dist", "process.log")

@task()
def test(ctx):
    ctx.run("echo \"database - OK\"")

@task()
def cd(ctx):
    os.chdir(ROOT_PATH)

@task()
def mkdirs(ctx):
    dirs = ["dist", "download", "hugo_files"]
    for cdir in dirs:
        if not os.path.exists(os.path.join(ROOT_PATH, cdir)):
            os.makedirs(os.path.join(ROOT_PATH, cdir))

@task()
def mklog(ctx):
    open(LOG_FILE,"w")

@task(cd, mklog, mkdirs)
def sources(ctx):
    ctx.run("python import_data.py 2>> %s" % LOG_FILE)

@task(cd, mklog, mkdirs)
def export_hugo(ctx):
    ctx.run("python export_hugo.py 2>> %s" % LOG_FILE)

@task(export_hugo)
def copy_brows(ctx):
    ctx.run("cp hugo_files/brows.csv ../DormancyBase/static/data/brows.csv")

@task(copy_brows)
def deploy(ctx):
    print(" template - DONE")
