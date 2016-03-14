# wrds #

Read SAS datasets remotely (from wrds-cloud) into a Pandas dataframe.

## Pre-Installation: ##

Note: **wrds** has **pandas** and **jaydebeapi** as dependencies. These will be installed alongside **wrds** in the event that they do not already exist in your environment.

### Mac OS X ###

Prior to installation, you may need to export the following variables for **pandas** to install successfully.
    
    export CFLAGS=-Qunused-arguments
    export CPPFLAGS=-Qunused-arguments

### Linux ###

Depending on your setup and distribution, you may need to install **g++** for **pandas** to install successfully.

If you encounter...

    x86_64-linux-gnu-gcc: error trying to exec 'cc1plus': execvp: No such file or directory
    error: Setup script exited with error: command 'x86_64-linux-gnu-gcc' failed with exit status 1

You can install **g++** on a Debian-based system with `apt-get install g++` to resolve this.

## Installation ##

    pip install wrds

### JDBC Driver Installation ###

You will also need to install the latest JDBC drivers as per the directions found [here](https://wrds-web.wharton.upenn.edu/wrds/support/Accessing%20and%20Manipulating%20the%20Data/_007R%20Programming/_001Using%20R%20with%20WRDS.cfm). They can be found in the "Preparing Your Environment - R Studio" section.

### Configuration File Setup ###

**wrds** expects there to be a config file in your local home directory named `.wrdsauthrc`

Its format is as follows:

    [credentials]
    username=<username>
    password=<SAS Password that has been run through PWENCODE>
    classpath=<set of paths to sas.core.jar and sas.intrnet.javatools.jar>

Once the JDBC drivers above have been installed, set classpath in the .wrdsauthrc file. 

Assume my local account is 'wrdsuser'.

Example:

    classpath=/Users/wrdsuser/WRDS_DRIVERS/sas.core.jar:/Users/wrdsuser/WRDS_DRIVERS/sas.intrnet.javatools.jar

