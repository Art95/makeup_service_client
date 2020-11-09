# Makeup Service Client
Client side for [service](https://github.com/Art95/makeup_service/) that allows user apply some makeup effects over video or picture with human face.

## Requirements
* Ubuntu 18.04 or higher
* Python 3.6 or higher
* Docker

## Running application
__Note__: if both server and client are running on the same machine,
please, plug in charger for laptops and expect some delays in stream.

Approach using docker is described below. Using virtual environments is also possible
but it demands OpenCV to be built from sources and passed to venv. 

1. Make sure that server part is running. Follow instructions [here](https://github.com/Art95/makeup_service/)
2. [Optional] If docker is not installed go to [installation guide](https://docs.docker.com/engine/install/ubuntu/)
3. [Optional] You can configure your system to avoid running *sudo* for docker commands [link](https://docs.docker.com/engine/install/linux-postinstall/)
4. Pull docker (alternatively, you can build image yourself by following __Note__ section below)
```
    sudo docker pull abaraniuk/makeup_service:client
```
5. Go to folder where you want code to be cloned to
6. Clone project's code 
```
    git clone https://github.com/Art95/makeup_service_client.git
    cd makeup_service_client
```
7. Allow docker to show windows by running
```
    xhost +local:
```
8. To start docker run
```
    sudo ./start.sh
```
9. To stop service run Ctrl+C and then
```
    sudo ./clean.sh
```
__Note__: to build docker go to project's directory and run:
```
    sudo docker build -t <NAME-FOR-IMAGE> .
```

__Note__: you can look into start.sh and execute docker commands with needed parameters yourself.
Supported parameters are:
* --host (string, ip or name address which client should run on)
* --port (integer with port number which client should run on)
* --debug (boolean (True/False) which mode client should use, debug or release)
* --server_host (string, ip or name address which server is running on)
* --server_port (integer with port number which server is running on)
* --hair-color (3 integer space separated values for b,g,r values of color code)
* --upper-lip-color (same as above)
* --lower-lip-color (same as above)
* --fps (integer, how many frames per second should client use)
* --flip-image (supported values True or False; sets if input images should be flipped)

## How it works
It will use webcam to pass images to server side and then apply simple makeup effects.
See [original project](https://github.com/zllrunning/face-makeup.PyTorch) for more information and examples.