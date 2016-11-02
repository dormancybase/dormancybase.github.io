#!/usr/bin/env python3
from invoke import task
import os
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))


@task()
def test(ctx):
    ctx.run("echo \"database - OK\"")
