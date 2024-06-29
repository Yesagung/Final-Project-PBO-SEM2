# siwp2005-final-project
## About This Project
In the context of UKRIDA's Portal System, which includes various sub-systems such as 
course management, student management, billing, calendar, bulletin, and scores student it is essential to 
develop  each  sub-system  as  independent  micro-services.

## whats in this project
This project consists of 9 endpoints whose goal it is to
- scores = Students can see the scores from each subject
- attendance = Students can see whether there is a lot of attendance or not
- bulletin = so that students know the latest information
- calendar = so that students can see the series of events
- billing = so students can pay and see the bill

### Quick start

- To start and build the development flask backend:
```
docker compose -f docker-compose.yaml up --build -d
```
Note: `docker compose` command is used in `Compose V2`. Supoosedly your version is `Compose V1` replace `docker compose` with `docker-compose`

After successful run the dev server, you will be able to see all containers are running 
```shell
docker ps
```
check specific container
```shell
docker ps --filter name="name of the container" 
```
- To stop service
```
docker compose -f docker-compose.yaml down
```
*specify `-v` to remove the mongodb volume*

- To remove all container
```
docker system prune
```

### Tech stack
- Flask
- MongoDB
- Docker  

References
* flask_mongoengine -> MongoDB connector ([docs](https://docs.mongoengine.org/# "docs"))
  * flask_jwt_extended -> JWT Token
- MongoDB ([docs](https://github.com/docker-library/docs/tree/master/mongo "docs"))

- Marshmallow -> Schema Validator ([docs](https://marshmallow.readthedocs.io/en/stable/index.html "docs"))
- Docker


### Debugging
Debug via docker logs
```shell
docker logs 'container name'
```

1. rebuild your development with:
```
docker compose -f docker-compose.yaml up --build -d
```
2. check your container name using:
``` shell
docker ps
```
3. try and debug your error from docker logs:
```shell
docker logs 'container name'
```


# Installation
## Install Dokcer and Docker Compose

## Ubuntu

## Windows
> if you are using windows, you can run the ubuntu image using your windows `WSL` subsystem
## WSL 2 with ubuntu Installation
### Enable wsl
- Open PowerShell as Administrator
- Enable WSL feature
    ```
      dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

    ```
- Enable Virtual Machine
    ```
    dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

    ```
    ![image](https://hackmd.io/_uploads/Hkps9rsV0.png)
- Restart your computer. 
> you need to restart your windows to see the effect whether you can run wsl on your windows
    
- Validate your wsl
    ```
    wsl --version
    ```
- ![image](https://hackmd.io/_uploads/HkL7oHiVC.png)
- set WSL 2 as default version
    ```
    wsl --set-default-version 2
    ```
![image](https://hackmd.io/_uploads/SyeviHsVR.png)


### Using Ubuntu on WSL 2

- check which linux distro are availables on your windows 
```
wsl --list --online
```
![image](https://hackmd.io/_uploads/SkS3aHs40.png)

- install ubuntu
```
wsl.exe --install -d <DistroName>
```
please change `<DistroName>` with the ubuntu distro list on your windows, we will use `Ubuntu-22.04`
`wsl.exe --install -d Ubuntu-22.04` then follow the instruction set ubuntu username and password

![image](https://hackmd.io/_uploads/ByBsy8iEA.png)
