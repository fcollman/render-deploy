# render-deploy
repo for docker-compose deployment of render stack.  This branch is for a multiple node deployment. 

## purpose of this repo
The docker compose yaml file contains the configuration of a set of docker containers which together for a working render stack application on a server.  This repo represents the current state of deployment of that docker based render stack that is used at the Allen Institute in the Synapse Biology department, and as such there are some configuration settings which are particular to our setup, but the system is easily reconfigured to be deployed elsewhere, and perhaps we will move to a more standardized configuration model in the near future.

## stack design overview
This docker compose stack will launch a server which will offer a set of services available on different ports external to the stack.  Those ports include

80,8080,8081,8082: render web service
The duplication of ports is only for historical reasons when we were running different versions of render on different ports for testing purposes and I wanted to maintain backward compatibility.  Running on port 80 simplifies the URL calls for gaining entry to the render dashboard, as most non programming users will find that more convienent to access the server, but you can configure these as you see fit.

This docker compose file alters the configuration of the base render docker image to point to the mongo docker for its database configuration, and to redirect all logging to stdout, so that it may be collected by logspout and sent to an ELK stack which we run seperately.  This isn't strictly necessary to be running.

8000,8001: ndviz webserver
This is the Node.js webserver that serves the neuroglancer powered ndviz visualization service.

## docker file dependancies
Presently this docker compose file refers to several docker images that must be accessible to the host system in order to run. 

There are some common was that most docker systems will automatically download from docker hub

mongo:3.4.2 - a mongo db docker image
ubuntu:16.04 - the base ubuntu docker image used for creating an nginx proxy load balancer

there are a few that are on docker hub, but we regularly are using docker images that are built internally and don't rely upon docker hub as these are systems we are modifying on a regular basis.

fcollman/render - the base docker image used to build multiple render nodes
fcollman/ndviz:latest - a docker image containing an ndviz server configured with the option of making requests to render for images

This also requires that you have docker installed and docker-compose installed with a recent version that supports the docker-compose 2.0 format.  If you build your own versions or branches of render or ndviz, you should either change this to point to your docker tag, or else use this tag.

## volume mount points
There are 2 different places mount points are specified and must be configured correctly for the systems you are running this on.

1) Mongodb data volume
(our default)
/mnt/SSD/mongodb:/data/db

you should change /mnt/SSD/mongodb to be the location where you wish to have mongo write its database tables.  This location will need high read/write availability.  Our server has this configured to be located on an NVMe SSD.  It might have been a better idea to do this with a docker data volume, I'm not certain.  Also there are potential issues with permissions, and you should make sure that docker can write to this location.

2) render web server mount points
(our default in common.yml)
volumes:
    - /nas:/nas:ro
    - /nas2:/nas2:ro
    - /nas3:/nas3:ro
    - /nas4:/nas4:ro

These define the locations that the render nodes can access data on the larger host.  Whatever filepaths are written into the render database, render needs to be able read that filepath from within the webservice inmo order for its image services to work properly.  We have mirrored the mountpoints of our data nas's on our host server within the docker image to simplify how this works.  

Note however that this gives you the opportunity to easily port a render database to a new host where the data mount points have changed.  Say the mongo database has tilespecs where files are located at /nas/subfolder/subsubfolder/image00000.tif, and now you move the data to a new storage mount point, when some hardware is upgraded   /newstorage/olddata/subfolder/subfolder/image00000.tif.

You can avoid having to invalidate all of your tilespecs by simply adding a volume mount command of.
volumes:
    - /newstorage/olddata:/nas:ro
    - /newstorage/olddata:/newstorage/olddata:ro

now within the render docker, the data will be available at both the old mount point and the new mount point, so backward compatibility has been maintained.  Note we mount these as read because render has no need to write to these locations.

# render configuration
The render subfolder contains a dockerfile which modifies the standard render docker to be configured properly for this stack.   This includes some convience functionality which rewrites URLs that point to the root of the render webservice to /render-ws/view/index.html, and autoappends the query parameter that configures the render dashboard to include links to the ndviz service running within this same stack.  

These could be modified easily to point to do the same thing for a catmaid webservice running within this docker stack, or on an existing server.  This simplifies the user interaction with the webservice.

This also configures the ndviz host links to default to the environment variable HOSTNAME.  So you should add export HOSTNAME=$HOSTNAME or export HOSTNAME=my.fullyqualified.dns.domain
whatever users of the service need to be able to type to gain access to the server spinning up the docker-compose stack.

Within the render/Dockerfile is where you can control how much RAM each render node will get made available.  

# starting service
First make sure that the host has access to all the docker images that you want to run
and that they are tagged according to tags referenced in your docker-compose.yml and common.yml files.

export HOSTNAME=$HOSTNAME (or whatever dns entry is appropriate for your server)
docker-compose up

This will print out all the logging messages from each of the containers to the terminal.  Assuming the stack starts up correctly at this point. You should test that things are working correctly, upload some data, then stop the service with ctrl-c, or docker-compose down.  To spin it up in the background run
docker-compose up -d
.  Note, you can run docker-compose up -d infinitely number of times and it will restart any docker images which were killed off while leaving the components which are still running in place without duplication.

This is convienent in that if you a component appears to become non-responsive you can simply kill it using docker-compose kill NAMEOFSERVICE.

the refresh_render.sh illustrates a simple script which stops and starts each of the render nodes one after the other, which is useful for dealing with render instances which have run into garbage collection problems and need to be restarted.

### testing
The test branch of this repo illustrates the use of this docker compose framework to spin up a complete testing environment of this stack, in which you have all the components built up from docker images of either the most current production versions of the code base, or a development version of a component which needs to be tested with the other production based elements of the system.  In such a case, the only need for mount points is to remap the locations where test results are going to run to the host filesystem to they can be analyzed.  Here the mongo mount point is removed, and data is written within the docker, and render doesn't have any mounts points.  When the testing stack is deleted, the database is removed and deleted as well.