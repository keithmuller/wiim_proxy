***wiim_proxy*** is a http proxy server that provides a http only control interface
to a wiim device.

***Use case***: Using a sofabaton x1s to control a wiim device

You will add the wiim device to sofabaton x1s as wifi virtual device to control a wiim
device.

***Implematition information***

This server uses uwsgi and is intended for use only on internal networks
that are safely behind a firewall.

This package uses systemd to start wiim_proxy at boot.

This server was tested using raspios (bookworm) 64-bit on a pi4 and pi5

This server supports all the controls (except power) found on the wiim remote.
It uses the published wiim http(s) interface to communicate with the wiim device

***Current limitations:*** Each wiim_proxy server can only control one wiim device at this time. 
Thus you would need one wiim_proxy server with a unique port number for each wiim device.

***This code was tested with a wiim_ultra. Other wiim_devices may need changes.***

# How to Install

(1) Examine and maybe edit the file Makefile. Pay attention to the settings at the top of the file.
You should not need to change the values for the following:
    
&nbsp;DESTDIR SYSMD OWNER GROUP
    
&nbsp;Do not change the value for: FILES.

(2) Edit wiim_proxy.ini. Change the ip address (10.0.1.103) in the line"pyargv=10.0.1.103" 
    to the ip address of the wiim device you want to control
  
(3) Run the follow to make sure the port number is not being used, this should have no match.:
        
        netstat -a | grep 5050
  
(4) Only If you got a return like:
        
&nbsp; tcp   0   0 0.0.0.0:5050    0.0.0.0:*       LISTEN  
        
Edit wiim_proxy.ini and change the port number (5050) in the line "http-socket = :5050" to a port that is not used

(5) This package is set to be installed in /opt/wiim_proxy and run as user
    and group www-data. If you want to change this, you will need to adjust the settings in
    the files: wiim_proxy.service and Makefile to be consistent.

(6) Make sure you can sudo first. Now copy the files to /opt/wiim_proxy:
    
    make install

(7) Now use make to install the required packages:
    
    make pkg_install

We use systemd to start the wiim_proxy server at boot 
    
(8) Create a symbolic link /etc/systemd/system/wiim_proxy.service that points at
       /opt/wiim_proxy/wiim_proxy.service and then enable wiim_proxy to start at boot:
      
       make service_install
       
(9) ***Optional step only if you want to start it now before a reboot:***
    
    make service_start

(10) After you have started wiim_proxy, running the following should return a line that looks like:

&nbsp; tcp   0   0 0.0.0.0:5050    0.0.0.0:*       LISTEN 

      netstat -a | grep 5050

(11) Do a reboot and try step (10) above to make sure all is well

(12) Test the proxy server.
   
&nbsp; As an example, assume the ip where wiim_proxy is running is 10.0.1.153
    The port number is 5050. The ip address of the wiim device is 10.0.1.103

&nbsp; From any web browser (or use curl) connect to:

&nbsp; http://10.0.1.153:5050/input/line-in
   
&nbsp; You should get:

&nbsp; ok

&nbsp; in the browser.

***End of install process***

# list of commands

In the following list ***$ip*** is the name or ip address of the system where this
server is running and ***$port*** is its port number ("http-socket = :5050")

http://$ip:$port/media/play

http://$ip:$port/media/pause

http://$ip:$port/media/toggle

http://$ip:$port/media/prev

http://$ip:$port/media/next

(***$int*** below must be between 0 and 100)
    
http://$ip:$port/vol/up

http://$ip:$port/vol/up/$int

http://$ip:$port/vol/down

http://$ip:$port/vol/down/$int

http://$ip:$port/vol/$int

http://$ip:$port/mute/on

http://$ip:$port/mute/off

http://$ip:$port/mute/toggle

http://$ip:$port/input/line-in

http://$ip:$port/input/wifi 

(command directly above also works with ethernet connected wiims)

http://$ip:$port/input/hdmi

http://$ip:$port/input/optical

http://$ip:$port/input/phono

http://$ip:$port/input/bluetooth

http://$ip:$port/output/optical

http://$ip:$port/output/line-out

http://$ip:$port/output/coax

http://$ip:$port/output/headphone

http://$ip:$port/output/bluetooth

http://$ip:$port/output/dlna

***$int*** preset below must be between 1 and 12 inclusive

http://$ip:$port/preset/$int

wiim_proxy is backwards compatible with the published Wiim API.

http://$ip:$port/httpapi.asp?command=$command

http://$ip:$port/command/$command
