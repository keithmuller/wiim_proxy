# Summary

***wiim_proxy*** is a http proxy server that provides a http only control interface
to any wiim device that supports the offical http(s) interface.

wiim_proxy supports all the controls (except the power and voice command) found on the wiim remote
as well as many of the commands described in the offical wiim http(s) interface document.

***Example use case for this software***: Controlling a wiim device from a Sofabaton x1s.

On the sofabaton x1s, create a wifi virtual device to connect via http to a wiim_proxy server running on a raspberry pi.

See the file ***sofabaton x1s example.pdf***

***Implematition information***

My wiim_proxy test/development environment is as follows:

&nbsp; (a) Any server running a recent release of linux (most distributions) to host the wiim_proxy server process. This software was developed and tested on a raspberry pi4 (and pi5) running raspios (bookworm) 64-bit. wiim_proxy code  should be able to run on a windows or apple system, but the install process would clearly have to be changed.

&nbsp; (b) ***wiim_ultra*** connected to a wiim vibelink.

&nbsp; (c) systemd is used to start the wiim_proxy server process on the pi5/pi4 at boot time.

&nbsp; (d) uwsgi (alone) is used as the intended use case is an internal home network safely behind a firewall.

***Current limitation:*** Each wiim_proxy server can only control one wiim device at this time. 
Thus you would need one wiim_proxy server with a unique port number for each wiim device.
This limitation will be looked at in the future.

# How to install

(0) On the raspberry pi where wiim_proxy will run, install git (google git install) if needed. Then download this package using git in your home directory:

    git clone https://github.com/keithmuller/wiim_proxy.git

    cd wiim_proxy

(1) Examine and maybe edit the file Makefile. Pay attention to the settings at the top of the Makefile.
You should not need to change the values for the following:
    
&nbsp;DESTDIR SYSMD OWNER GROUP
    
&nbsp;Do not change the value for: FILES.

(2) Edit wiim_proxy.ini. Change the ip address (10.0.1.103) in the line "pyargv=10.0.1.103 0" 
    to the ip address of the wiim device you want to control. The 0 after the ip address is the debug level, 0 for production use.
    So for example if your wiim device is at 10.0.1.111 the line would be "pyargv=10.0.1.11 0"
  
(3) Run the follow to make sure the port number is not being used, this should have no match.:
        
        netstat -a | grep 5050
  
(4) Only If you got a return like:
        
&nbsp; tcp   0   0 0.0.0.0:5050    0.0.0.0:*       LISTEN  
        
Edit wiim_proxy.ini and change the port number (5050) in the line "http-socket = :5050" to a port that is not used.

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

(12) Test the proxy server. As an example, assume:

&nbsp; 10.0.1.158 is the ip where wiim_proxy is running

&nbsp; 5050 is the port number of wiim_proxy server

&nbsp; 10.0.1.103 is the ip address of the wiim device in the file wiim_proxy.ini

&nbsp; ***From any web browser (or use curl) connect to:***

    http://10.0.1.158:5050/input/line-in
   
&nbsp; You should get:

&nbsp; ok

&nbsp; as a return value.

***End of install process***

# Debugging

You can run wiim_proxy in debug mode with verbose enabled to make sure it is sending the expected commands to the wiim device.

Debugging is best done by running wiim_proxy directly from the command line so you can see each command being sent.

(1) If you have already installed wiim_proxy to /opt, stop the service from the downloaded wiim_proxy directory from github

    make service_stop

(2) Now run wiim_proxy directly from the command line in debug mode

    make test

(3) you will see something similar to the following output after the step above:

uwsgi --ini test.ini
<br>[uWSGI] getting INI configuration from test.ini
<br>*** Starting uWSGI 2.0.21-debian (64bit) on [Wed May  7 10:22:33 2025] ***
<br>compiled with version: 12.2.0 on 19 May 2023 13:59:29
<br>os: Linux-6.12.25+rpt-rpi-2712 #1 SMP PREEMPT Debian 1:6.12.25-1+rpt1 (2025-04-30)
<br>nodename: keithm-pi5
<br>machine: aarch64
<br>clock source: unix
<br>pcre jit disabled
<br>detected number of CPU cores: 4
<br>current working directory: /home/kmuller/wiim_proxy
<br>detected binary path: /usr/bin/uwsgi-core
<br>your processes number limit is 64577
<br>your memory page size is 16384 bytes
<br>detected max file descriptor number: 1024
<br>lock engine: pthread robust mutexes
<br>thunder lock: disabled (you can enable it with --thunder-lock)
<br>uwsgi socket 0 bound to TCP address :5050 fd 3
<br>Python version: 3.11.2 (main, Nov 30 2024, 21:22:50) [GCC 12.2.0]
<br>*** Python threads support is disabled. You can enable it with --enable-threads ***
<br>Python main interpreter initialized at 0x7fff72a1fee8
<br>your server socket listen backlog is limited to 100 connections
<br>your mercy for graceful operations on workers is 60 seconds
<br>mapped 145840 bytes (142 KB) for 1 cores
<br>*** Operational MODE: single process ***
<br>WSGI app 0 (mountpoint='') ready in 0 seconds on interpreter 0x7fff72a1fee8 pid: 20960 (default app)
<br>*** uWSGI is running in multiple interpreter mode ***
<br>spawned uWSGI master process (pid: 20960)
<br>spawned uWSGI worker 1 (pid: 20961, cores: 1)

(3) Now in another commad line window, browser, or from sofabaton, test a command. For example say you sent from another window 

    curl http://10.0.1.158:5050/vol/up

(4) In the command line window where wiim_proxy is running you should see (the volume number depends on the current colume level):

API command: getPlayerStatus
<br>API command: setPlayerCmd:vol:27

(5) If you get an error message (a badly formed url command) or no response then adjust the http commands in the sofabaton app for example.

# List of commands

***TODO:*** wiim does not yet support an http api for the wiim remote power button at this time. It is expected to be added sometime in the future.

In the following list of commands:

&nbsp; ***$ip*** is the network name or network ip address of the system where the wiim_proxy
server is running.

&nbsp; ***$port*** is the network port number ("http-socket = :5050")

http://$ip:$port/media/play
<br>http://$ip:$port/media/pause
<br>http://$ip:$port/media/resume
<br>http://$ip:$port/media/toggle
<br>http://$ip:$port/media/stop
<br>http://$ip:$port/media/prev
<br>http://$ip:$port/media/next
<br>http://$ip:$port/media/seekfow
<br>http://$ip:$port/media/seekback

**$int volume values below must be between 0 and 100 inclusive**
    
http://$ip:$port/vol/up
<br>http://$ip:$port/vol/up/$int
<br>http://$ip:$port/vol/down
<br>http://$ip:$port/vol/down/$int
<br>http://$ip:$port/vol/$int

http://$ip:$port/mute/on
<br>http://$ip:$port/mute/off
<br>http://$ip:$port/mute/toggle

**wifi command  also works with ethernet connected wiims**
<br>http://$ip:$port/input/wifi 
<br>http://$ip:$port/input/line-in
<br>http://$ip:$port/input/hdmi
<br>http://$ip:$port/input/optical
<br>http://$ip:$port/input/phono
<br>http://$ip:$port/input/bluetooth
<br>http://$ip:$port/input/next-input

http://$ip:$port/output/optical
<br>http://$ip:$port/output/line-out
<br>http://$ip:$port/output/coax
<br>http://$ip:$port/output/headphone
<br>http://$ip:$port/output/bluetooth
<br>http://$ip:$port/output/dlna

***$int*** preset numbers below must be between 1 and 12 inclusive

http://$ip:$port/preset/$int

wiim_proxy is backwards compatible with the published Wiim API.

http://$ip:$port/httpapi.asp?command=$command
<br>http://$ip:$port/command/$command
