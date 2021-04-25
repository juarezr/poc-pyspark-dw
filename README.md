
# Data Engineering POC

## Description

This proof of concept will explore concepts and tools in Data Engineering, and required knowledge in
Software development as well.

### Scope

This POC task is to build an automatic process to ingest data on an on-demand basis. The data represents trips taken by different vehicles, and include a city, a point of origin and a destination.

This [CSV file](trips.csv) gives a small sample of the data your solution will have to handle. We would like to have some visual reports of this data, but in order to do that, we need to explore the following features.

### Mandatory Features

- There must be an automated process to ingest and store the data.
- Trips with similar origin, destination, and time of day should be grouped together.
- Develop a way to obtain the weekly average number of trips for an area, defined by a bounding box (given by coordinates) or by a region.
- Develop a way to inform the user about the status of the data ingestion without using a polling solution.
- The solution should be scalable to 100 million entries. It is encouraged to simplify the data by a data model. Please add proof that the solution is scalable.
- Use a SQL database.

### Bonus features

- Containerize the solution.
- Sketch up how one would set up the application using any cloud provider (AWS, GoogleCloud, etc).

## Solution

### Components

For demonstration pourposes this POC will have this pieces that interact togheter:

1. Data Warehouse:
   A regular Postgresql SQL database simulating an OLAP colunar database like Amazon Redshift or even a Hadoop Data Lake.
2. Ingestion routine
   A PySpark batch program for simulating a ETL job or a Big Data process running on a Hadoop Cluster.
2. Report routine
   A Python batch program for simulating a BI visualization tool (Tableu, Microstrategy, PowerBI, Apache Superset) or a Data Lake query tool (like Hive, Presto, AWS Athena).

### Limitations

Because the objective of POC is just to be a demonstration, there are many shortcomings and limitations that are hardcoded by design for not making the project and the code complex and easy the understanding of the main functionality that I want to show.

Here is some of them:

- There is only full dataset ingestion.
  Although incremental ingestion is really common, it can be added later if a real pipeline require it. This can be the case in scenarious like importing daily trips or latest orders, etc...
- There is no clustering for data processing
  Using a Hadoop/BigData cluster for running the Spark processing could allow paralel processing of data on dozen of servers. Doing this would make the sofware setup complex and turn the local reproduction harder.
- The Data Warehouse ingestion is really simple.
  The Postgresql tables are designed following a really simple fact/dimension like in Star Scheme. Probably it works in Redshift with a few fixes.
- No GIS is used in the Data Warehouse schema.
  It would be possible to use a extension like PostGIS for querying trips in a bounding box.
- There is customizable parameters in reporting
  The parameters for querying and generating the report are hardcoded. You can improve later if needed.

## Testing

### Requirements

For developing or testing the POC/solution the following software was used:

1. Ubuntu 20.10 ( a similar distro or event Widows with WSL3 may work )
2. Git
3. [Docker](https://docs.docker.com/engine/install/ubuntu/)
4. Docker Compose

### Reproducing

For configuring the environment and executing the programs you must execute the following steps running commands in a terminal shell.

#### Set up the docker repository in your local machine

Follow [these instructions](https://docs.docker.com/engine/install/ubuntu/):

``` bash
$ sudo apt-get update
$ sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

#### Install docker engine in your local machine

``` bash
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
```

#### Install docker-compose in your local machine

Follow [these instructions](https://docs.docker.com/compose/install/#install-using-pip):

``` bash
$ sudo apt-get install python3-pip
$ pip install docker-compose
```

Alternatively you can follow [these instructions](https://docs.docker.com/compose/install/#install-compose-on-linux-systems):

``` bash
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.29.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose
```

#### Clone this git repository

``` bash
$ git clone git@github.com:juarezr/poc-pyspark-dw.git
```
#### Create the execution environment with docker-compose

``` bash
$ docker-compose build
$ docker-compose run --rm poc
```

This will open a shell inside the container:

``` bash
root@pyspark_env:/tmp#
```

Quit from this shell using command: `exit`.

#### Run the routines that simulate the Data Enginering / Big Data process

``` bash
$ python ingest.py # For ingesting the provided data in trips.csv
$ python report.py # For obtaining the result from the Database
```

#### Cleanup

Clean/Remove the containers with this command in another shell window:

``` bash
$ docker-compose down
$ docker image rm poc-pyspark-image
$ docker image rm poc-dw-image
```

Have fun!
