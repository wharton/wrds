# wrds #

Read SAS datasets remotely (from wrds-cloud) into a Pandas dataframe.

Pre-installation:

Mac OS X:

Prior to installation, you may need to export the following variables:
    
    export CFLAGS=-Qunused-arguments
    export CPPFLAGS=-Qunused-arguments

Once the wrds module has installed, you'll need to set up a config file in your home directory named `.wrdsauthrc`

Its format is as follows:

    [credentials]
    username=<username>
    password=<SAS Password that has been run through PWENCODE>
    classpath=<set of paths to sas.core.jar and sas.intrnet.javatools.jar>

You will also need to install the latest JDBC drivers as per the directions found here[https://wrds-web.wharton.upenn.edu/wrds/support/Accessing%20and%20Manipulating%20the%20Data/_007R%20Programming/_001Using%20R%20with%20WRDS.cfm]. They can be found in the "Preparing Your Environment - R Studio" section.

Once the JDBC drivers have been installed, set classpath in the .wrdsauthrc file. Assume my local account is called 'wrdsuser'.

Example:

    classpath=/Users/wrdsuser/WRDS_DRIVERS/sas.core.jar:/Users/wrdsuser/WRDS_DRIVERS/sas.intrnet.javatools.jar

