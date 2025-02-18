# Notes module_4 

## What is Analytics Engineering?
Provides a bridge between the data engineering and data analytics by providing a clean and reliable dataset for analysis, it is focused in the moving and transformation of data.

## Data Modeling Concepts

### ETL vs ELT

The main difference between ETL and ELT is that the ETL transforms data before loading it to a Data Warehouse, the ELT, otherwise, transforms the data after loading it inside a data warehouse. 

Because of the transformation before loading, the ETL is more stable and compliant to data analysis, even tho it requires more storage and compute cost, the ELT is faster and more flexible to data analysis with a lower cost and maintenance.

### Kimball's Dimensional Modeling

It prioritises user understandability and query performance over non redudant data.

#### Elements of Dimensional Modeling
<b>Facts tables<b> -> Are measurements, metrics or facts about a business.
<b>Dimensions tables<b> -> Corresponds to a business entity.

It's also known as star schema.

#### Architecture of Dimensional Modeling / Kitchen analogy

The ETL process can be comparated with a restaurant, there is a stage area where are the raw data, a place that is not meant to be exposed to everyone, just like where the ingredients of a restaurant are stored. After that, we need to process our raw data to data models, ensuring efficiency and standards, this stage corresponds to a kitchen from a restaurant and can only be done by the cookers. Lastly, the presentation area, which is the dinning hall, where we present our data to shareholders.

## What is dbt?

Is a transformation workflow that transforms the data into something usefull for analysis and business decision making process

### How dbt works?

It turns a table into a model. A table is sent to the modeling layer, which will make transformations to it and persist it back to data warehouse. Each model is a '.sql' file, SELECT statement, with no DDL or DML, and a file that dbt will compile and run.

