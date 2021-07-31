import mysql.connector
import pandas as pd
import numpy as np
from datetime import date
# from configparser import ConfigParser


def extract_data():
    case_data = pd.read_csv(
        "https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_malaysia.csv")
    test_data = pd.read_csv(
        "https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/tests_malaysia.csv")

    diff = len(test_data) - len(case_data)

    test_data = test_data.drop(test_data.index[:diff])
    test_data = test_data.reset_index()

    total_testing = test_data["pcr"] + test_data["rtk-ag"]
    total_cases = case_data["cases_new"]
    dates = test_data["date"]

    case_test_ratio = total_cases / total_testing
    case_test_ratio.round(2)

    frame = {"date": dates, "total_testing": total_testing,
             "total_cases": total_cases, "case_test_ratio": case_test_ratio}

    new_df = pd.DataFrame(frame)
    new_df.to_csv("covid_malaysia{}.csv".format(
        date.today().strftime("%Y%m%d")))


def load_to_database():

    # config = ConfigParser()
    # config.read("db_creds.cfg")

    db = mysql.connector.connect(
        # host=config.get("mysql-remote", "MYSQL_Host"),
        # user=config.get("mysql-remote", "MYSQL_User"),
        # password=config.get("mysql-remote", "MYSQL_Password"),
        # database=config.get("mysql-remote", "MYSQL_Database"),

        host="INSERT_HOST",
        user="INSERT_USER",
        password="INSERT_PASSWORD",
        database="INSERT_DB",
    )

    # The cursor is an object used to make a connection for executing SQL queries.
    cursor = db.cursor()

    with open("covid_malaysia{}.csv".format(date.today().strftime("%Y%m%d"))) as file:

        # Skip the header
        next(file)
        for line in file:
            line = line.replace("\n", "")
            values = line.split(",")[1:]

            # Note that this table name is not fixed and is dependent on current use.
            insert_query = """
                INSERT IGNORE INTO covid_data
                VALUES ('{}', '{}', '{}', '{}')
                """.format(
                values[0],
                values[1],
                values[2],
                values[3]
            )

            cursor.execute(insert_query)

    db.commit()
    cursor.close()
    db.close()
