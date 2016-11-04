#/bin/bash

invoke template.deploy
inv database.sources
invoke database.deploy
invoke dist_clone
invoke deploy
invoke clean_all
