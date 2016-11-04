#/bin/bash

invoke template.deploy
invoke database.deploy
invoke dist_clone
invoke deploy
invoke clean_all
