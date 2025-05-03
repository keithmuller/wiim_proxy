# DESTDIR should match WorkingDirectory= in wiim_proxy.service
DESTDIR	=	/opt/wiim_proxy
SYSMD	=	/etc/systemd/system
# OWNER should match User= in the file wiim_proxy.service
OWNER	=	www-data
GROUP	=	www-data
FILES	=	__init__.py wiim_device.py wiim_proxy.ini wiim_proxy.py \
		wiim_proxy.service 

.PHONY:	all test install service_install service_start service_stop pkg_install

all:
	@echo "Follow the instructions in README.md"

install:
	-sudo mkdir $(DESTDIR)
	sudo cp -p $(FILES) $(DESTDIR)
	sudo chown -R $(OWNER):$(GROUP) $(DESTDIR)

# The following targets only need to be run once!

pkg_install:
	sudo apt-get -y install uwsgi
	sudo apt-get -y install uwsgi-plugin-python3
	sudo apt-get -y install python3-flask

service_install:
	sudo ln -sf $(DESTDIR)/wiim_proxy.service $(SYSMD)/wiim_proxy.service
	sudo systemctl enable wiim_proxy.service

# these targets are optional

service_start:
	sudo systemctl start wiim_proxy.service

service_stop:
	sudo systemctl stop wiim_proxy.service

# only for testing when the service is not running
test:
	uwsgi --ini wiim_proxy.ini
