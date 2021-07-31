# Malaysia COVID-19 Data Pipeline with Airflow

This is a simple data pipeline that performs an ETL (Extract, Transform, Load) process. The workflow includes obtaining Malaysian COVID-19 data from a public repository, selecting important data from different files, computing new statistics from it and storing the final data in a database. This process is an attempt to summarise the data and compute simple statistics that could help understand the data better.

This is more of a practice of using Airflow that would theoretically allow to automate this entire workflow on a scheduled basis, eg. daily when the data is updated.

## The Idea

1. Extract desired data from the public repository https://github.com/MoH-Malaysia/covid19-public
   - The data is in a .csv file which can be requested and read by pandas.
2. Get the important columns of data from different files. This would be:
   - The number of cases in a day from the cases file.
   - The total number of tests (rtk + pcr) in a day from the tests file.
3. Compute a new data column in the form of a case-to-test ratio.
4. Store this transformed data in a database that we could use for something else, eg. a dashboard.

With Airflow, the idea would be to schedule and automate this entire process.

## Setting up Airflow

This is where I found most difficulty in. It seems that Airflow doesn't run natively on Windows (which is the OS I use) and hence it was more complicated than usual to get it up and running. For this project, I settled with the usage of docker-compose which runs all the defined services through a few commands. The docker-compose file was obtained from https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml
(Note that this requires the installation of Docker and docker-compose)

To first initialise the Airflow instance which initialises the database and creates an admin user, use the following command:

```
docker-compose up airflow-init
```

To then start the required services specified in the docker-compose file, use the following command:

```
docker-compose up
```

At this stage, you should be able to see the web UI at `localhost:8080`

Finally, to stop the containers, run the following command:

```
docker-compose down
```

## The Implementation

1. I first used a Jupyter notebook `exploration.ipynb` to explore the data and identify the columns I wanted. I also used this to test the computation of the case-to-test ratio data that I wanted to have.
2. Once I had identified how I wanted the data to look like and the process required, I converted the steps into a function `extract_data()` in `covid_tasks.py`. This function exports the final data in the form of a .csv file.
3. The other function in `covid_tasks.py` is `load_to_database()` which establishes a connection to a MySQL database and stores the data in a table.
   - Note that at the moment, this inserts every single data in the csv file to the database and would hence not work the second time this is run. A better method would probably be to only add the new data to the database.
   - The function also works with local databases but when turned into a DAG, it is unable to establish a connection with the database.
4. With these functions set up, they are then imported into the `covid_data_dag.py` where the Directed Acyclic Graph (DAG) is set up for this simple workflow. The PythonOperator is used to execute these function.
   - Note that I believe this isn't the best file structure where both the tasks and the DAG file are in the same directory. However, for this purpose, it simplified the process of importing the functions.

- The final result of the database:

  ![image](https://user-images.githubusercontent.com/63803360/127737058-782e6302-fc87-47fa-8582-2af863ff2c45.png)

## References

1. More on Airflow.

   - https://airflow.apache.org/

2. Set up Airflow using docker-compose.

   - https://www.youtube.com/watch?v=aTaytcxy2Ck

3. Idea for this mini project.
   - https://python.plainenglish.io/simple-etl-with-airflow-372b0109549
