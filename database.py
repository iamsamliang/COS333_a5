#!/usr/bin/env python

from sqlite3 import connect
from sys import argv, stderr
from os import path
import database_handler


class Database():

    def __init__(self):
        self._connection = None

    def connect(self):
        DATABASE_NAME = 'reg.sqlite'
        if not path.isfile(DATABASE_NAME):
            print(f"{argv[0]}: database reg.sqlite not found", file=stderr)
            raise Exception(
                'A server error occurred. Please contact the system administrator.')
        try:
            self._connection = connect(DATABASE_NAME)
        except Exception as e:
            print(f'{argv[0]}: {e}', file=stderr)
            raise Exception(
                'A server error occurred. Please contact the system administrator.')

    def disconnect(self):
        try:
            self._connection.close()
        except Exception as e:
            print(f'{argv[0]}: {e}', file=stderr)
            raise Exception(
                'A server error occurred. Please contact the system administrator.')

    def search(self, form_args):
        try:
            cursor = self._connection.cursor()

            # form_args is a list that stores all the arguments needed for sql command
            # create appropriate sql command
            sql_command, arg_arr = database_handler.create_sql_command(
                form_args)
            # cursor.execute here
            cursor.execute(sql_command, arg_arr)

            rows = []
            row = cursor.fetchone()
            while row is not None:
                rows.append(row)
                row = cursor.fetchone()
            cursor.close()
            return rows
        except Exception as e:
            print(f'{argv[0]}: {e}', file=stderr)
            raise Exception(
                'A server error occurred. Please contact the system administrator.')

    def class_details(self, class_id):
        try:
            cursor = self._connection.cursor()

            sql_command1 = "SELECT classes.courseid, classes.days, classes.starttime, classes.endtime, classes.bldg, classes.roomnum, crosslistings.dept, crosslistings.coursenum, courses.area, courses.title, courses.descrip, courses.prereqs FROM classes, crosslistings, courses WHERE classes.courseid = courses.courseid AND crosslistings.courseid = courses.courseid AND classid=? ORDER BY dept ASC, coursenum ASC"

            # fetching professors if any
            sql_command2 = "SELECT profs.profname FROM coursesprofs, profs WHERE coursesprofs.courseid=? AND coursesprofs.profid=profs.profid ORDER BY profname"

            cursor.execute(sql_command1, [class_id])

            results = {}
            row = cursor.fetchone()

            # If reg.py sends a "class details" query specifying a classid that does not exist in the database, then regserver.py must write a descriptive error message to its stderr and continue executing.
            # if classid does not exist, return an empty dictionary
            if row is None:
                return results

            firstrow = row
            courseid = str(row[0])
            results['courseid'] = courseid
            results['days'] = str(row[1])
            results['start'] = str(row[2])
            results['end'] = str(row[3])
            results['building'] = str(row[4])
            results['room'] = str(row[5])

            dept_num_list = []
            dept_num_list.append(str(row[6]) + " " + str(row[7]))
            row = cursor.fetchone()
            while row is not None:
                dept_num_list.append(str(row[6]) + " " + str(row[7]))
                row = cursor.fetchone()

            results['dept_num'] = dept_num_list
            results['area'] = str(firstrow[8])
            results['title'] = str(firstrow[9])
            results['desc'] = str(firstrow[10])
            results['prereq'] = str(firstrow[11])

            cursor.execute(sql_command2, [courseid])

            professors = []
            row = cursor.fetchone()
            while row is not None:
                professors.append(str(row[0]))
                row = cursor.fetchone()
            results['profs'] = professors
            cursor.close()
            return results
        except Exception as e:
            print(f'{argv[0]}: {e}', file=stderr)
            raise Exception(
                'A server error occurred. Please contact the system administrator.')

# -----------------------------------------------------------------------

# For testing:


if __name__ == '__main__':
    database = Database()
    database.connect()
    books = database.search('Kernighan')
    for book in books:
        print(book)
    database.disconnect()
