## Introduction

This note contains all my annotations during the first module of the Data Engineering Zoomcamp 2025.

### Data Engineering
Data Engineering is a field characterized by designing, building, and maintaining systems that collect, aggregate, and store data in various formats, ensuring accessibility, reliability, and readiness for analysis.

### Introduction to Docker

([Source Video](https://www.youtube.com/watch?v=EYNwNlOrpr0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=4))

Docker is a platform used to develop and run applications in a container, which is a unit of software that packages up code and lists all its dependencies for easy replicability. Every change made to a container does not persist after it is closed.

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

I've encountered some issues during my implementation, but with adjustments to the `requirements.txt` dependencies, I managed to resolve them.

### PGAdmin

Pgcli is not a convinient way for data exploration and querying,the PGAdmin is a tool used to interact with PostgreSQL databases via a GUI in a more convinient and intuitive way.

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
