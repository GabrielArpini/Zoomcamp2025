## Introduction

This note contain all my anotations during the first module of the Data Engineering Zoomcamp 2025.

### Data Engineering
Data Engineering is a field characterized by the designing, building, and maintaining of systems that collect, aggregate, and store data in various formats, ensuring accessibility, reliability, and readiness for analysis.

### Introduction to Docker

([Source Video](https://www.youtube.com/watch?v=EYNwNlOrpr0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=4))

Docker is a platform that is used to develop and run applications in a container, which is a unit of software that packages up codes and lists all its dependecies for easy replicability. Every change made into a container does not change it afterwards.

([Reference](https://www.docker.com/resources/what-container/))

To learn more about docker we are going to reproduce the contet of te Source Video. The following image contains the data pipeline presented in the source video, which we will reproduce.

![image](images/data_pipeline.png)


For instance, we need to create a container with a postgresql instance running. For that, we will use the following code:

```bash
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:13
```

The -v stands for the folder which will store our database data, because, as said before, if a container is closed, it will return to the original state, with that option, -v, we are assigning a folder to store our data, so we don't lose it.

With our connection open, we can open a jupyter notebook to ingest our data inside the postgresql database. First, we import pandas to read the parquet file, as in:

```Jupyter Notebook
import pandas as pd
df = pd.read_parquet("yellow_tripdata_2021-01.parquet")
```

Then, we import sqlalchemy to create our connection inside our notebook:

```Jupyter Notebook
from sqlalchemy improt create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
engine.connect()
```

And then, we ingest the data inside our dataframe into engine:

```Jupyter Notebook
df.to_sql(name="yellow_taxi_data",con=engine, method='multi', chunksize=100000,if_exists='append',index=False)
```
