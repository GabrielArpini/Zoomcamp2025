# Answers for the week 4 homework

## Question 1

Answer: select * from myproject.raw_nyc_tripdata.ext_green_taxi

As we can see in the code, the `database` variable is set to a `DBT_BIGQUERY_PROJECT` variable or a default value `dtc_zoomcamp_2025`, the same to the `schema` variable, we have an export only to the first variable mentioned, so the output will be: 

select * from `myproject`.raw_nyc_tripdata.ext_green_taxi

Where raw_nyc_tripdata is the default value for `schema`
## Question 2

Answer: Update the WHERE clause to pickup_datetime >= CURRENT_DATE - INTERVAL '{{ var("days_back", env_var("DAYS_BACK", "30")) }}' DAY

Because, setting up in that order assures that the `WHERE` clause will accomplish said task 

## Question 3

Answer: dbt run --select models/staging/+

Because, it does not necessarily run the `fct_taxi_monthly_zone_revenue`. All the other options run all materialize the `fct_taxi_monthly_zone_revenue` by running everything or by running some things and it's dependencies.

## Question 4

1 - Setting a value for DBT_BIGQUERY_TARGET_DATASET env var is mandatory, or it'll fail to compile

`TRUE`, because it is used in either case, if it is not set the code will fail.

2 - Setting a value for DBT_BIGQUERY_STAGING_DATASET env var is mandatory, or it'll fail to compile

`FALSE`, the only mandatory env var is `DBT_BIGQUERY_TARGET_DATASET`, the `DBT_BIGQUERY_STAGING_DATASET` is only needed when it is the model type is not `core`, but if it is not present the env_var will set to the default `DBT_BIGQUERY_TARGET_DATASET`


3 - When using core, it materializes in the dataset defined in DBT_BIGQUERY_TARGET_DATASET

`TRUE`, because the if condition is met it will set the env_var to `DBT_BIGQUERY_TARGET_DATASET`

4 - When using stg, it materializes in the dataset defined in DBT_BIGQUERY_STAGING_DATASET, or defaults to DBT_BIGQUERY_TARGET_DATASET

`TRUE`, the first variable is the one that will be used if it exists, it it not exists the second one, the default, will be used.

5 - When using staging, it materializes in the dataset defined in DBT_BIGQUERY_STAGING_DATASET, or defaults to DBT_BIGQUERY_TARGET_DATASET

`TRUE`, same answer as the one above.


## Question 5

TODO, need more study, with videos provided it is hard, no time left.

## Question 6

TODO

## Question 7

TODO