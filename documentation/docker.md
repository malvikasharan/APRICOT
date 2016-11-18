[![Latest Version](https://img.shields.io/pypi/v/bio-apricot.svg)](https://pypi.python.org/pypi/bio-apricot/)
[![License](https://img.shields.io/pypi/l/bio-apricot.svg)](https://pypi.python.org/pypi/bio-apricot/)
[![DOI](https://zenodo.org/badge/21283/malvikasharan/APRICOT.svg)](https://zenodo.org/badge/latestdoi/21283/malvikasharan/APRICOT)
[![](https://images.microbadger.com/badges/image/malvikasharan/apricot.svg)](https://microbadger.com/images/malvikasharan/apricot "Get your own image badge on microbadger.com")

![alt tag](https://github.com/malvikasharan/APRICOT/blob/master/APRICOT_logo.png)


####APRICOT Docker image

We recommend users to [install Docker software](https://docs.docker.com/engine/installation/) in their system to use the [docker images](https://hub.docker.com/r/malvikasharan/). 

In order to work with the Docker image for APRICOT, please follow these directions:

**1. Get Docker image**

  The image can be acquired by simply using this command:

  ```
  $ docker pull malvikasharan/apricot
  ```

**2. Create the Docker container for testing the software**
  
  ```
  $ docker run -it malvikasharan/apricot bash
  ```
  
  Here is a quick way to test if different modules work in your system (without really installing the complete filesystem).
  
  **Run the analysis in the `home` folder**
  
  ```
  $ cd home
  $ apricot -h
  ```
  
   **Run test/example analysis**
  
   The git repository contains a shell script [APRICOT/shell_scripts/run_example.sh](https://github.com/malvikasharan/APRICOT/blob/master/shell_scripts/run_example.sh) with shell commands that can be used for the demonstration of APRICOT installation including analysis with an example. 

  ```
  $ wget https://raw.githubusercontent.com/malvikasharan/APRICOT/master/shell_scripts/run_example.sh
  $ sh run_example.sh
  ```
  
  By default, this script generates a main analysis folder `APRICOT_analysis` and several sub-directories. To understand each components of the software and generated results, We recomend you to check out the [tutorial](https://github.com/malvikasharan/APRICOT/blob/master/documentation/APRICOT_tutorial.md).

**3. Get the supporting data required for running your queries**

  Users are required to establish a directory `source_files` containing all the [required supporting data](https://github.com/malvikasharan/APRICOT/blob/master/documentation/database_dependencies.md) (size: 14 GB compressed), which can be set-up using one of the two options:
  
  **option-1: ...in the local system - RECOMMENDED** 
  
  This should be set-up once in the local system (please exit the container using the command `exit` if already running it) and can be reused in different containers (shown in the point 4)
  
  This will ensure that users would not have to get the dataset every time a new Docker container for APRICOT is created. Moreover, this will keep the size of the container small by not having to install the large databases inside the container.
  
  **option-2: ...inside a new Docker conatiner**
  
  The supporting data can be used only inside the Docker container (every Docker container will need this set-up individually)
  
  **Commands to acquire the supporting data**
  
  ```
  $ wget http://data.imib-zinf.net/APRICOT-supporting_dataset.zip
  $ unzip APRICOT-supporting_dataset.zip
  ```
  
  Alternatively, these files can be installed/downloaded using the script docker_support.sh provided in the git repository of APRICOT.

  ```
  $ wget https://raw.githubusercontent.com/malvikasharan/APRICOT/master/shell_scripts/docker_support.sh
  $ sh docker_support.sh
  ```

**4. Using the supporting data from the local system (Recommended)**
    
  When the directory `source_files` is set-up in the local system, use the following command to mount the directory `source_file` into the Docker container (provide full path for $FULL_PATH_SOURCE_FILES):

  ```
  $ docker run -it -v /{$FULL_PATH_SOURCE_FILES}/source_files/:/home/source_files malvikasharan/apricot bash
  $ cd home
  ```
  
**5. Carry out analysis by APRICOT**
  ```
  $ wget https://raw.githubusercontent.com/malvikasharan/APRICOT/master/shell_scripts/run_example.sh
  $ sh run_example.sh
  ```
  For further details, please check the [Tutorial](https://github.com/malvikasharan/APRICOT/blob/master/documentation/APRICOT_tutorial.md) and [Tools and data dependencies](https://github.com/malvikasharan/APRICOT/blob/master/documentation/software_dependencies.md)

#### Docker image with all dependencies

To avoid the extra step for the installation of the databases locally (or inside the Docker container), an optional Docker image containing all dependencies can be used.

````
$ docker pull malvikasharan/apricot_with_dependencies
$ docker run -it malvikasharan/apricot_with_dependencies bash
$ cd home
$ cp APRICOT/shell_scripts/run_example.sh .
$ sh run_example.sh
````


