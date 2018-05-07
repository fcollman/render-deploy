# render-deploy
repo for docker-compose deployment of render stack

## purpose of this repo
The docker compose yaml file contains the configuration of a set of docker containers which together for a working render stack application on a server.  This repo represents the current state of deployment of that docker based render stack that is used at the Allen Institute in the Synapse Biology department, and as such there are some configuration settings which are particular to our setup, but the system is easily reconfigured to be deployed elsewhere, and perhaps we will move to a more standardized configuration model in the near future.

## stack design overview
This docker compose stack will launch a server which will offer a set of services available on different ports external to the stack.  Those ports include

8080,80: render web service
The duplication of ports is only for historical reasons when we were running different versions of render on different ports for testing purposes and I wanted to maintain backward compatibility.  Running on port 80 simplifies the URL calls for gaining entry to the render dashboard, as most non programming users will find that more convienent to access the server, but you can configure these as you see fit.

This docker compose file alters the configuration of the base render docker image to point to the mongo docker for its database configuration, and uses environment variables to configure the memory settings and the ndviz links.  For a complete list of render docker configurations see https://github.com/AllenInstitute/render/blob/master/docs/src/site/markdown/render-ws-docker.md#environment-variables.  One of particular note WEB_SERVICE_MAX_TILE_SPECS_TO_RENDER, controls how many images a particular render image request needs to involve before render will give up and just render green box outlines of the tiles.  If you are seeing green tiles and are unhappy about it, this would be the knob to twiddle.  

5000: vizrelay service
This is a lightweight redirect service that takes the short urls that render would prefer to construct and expands them out to full neuroglancer style json urls, and in the process adds some configurable default settings, such as that we would like additive blend mode turned on for all layers, and would would like to have the xy view be the default (to prevent neuroglancer/ndviz from loading 1000 z's at once, which render is not fast at).  The volume mounted file vizrelay_config.json contains the configuration of where this service redirects to and its configuration so you are free to alter it as you see fit. 

8001: ndviz webserver
This is the Node.js webserver that serves the neuroglancer powered ndviz visualization service.

In this example I have set all the configurations to work as localhost, but if you want this to operate as a true server to users elsewhere you shoudl replace those references in the docker_compose file and the vizrelay_config.json to reference the IP of the server you are running this one. 

## docker file dependancies
Presently this docker compose file refers to several docker images that must be accessible to the host system in order to run. 

There are some common was that most docker systems will automatically download from docker hub

mongo:3.4.2 - a mongo db docker image
fcollman/render - the docker image used for render nodes (this is continually built and reflects a recent AllenInstitute/render master branch)
neurodata/ndviz:beta - a docker image containing an ndviz server, maintained by neurodata
fcollman/vizrelay - my fork of a microservice written by Eric Perlman that lets us redirect and reconfigure neuroglancer links.

This also requires that you have docker installed and docker-compose installed with a recent version that supports the docker-compose 2.0 format.  If you build your own versions or branches of render or ndviz, you should either change this to point to your docker tag, or else use this tag.

## volume mount points
There are 2 different places mount points are specified and must be configured correctly for the systems you are running this on.

1) Mongodb data volume
(our default)
```
volumes:
    ./data:/data/db
```

you should change ./data to be the location where you wish to have mongo write its database tables.  This location will need high read/write availability.  Our server has this configured to be located on an NVMe SSD.  It might have been a better idea to do this with a docker data volume, I'm not certain.  Also there are potential issues with permissions, and you should make sure that docker can write to this location.

2) render web server mount points
```
    volumes:
        - ${PWD}:${PWD}
```
These define the locations that the render nodes can access data on the larger host.  Whatever filepaths are written into the render database, render needs to be able read that filepath from within the webservice inmo order for its image services to work properly.  I would reccomend keeping mirrored mount points so you don't get confused about where your data is locally, vs where render thinks it is inside the docker.  Render needs to be able to read the images if you want it to be able to do server side rendering (which is necessary for web based visualization).

Note however that this gives you the opportunity to easily port a render database to a new host where the data mount points have changed.  Say the mongo database has tilespecs where files are located at /nas/subfolder/subsubfolder/image00000.tif, and now you move the data to a new storage mount point, when some hardware is upgraded   /newstorage/olddata/subfolder/subfolder/image00000.tif.

You can avoid having to invalidate all of your tilespecs by simply adding a volume mount command of.
```
volumes:
    - /newstorage/olddata:/nas:ro
    - /newstorage/olddata:/newstorage/olddata:ro
```
now within the render docker, the data will be available at both the old mount point and the new mount point, so backward compatibility has been maintained.  Note we mount these as read because render has no need to write to these locations.

# render configuration
As mentioned above the render webservice is configure through environment variables. This stack is setup to work with webservice running on the same host, but you could most certainly configure them to point to neuroglancer/ndviz running somewhere else, or a mongo server that is maintained elsewhere. 

# starting service
export HOSTNAME=$HOSTNAME (or whatever dns entry is appropriate for your server)
docker-compose up

This will print out all the logging messages from each of the containers to the terminal.  Assuming the stack starts up correctly at this point. You should test that things are working correctly, upload some data, then stop the service with ctrl-c, or docker-compose down.  To spin it up in the background run
docker-compose up -d
.  Note, you can run docker-compose up -d infinitely number of times and it will restart any docker images which were killed off while leaving the components which are still running in place without duplication.

This is convienent in that if you a component appears to become non-responsive you can simply kill it using docker-compose kill NAMEOFSERVICE.

# getting started with render

You should take a look at the render documentation
https://github.com/saalfeldlab/render

and the render-python user guide
http://render-python.readthedocs.io/en/latest/guide/index.html
