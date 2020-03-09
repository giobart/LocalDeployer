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
    'PROJECT_NAME':'My-awsome-project'
    'STARTUP_COMMAND':'python helloworld.py'
    'SET_AS_STARTUP_APPLICATION':True
    'ON_DEPLOY_REBOOT':True
}
```
Note that the mandatory part in the deployment descriptor is just the PROJECT_NAME 

Now on your development machine, from the root folder of the project type:

`localdeployer deploy`

All the local network available devices (where the server was installed) will be listed

```
$~ Availabe devices:
$~ 1) raspberrypigio2
$~ 2) raspberrypi5
$~ Type the device number where you wish to deploy
``` 

now just type the number of the device where you want to deploy your code and that's it. 

Have Fun!

## Server installing guide

### TODO

## Client installing guide

### TODO

## How to contribute

Fell free to open issues, improve the code quality, add and propose features or whatever you have in your mind. 

## Disclaimer

This is a development only tool, use this just to test locally your own application without having to configure complex toolchain. I suggest you to use proper tools for your production environment. 
