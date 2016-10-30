[![Latest Version](https://img.shields.io/pypi/v/bio-apricot.svg)](https://pypi.python.org/pypi/bio-apricot/)
[![License](https://img.shields.io/pypi/l/bio-apricot.svg)](https://pypi.python.org/pypi/bio-apricot/)
[![DOI](https://zenodo.org/badge/21283/malvikasharan/APRICOT.svg)](https://zenodo.org/badge/latestdoi/21283/malvikasharan/APRICOT)
[![](https://images.microbadger.com/badges/image/malvikasharan/apricot.svg)](https://microbadger.com/images/malvikasharan/apricot "Get your own image badge on microbadger.com")

![alt tag](https://github.com/malvikasharan/APRICOT/blob/master/APRICOT_logo.png)

####APRICOT Docker image

We recommend users to use APRICOT [docker image](https://docs.docker.com/v1.8/userguide/dockerimages/) which comprises of all the tool dependencies and allows a frictionfree functionalities of the software.

Use the follwing command to pull th image toyour local system (the [docker](https://docs.docker.com/engine/installation/) must be installed):

````
$ docker pull malvikasharan/apricot
````

####Database requirements for the software

This docker image requires an additional step for fetching the databases required to run the software.

#####Run the container:
````
$ docker run -it malvikasharan/apricot bash
````
APRICOT is installed and can be called using command `apricot` and the libraries will be saved at `usr/local/lib/python3.5/site-packages/apricotlib/`

#####Go to the `home` folder to test the software:
````
$ cd home
````

####Docker with complete filsystem


