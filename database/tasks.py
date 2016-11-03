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
def mklog(ctx):
    open(LOG_FILE,"w")

@task(cd, mklog)
def sources(ctx):
    ctx.run("python import_data.py 2> %s" % LOG_FILE)
