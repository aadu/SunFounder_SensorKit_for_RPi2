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
