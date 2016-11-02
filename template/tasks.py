#!/usr/bin/env python3
from invoke import task
import os
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))


@task()
def test(ctx):
    ctx.run("echo \"template - OK\"")

@task()
def cd(ctx):
    os.chdir(ROOT_PATH)

@task(cd)
def npm_install(ctx):
    ctx.run("npm install")

@task(npm_install)
def grunt_build(ctx):
    ctx.run("grunt build")

@task(grunt_build)
def copy_js(ctx):
    ctx.run("cp dist/js/app.js ../DormancyBase/themes/DormancyBase/static/js/app.js")

@task(grunt_build)
def copy_css(ctx):
    ctx.run("cp dist/css/style.css ../DormancyBase/themes/DormancyBase/static/css/style.css")
    ctx.run("cp node_modules/uikit/dist/fonts/* ../DormancyBase/themes/DormancyBase/static/css/fonts/")

@task(copy_js, copy_css)
def deploy(ctx):
    print(" template - DONE")
