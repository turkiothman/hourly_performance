"""
    PYTHON APP(/SCRIPT) TO CALCULATE PERFORMANCES HOURLY AND STORE DATA IN
    MYSQL DATABASE
"""


from datetime import datetime
from mysql.connector import connect, Error


now = datetime.now()
curDay = now.strftime("%d/%m/%Y")
curTime = now.strftime("%H:%M:%S")
# print(curDay, curTime)


def main():
    """ MAIN FUNCTION: FOR LOCAL SCOPING """

    try:
        with connect(
            host="localhost",
            user="root",
            password="",
            database="isa",
        ) as connection:
            print("Connection to DB succeeded!")

            select_query = """
                SELECT
                    registration_number,
                    Firstname,
                    Lastname,
                    ROUND(SUM((quantity * tps_ope_uni)) / 60, 2) AS performance
                FROM `pack_operation`
                WHERE
                    registration_number IS NOT NULL
                    AND cur_day = DATE_FORMAT(CURDATE(), '%d/%m/%Y')
                    AND cur_time > SUBTIME(CURRENT_TIME(), 010000)
                GROUP BY registration_number
            """

            insert_query = """
                INSERT INTO performance_per_hour
                (registration_number, first_name,
                 last_name, performance, cur_day, cur_time)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            with connection.cursor() as cursor:

                cursor.execute(select_query)
                results = cursor.fetchall()

                if len(results) > 1:
                    insert_records = [
                        (result[0], result[1], result[2],
                         result[3], curDay, curTime,)
                        for result in results
                    ]
                    cursor.executemany(insert_query, insert_records)
                    connection.commit()

    except Error as err_msg:
        print(err_msg)


if __name__ == '__main__':
    main()