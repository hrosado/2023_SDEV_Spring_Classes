'''
Create table
Validate that it doesn’t already exist
Delete the table
Insert a record
Get a single record
Insert a bunch of records
Look at the difference between:
Scan for records
Query for records

'''
import decimal
import json

import boto3
import subprocess

DYNAMODB_RESOURCE = boto3.resource('dynamodb')


def create_table():
    table = DYNAMODB_RESOURCE.create_table(
        TableName='Courses',
        KeySchema=[
            {
                'AttributeName': 'CourseID',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'Title',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'CourseID',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Title',
                'AttributeType': 'S'
            },
            # Sensors --attribute-definitions AttributeName=Sensor,AttributeType=S --key-schema AttributeName=Sensor,KeyType=HASH
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    print("Table status:", table.table_status)
    print(f"Table [{table.name}] created successfully!")
    run_bat_file()


def update_table():
    table = DYNAMODB_RESOURCE.Table('Courses')

    with open('c:/Users/hommy/Documents/Repos/SDEV_UMGC/SDEV_400_Sec_Pro_Cloud/Week_04_SDEV_400_Sec_Pro_Cloud/Week_04_SDEV_400_Sec_Pro_Cloud_Homework/courses.json') as json_file:
        Courses = json.load(json_file)

        for course in Courses:
            # print(course['CourseID'])
            courseid = course['Item':'CourseID']
            title = title['Title']
            subject = subject['Subject']

            print("Adding Course: ", courseid, title, subject)

            table.put_item(
                Item={
                    'courseID': courseid,
                    'title': title,
                    'subject': subject,
                }
            )

        # data = json_file.read()
        # datadict = json.loads(data)

        # table.put_item(Item=datadict)

        # courses = json.load(json_file, parse_float=decimal.Decimal)
        # for i in courses:
        #     courseID = int(i['CourseID'])
        #     title = title['Title']
        #     subject = subject['Subject']

        #     print("Adding course:", courseID, title)

        #     table.put_item(
        #         Item={
        #             'courseID': courseID,
        #             'title': title,
        #             'subject': subject,
        #         }
        #     )


def run_bat_file():
    subprocess.call([r'Homework_02.bat'])


def main_menu():
    """Provides user with a main-menu display."""
    user_selection = input("\n******************************************\n"
                           + "Please Enter the Subject:\n"
                           + "1. List all Buckets (L)\n"
                           + "2. Create an S3 Bucket (C)\n"
                           + "3. Delete an S3 Bucket (D)\n"
                           + "4. S3 Specific Actions - Submenu (S)\n"
                           + "5. Exit (Q)\n"
                           + "******************************************\n")

    if user_selection == '1':
        print("User selection: " + user_selection)
        # print_buckets()
    elif user_selection == '2':
        print("User selection: " + user_selection)
        # create_bucket()
    elif user_selection == '3':
        print("User selection: " + user_selection)
        # delete_bucket()
    elif user_selection == '4':
        print("User selection: " + user_selection)
        # sub_menu()
    elif user_selection == '5':
        print("User selection: " + user_selection)
        # exit_application()


# create_table()
update_table()
# run_bat_file()
