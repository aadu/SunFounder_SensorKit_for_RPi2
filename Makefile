.PHONY: format ls-files sync

format:
	make ls-files | xargs -n1 yapf --style setup.cfg -i
	make ls-files | xargs -n1 isort

# http://serverfault.com/questions/215007/associate-name-with-ip-for-ssh	#

ls-files:
	@find ./Python -type f -name '*.py'

sync:
	rsync -avzh -e "ssh -i ${HOME}/.ssh/id_rsa" --progress \
	../sensorkit pi:/home/pi

install:
	rsync -avzh -e "ssh -i ${HOME}/.ssh/id_rsa" --progress \
	config/ pi:/home/pi/.jupyter


# sudo apt-get update && sudo apt-get install tmux
# tmux new -s jupyter
# jupyter notebook
