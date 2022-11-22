device=103AF69D

cat:
	cat Makefile


dis:
	hdhomerun_config discover


help:
	hdhomerun_config ${device} get help

stat: stream
	hdhomerun_config ${device} get /tuner0/status

debug:
	hdhomerun_config ${device} get /tuner0/debug

stream:
	hdhomerun_config ${device} get /tuner0/streaminfo


cmd =  hdhomerun_config ${device} get 
sys:
	${cmd} /sys/copyright
	${cmd} /sys/debug
	${cmd} /sys/features
	${cmd} /sys/hwmodel
	${cmd} /sys/model
	${cmd} /sys/version


target:
	${cmd} /tuner0/target
