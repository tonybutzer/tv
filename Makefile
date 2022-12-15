cat:
	cat Makefile

pesky:
	git config --global user.email "tonybutzer@gmail.com"
	git config --global user.name "tonyButzer"



publish:
	git add .
	git commit -m "sleepy work 2022 November"
	git push



sudopass:
	@echo visudo
	@echo 'tony ALL=(ALL) NOPASSWD: ALL'
	@echo should be last line


build:
	docker build -t tv .


dtest:
	docker run -it --network host tv bash


toctool:
	wget https://raw.githubusercontent.com/ekalinin/github-markdown-toc/master/gh-md-toc
	chmod a+x gh-md-toc
	sudo mv gh-md-toc /usr/local/bin


toc:
	gh-md-toc --insert --no-backup README.md

