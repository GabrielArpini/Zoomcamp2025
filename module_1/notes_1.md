## Introduction

This note contains all my annotations during the first module of the Data Engineering Zoomcamp 2025.

### Data Engineering
Data Engineering is a field characterized by designing, building, and maintaining systems that collect, aggregate, and store data in various formats, ensuring accessibility, reliability, and readiness for analysis.

### Introduction to Docker

([Source Video](https://www.youtube.com/watch?v=EYNwNlOrpr0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=4))

Docker is a platform used to develop and run applications in a container, which is a unit of software that packages up code and lists all its dependencies for easy replicability. Every change made to a container does not persist after it is closed unless a volume is specified, a volume will bind a directory inside the host machine to a directory in a container ensuring data persistance.

([Reference](https://www.docker.com/resources/what-container/))

To learn more about Docker, we are going to reproduce the content of the source video. The following image contains the data pipeline presented in the source video, which we will reproduce:

![image](./images/data_pipeline.png)


For instance, we need to create a container with a PostgreSQL instance running. For that, we will use the following code:

```bash
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:13
```

The `-v` flag specifies the folder that will store our database data because, as stated before, if a container is closed, it will return to its original state. With the `-v` option, we are assigning a folder to store our data, so we don't lose it.

### Ingesting
With our connection open, we can open a Jupyter Notebook to ingest our data into the PostgreSQL database. First, we import pandas to read the parquet file, as shown below:

```Jupyter Notebook
import pandas as pd
df = pd.read_parquet("yellow_tripdata_2021-01.parquet")
```

Then, we import SQLAlchemy to create our connection inside the notebook:

```Jupyter Notebook
from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
engine.connect()
```

Next, we ingest the data from our DataFrame into the database:

```Jupyter Notebook
df.to_sql(name="yellow_taxi_data",con=engine, method='multi', chunksize=100000,if_exists='append',index=False)
```
With the code above, the `to_sql` function is very slow as it creates an `INSERT` command for each row. By using the `method='multi'` option, it batches rows into a single `INSERT` query. The `chunksize` parameter is important because some languages have a parameter limit. I’m not sure about PostgreSQL's limits, but implementing this method was a valuable learning experience.
([Source](https://stackoverflow.com/questions/29706278/python-pandas-to-sql-with-sqlalchemy-how-to-speed-up-exporting-to-ms-sql))

I've encountered some issues during my implementation, but with some dependencies in the `requirements.txt`, I managed to resolve them.

### PGCli

PGCli is a way to interact with a PostgreSQL database via a terminal. It can be used to get a quick view of the database content. The following command is an example showing how to use PGCli to connect to our database:

´´´Bash

pgcli -h localhost -p 5432 -u root -d ny_taxi


### PGAdmin

Pgcli is not a convenient way for data exploration and querying,the PGAdmin is a tool used to interact with PostgreSQL databases via a GUI in a more convinient and intuitive way.

To create a PGAdmin instance via docker, it's needed the following command

```bash
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    dpage/pgadmin4
```
But there is a problem, we cannot connect our database into the PGAdmin, because they are separated containers and are not in the same network. To solve that we need to create a network with:

```bash
docker network create pg-network
```
And then, insert the network configurations in the docker command to create the instance of the database and PGAdmin:

```bash
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name=pg-database \
    postgres:13
```
```bash
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name=pgadmin \
    dpage/pgadmin4
```

The `pg-network` is the network that we created previously, notice that it appear in both docker commands, the `name` of the database is used to connect inside the pgadmin GUI.


### Docker-Compose

Docker-Compose is a tool to create and run multiple containers with a single `.yaml` configuration file, you can start all your container stack with a single command, making it easier to manage your environment.

To get started with docker-compose, firstly you need to create a `docker-compose.yaml` file with:

```bash
code docker-compose.yaml
```
Then, inside the newly created `docker-compose.yaml` we can specify every service we want to run, as in:
```yaml
services:
  pgdatabase:
    image: postgres:13
    environment:
      - POSTGRES_USER=root 
      - POSTGRES_PASSWORD=root
      - POSTGRES_DB=ny_taxi
    volumes:
      - "./ny_taxi_postgres_data:/var/lib/postgresql/data:rw"
    ports:
      - "5432:5432"  
    
  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    ports:
      - "8080:80"
```
Notice that every container we want to run is inside the `services` tag. First, we specify the name that will be used (e.g `pgdatabase`), then the container image we want to use, the environment, which can be the credentials, database name, etc, volumes, if we want to keep data even if we stop docker-compose, and the ports to use on our host machine and inside the container.

After specifying and configuring our `docker-compose.yaml` we can simply start it by running:
```bash
docker-compose up -d
```
The `-d` tag means detached mode, in other words, all the containers will run in background mode and will not stuck your terminal.

If we don't specify a network inside the docker-compose.yaml it will automatically define one for you, to check the network you can run the following command:

```bash
docker network ls
```


