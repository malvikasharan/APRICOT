[![Latest Version](https://img.shields.io/pypi/v/bio-apricot.svg)](https://pypi.python.org/pypi/bio-apricot/)
[![License](https://img.shields.io/pypi/l/bio-apricot.svg)](https://pypi.python.org/pypi/bio-apricot/)
[![DOI](https://zenodo.org/badge/21283/malvikasharan/APRICOT.svg)](https://zenodo.org/badge/latestdoi/21283/malvikasharan/APRICOT)
[![](https://images.microbadger.com/badges/image/malvikasharan/apricot.svg)](https://microbadger.com/images/malvikasharan/apricot "Get your own image badge on microbadger.com")

![alt tag](https://github.com/malvikasharan/APRICOT/blob/master/APRICOT_logo.png)

#### APRICOT Docker image

We recommend users to use APRICOT [Docker image](https://docs.docker.com/v1.8/userguide/dockerimages/) which comprises of all the tool dependencies and allows a frictionfree functionalities of the software.

Use the follwing command to pull th image toyour local system (the [Docker](https://docs.docker.com/engine/installation/) must be installed):

````
$ docker pull malvikasharan/apricot
````

##### Run the container:
````
$ docker run -it malvikasharan/apricot bash
````

APRICOT is installed and can be called using command `apricot` and the libraries will be saved at `/usr/local/lib/python3.5/site-packages/apricotlib/`


##### Go to the `home` folder to test the software:

````
$ cd home
$ apricot
````

Try a test run:

````
$ cp APRICOT/shell_scripts/run_example.sh .
$ sh run_example.sh
````

#### Database requirements for the software

An additional step is needed to fetch the supporting data in order to carry out analysis of your queries

  Users are required to establish a directory `source_files` containing all the [required files](https://github.com/malvikasharan/APRICOT/blob/master/documentation/database_dependencies.md), which can be set-up as shown below inside the docker container (in the `home` folder) or in the local system (in that case exit the Docker container by `exit`):

  ```
  $ wget https://data.imib-zinf.net/APRICOT-supporting_dataset.zip --no-check-certificate
  $ unzip APRICOT-supporting_dataset.zip
  ```

  Alternatively, these files can be installed/downloaded using the script docker_support.sh provided in the git repository of APRICOT.

  ```
  $ wget https://raw.githubusercontent.com/malvikasharan/APRICOT/master/shell_scripts/docker_support.sh
  $ sh docker_support.sh
  ```

When the data directory is set-up inside the Docker container (in the home folder), APRICOT can be simply run to carry out analysis.

When the script is used to create a local dataset, use th following command to mount the directory `source_file` into the Docker container:

```
$ docker run -it -v /$FULL_PWD/source_files/:/home/source_files malvikasharan/apricot bash
$ cd home
$ cp APRICOT/shell_scripts/run_example.sh .
$ sh run_example.sh
```

This will ensure that users would not have to get the dataset every time a new Docker container for APRICOT is created. Moreover, this will keep the size of the container small by not having to install the large databases inside the container.

#### Docker image with all dependencies

To avoid the extra step for the installation of the databases locally (or inside the Docker container), an optional Docker image containing all dependencies can be used.

````
$ docker pull malvikasharan/apricot_with_dependencies
$ docker run -it malvikasharan/apricot_with_dependencies bash
$ cd home
$ cp APRICOT/shell_scripts/run_example.sh .
$ sh run_example.sh
````


