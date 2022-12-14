cat:
	cat Makefile

isc:
	sudo apt install isc-dhcp-server

start:
	sudo cp ./dhcp.conf_template /etc/dhcp/dhcpd.conf
	sudo systemctl restart isc-dhcp-server
