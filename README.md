# LocalDeployer
Deploy fast and easily your applications to the local development IoT infrastructure

## How it works
Install the server tool to all your RaspberryPi (& co), make sure to auto start the service on boot.
Install the client application on your development machine.

Now just put a Deployment Descriptor in the project root like in the following example:

File: ` DEPLOY-DESCRIPTOR.json `

Content:

```
{
    "PROJECT_NAME":"My-awsome-project"
    "STARTUP_COMMAND":"python helloworld.py"
    "SET_AS_STARTUP_APPLICATION":true
    "ON_DEPLOY_REBOOT":true
}
```
Note that the mandatory parts in the deployment descriptor are just the PROJECT_NAME and SET_AS_STARTUP_APPLICATION. <br>
You must set ON_DEPLOY_REBOOT and STARTUP_COMMAND only if SET_AS_STARTUP_APPLICATION is True


Run the client to perform the deploy with  
`python deploy.py -i <input-folder> -r <remote-id>`

The list of all the configured remote-id device can be listed with

```
$~ python deploy.py -l

####### Remote configured machines #######
  Remote Id  Hostname/IP
-----------  ---------------
          0  raspberrypigio2
``` 

The listed devices are the ones configured into the config.py file ìn the line

``` REMOTE_MACHINES = ["raspberrypigio2"] ```

Have Fun!

## Server installing guide

### TODO

## Client installing guide

### TODO

## How to contribute

Fell free to open issues, improve the code quality, add and propose features or whatever you have in your mind. 

## Disclaimer

This is a development only tool, use this just to test locally your own application without having to configure complex toolchain. I suggest you to use proper tools for your production environment. 
