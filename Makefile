cat:
	cat Makefile

pesky:
	git config --global user.email "tonybutzer@gmail.com"
	git config --global user.name "tonyButzer"



publish:
	git add .
	git commit -m "sleepy work 2022 November"
	git push
