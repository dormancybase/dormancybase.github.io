#!/usr/bin/env python3
from invoke import task
import os

from import_data import process_sources

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))


@task()
def test(ctx):
    ctx.run("echo \"database - OK\"")

@task()
def sources(ctx):
    process_sources("dist/sources.json")
