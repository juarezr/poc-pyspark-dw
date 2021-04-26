
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

1. Data Storage:
   A regular Postgresql SQL database with PostGis extensions.
2. Ingestion routine
   A PySpark batch program simulating a ETL job or a Bulk insert routine.
2. Report routine
   A PySpark batch program for simulating a reporting tool or a frontend app.

### Limitations

Because the objective of POC is just to be a demonstration, there are many shortcomings and limitations that are hardcoded.

This is done by design for keeping the project and the code simple and easy to understand without compromizing the main functionality that is required to show.

Here is some of them:

- There is only full dataset ingestion.
  - Although incremental ingestion is really common, it can be added later if a real pipeline require it.
  - This can be the case in scenarious like importing daily trips or latest orders, etc...
- The file `trips.csv` is just copied inside the container.
  - Normally there is a remote storage and a network copy for handling that.
- All reports run with fixed parameters
  - The parameters for querying and generating the report are hardcoded. It can improved later if needed.
- User notification is a simple message after the data ingestion
  - This can be extended by using this hook to send a email, call a remote API, or register an event in a communication platform.
  - Of course this depends on the software ecosystem used for reaching the user.
- The deduplication of similar trips are just a report
  - Off course this can be improved by inserting it as step of the ingestion process.
  - Of course this depends on the software ecosystem used for reaching the user.
- The software setup won't scale to huge volumes of data
  - Doing it would make the sofware setup complex and turn the local reproduction harder.
  - However the architecture allows to grow the capacite by adding hardware/resources and improving the code for removing the limitations

### Scalability Proofs

The main bottlenecks that restrict scaling a solution like this are:

#### The time spent ingesting data into the database.

Inserting data row by row like a traditional application can be overkill when the volume of data is big.

The data must be ingested in batches, using the bulk insertion mecanisms that the database applications normally provides.

In this POC, we are using Apache Spark running in standaralone mode as ETL/Data transfer for handling this.
It allows fast read, processing, transformation, that scales from a local process running on one CPU Core to hundreds of multi-core servers in a cluster.

Alternatively is possible to use native tools for importing the data like:
- MSSQL bulk copy utility
- Redshift `COPY` command
- Bulk insert APIs

#### The delay for getting answer from the query

For this POC, the mandatory features require using support for geographic/spatial information for allowing location queries.

If one would use a regular OLTP database without GIS support for this tasks, it's possible that the end user could have slow response time for some queries.

In this POC, we are using Postgresql with PostGis extensions that allow creating GIST indexes for accelerating many times the query resolution.

#### Managing the database size

It is relatively common that spatial databases have a huge size.

This affects availability and costs because of the restritions of size and throuput that a database server have.
Normally a huge database makes harder to keep the regular routines like backup, replication, and replication.

In this POC, the PostGis database can be expanded migrating from the docker container to a larger on-promisses/cloud server.

If the application does not require too complex features for the spatial queries, this can be mitigated by using a database cluster like AWS Redshift, or using a Big Data query tool like Presto. This tools have some limited geographic/spatial features, but can scale horizontally to dozen of servers in a cluster.

### Deploying in the Cloud

A possible environment setup for the deploying a similar application in the AWS cloud is:

1. Database Server
    1. If there is the need for advanced spatial function to be used in the queries:
        1. Running Postgresql SQL database with PostGis extensions within a EC2 instance configuration. The setup and maintanance would be a responsability of the admin/develop.
    1. Otherwise:
        1. Running a AWS Redshift Cluster. In this case the maintenance is provided by AWS.
        2. Storing and querying a Data Lake stored inside AWS S3 using AWS Athena or Presto running inside a AWS EMR cluster. In this case, it's necessary to manually build the data lake and ingest data using Big Data tools.
2. Ingestion
    1. The source data can be collected and stored into the AWS S3 storage before processing and ingesting.
    2. The Spark ingestion routine developed in this POC could be adapted for running inside AWS EMR. This will allow huge processing throuput by the large scaling available.
    3. If importing to AWS Redshift, one could take advantage of AWS S3 again for importing the processed data.
    4. Instead of Spark there is some other alternatives:
        1. Using AWS Glue for ingesting into Redshift/Postgres
        1. Using AWS Kinesis Firehose for ingesting into AWS Redsfhit.
3. Orchestration
    1. Using Apache Airflow is a good alternative because it allows programatically control all the workflow by writing Python code.
    2. Alternatively one could use AWS Cloudwatch Rules combined with AWS Lambda and AWS Step Functions for triggering, and controlling the ingestion and ETL.

## Testing

### Requirements

For developing or testing the POC/solution the following software was used:

1. Ubuntu 20.10 ( a similar distro or event Widows with WSL3 may work )
2. Git
3. [Docker](https://docs.docker.com/engine/install/ubuntu/)
4. Docker Compose

### Software Setup

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

### Running / Reproducing

#### Create the execution environment with docker-compose

``` bash
$ docker-compose build
$ docker-compose run --name poc-etl  etl
```

This will open a shell inside the container:

``` bash
root@poc-pyspark:~#
```

Quit from this shell using command: `exit`.

#### Running routines inside container

Run the routines that simulate the Data Enginering process by executing the python program.
They have no paramaters and they present the result in console.

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

### Debugging

For developing/debugging:

1. Install Python 3 on computer
2. Add python to PATH environment variable
3. Install [vscode](https://code.visualstudio.com/docs/setup/setup-overview)
4. Install these extensions:
   1. VSCode Remote Development Extension Pack
      1. <kbd>Ctrl</kbd> > + <kbd>P</kbd> > `ext install ms-vscode-remote.vscode-remote-extensionpack`
   2. Python
      1. <kbd>Ctrl</kbd> > + <kbd>P</kbd> > `ext install ms-python.python`
4. Switch between local/remote mode in `vscode`:
   1. <kbd>F1</kbd> > `Remote-Containers: Open in Container`
   2. After this VSCode will open a remote folder inside the container
   3. You can now edit and debug the source code
   4. <kbd>F1</kbd> > `Remote-Containers: Reopen Locally` to return tho local repository
5. Debugging:
   1. Open and focus in a python file in VSCode
   2. Set breakpoints as needed
   3. Run/debug with <kbd>F5</kbd> >


Have fun!
