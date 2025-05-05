***wiim_proxy*** is a http proxy server that provides a http only control interface
to any wiim device that supports the offical http(s) interface.

wiim_proxy supports all the controls (except the power and voice command) found on the wiim remote
as well as many of the commands described in the offical wiim http(s) interface document.

***Example use case for this software***: Controlling a wiim device from a Sofabaton x1s.

On the sofabaton x1s, create a wifi virtual device to connect via http to a wiim_proxy server running on a raspberry pi.

***Implematition information***

My wiim_proxy test/development environment is as follows:

&nbsp; (a) raspberry pi4 (or pi5) running raspios (bookworm) 64-bit to host the wiim_proxy server process.

&nbsp; (b) ***wiim_ultra*** connected to a wiim vibelink.

&nbsp; (c) systemd is used to start the wiim_proxy server process on the pi5/pi4 at boot time.

&nbsp; (d) uwsgi (alone) is used as the intended use case is an internal home network safely behind a firewall.

***Current limitation:*** Each wiim_proxy server can only control one wiim device at this time. 
Thus you would need one wiim_proxy server with a unique port number for each wiim device.
This limitation will be looked at in the future.

# How to install

(1) Examine and maybe edit the file Makefile. Pay attention to the settings at the top of the Makefile.
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

# List of commands

In the following list ***$ip*** is the name or ip address of the system where this
server is running and ***$port*** is its port number ("http-socket = :5050")

http://$ip:$port/media/play

http://$ip:$port/media/pause

http://$ip:$port/media/resume

http://$ip:$port/media/toggle

http://$ip:$port/media/stop

http://$ip:$port/media/prev

http://$ip:$port/media/next

http://$ip:$port/media/seekfow

http://$ip:$port/media/seekback

***$int*** volume values below must be between 0 and 100 inclusive
    
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

***wifi above also works with ethernet connected wiims**

http://$ip:$port/input/hdmi

http://$ip:$port/input/optical

http://$ip:$port/input/phono

http://$ip:$port/input/bluetooth

http://$ip:$port/input/next-input

http://$ip:$port/output/optical

http://$ip:$port/output/line-out

http://$ip:$port/output/coax

http://$ip:$port/output/headphone

http://$ip:$port/output/bluetooth

http://$ip:$port/output/dlna

***$int*** preset numbers below must be between 1 and 12 inclusive

http://$ip:$port/preset/$int

wiim_proxy is backwards compatible with the published Wiim API.

http://$ip:$port/httpapi.asp?command=$command

http://$ip:$port/command/$command
