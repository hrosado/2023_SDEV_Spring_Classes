Certainly! Here's an updated version of the Python application that creates the "Sensors" table with the specified attributes and populates it with at least 20 records, including a random attribute for each record:

python
Copy code
import boto3
import random

def create_table():
    dynamodb = boto3.client('dynamodb')
    table_name = 'Sensors'

    response = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'Sensor',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Sensor',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'SensorDescription',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'ImageFile',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'SampleRate',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'Location',
                'AttributeType': 'SS'
            },
            {
                'AttributeName': 'RandomAttribute',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    print(f'Table "{table_name}" created.')

def populate_table():
    dynamodb = boto3.resource('dynamodb')
    table_name = 'Sensors'
    table = dynamodb.Table(table_name)

    items = [
        {
            'Sensor': 'sensor1',
            'SensorDescription': 'Sensor 1 Description',
            'ImageFile': 'path/to/image1.jpg',
            'SampleRate': 2048,
            'Location': ['Aberdeen MD', 'Orlando FL'],
            'RandomAttribute': 'Random 1'
        },
        {
            'Sensor': 'sensor2',
            'SensorDescription': 'Sensor 2 Description',
            'ImageFile': 'path/to/image2.jpg',
            'SampleRate': 4096,
            'Location': ['Chicago IL', 'Seattle WA'],
            'RandomAttribute': 'Random 2'
        },
        # Add more items here
        # ...
    ]

    for i in range(18):
        item = {
            'Sensor': f'sensor{i + 3}',
            'SensorDescription': f'Sensor {i + 3} Description',
            'ImageFile': f'path/to/image{i + 3}.jpg',
            'SampleRate': random.choice([1024, 2048, 4096]),
            'Location': random.sample(['Aberdeen MD', 'Orlando FL', 'Chicago IL', 'Seattle WA'], random.randint(1, 4)),
            'RandomAttribute': f'Random {i + 3}'
        }
        items.append(item)

    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)

    print(f'{len(items)} records added to table "{table_name}".')

# Example usage
create_table()
populate_table()

'''
Make sure you have the boto3 library installed (pip install boto3) 
and have your AWS credentials properly configured. The application 
creates a table named "Sensors" with the specified attributes: 
Sensor (hash key), SensorDescription, ImageFile, SampleRate, 
Location, and RandomAttribute. The populate_table function generates 
additional records by randomly selecting attributes. You can modify 
the items list or customize the generation of random attributes as per your requirements.
'''

# Second part
import boto3

def create_table():
    dynamodb = boto3.client('dynamodb')
    table_name = 'Courses'

    response = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'CourseID',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'CourseID',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Subject',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'CatalogNbr',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Title',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'NumCredits',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    print(f'Table "{table_name}" created.')

def populate_table():
    dynamodb = boto3.resource('dynamodb')
    table_name = 'Courses'
    table = dynamodb.Table(table_name)

    items = [
        {
            'CourseID': '001',
            'Subject': 'SDEV',
            'CatalogNbr': '400',
            'Title': 'Secure Programming in the Cloud',
            'NumCredits': 3
        },
        # Add more items here
        # ...
    ]

    for i in range(1, 10):
        item = {
            'CourseID': f'00{i + 1}',
            'Subject': f'SUB{i + 1}',
            'CatalogNbr': f'CAT{i + 1}',
            'Title': f'Title {i + 1}',
            'NumCredits': i + 1
        }
        items.append(item)

    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)

    print(f'{len(items)} records added to table "{table_name}".')

def search_title():
    dynamodb = boto3.resource('dynamodb')
    table_name = 'Courses'
    table = dynamodb.Table(table_name)

    while True:
        subject = input('Enter the subject (e.g. SDEV): ')
        catalog_nbr = input('Enter the catalog number (e.g. 400): ')

        if not subject or not catalog_nbr:
            print('Both subject and catalog number are required. Please try again.')
            continue

        response = table.scan(
            FilterExpression='Subject = :subject and CatalogNbr = :catalog_nbr',
            ExpressionAttributeValues={
                ':subject': subject,
                ':catalog_nbr': catalog_nbr
            }
        )

        if response['Items']:
            for item in response['Items']:
                print(f'Title: {item["Title"]}')
        else:
            print('No matching course found.')

        choice = input('Do you want to search again? (y/n): ')
        if choice.lower() != 'y':
            break

# Example usage
create_table()
populate_table()
search_title()

# End Second part
'''
Make sure you have the boto3 library installed 
(pip install boto3) and have your AWS credentials properly configured. 
The application creates a table named "Courses" with the specified attributes: 
CourseID (hash key), Subject, CatalogNbr, Title, and NumCredits. 
The populate_table function generates additional course items. 
The search_title function prompts the user to enter a subject 
and catalog number and searches for the corresponding title 
in the "Courses" table. It continues to loop until the user 
requests to exit or if the subject and catalog number are not entered. 
You can modify the items list or customize the search functionality 
as per your requirements.
'''


# 3 Section
# To delete all DynamoDB tables created for this exercise using the AWS CLI, you can follow the steps below:

# 1. Open the AWS CLI or AWS CloudShell.
# 2. Run the following command to list all DynamoDB tables:

#    ```bash
   aws dynamodb list-tables
#    ```

#    This command will return a list of all the DynamoDB tables in your AWS account.

# 3. Identify the tables that were created for this exercise. In this case, it is the "Courses" table.

# 4. Run the following command to delete each table:

#    ```bash
   aws dynamodb delete-table --table-name <table-name>
#    ```

#    Replace `<table-name>` with the name of the table you want to delete. In this case, it is the "Courses" table.

# 5. Repeat the above command for each table that needs to be deleted.

# 6. After executing the delete-table command for each table, you should receive responses similar to the following:

#    ```
   {
       "TableDescription": {
           "TableName": "<table-name>",
           "TableStatus": "DELETING",
           ...
       }
   }
#    ```

#    This response indicates that the table deletion process has been initiated.

# 7. Wait for a few moments until the tables are deleted. You can check the status of the tables by running the `list-tables` command again.

# 8. Once the tables are deleted, you should receive a response similar to the following when running the `list-tables` command:

#    ```
   {
       "TableNames": []
   }
#    ```

#    This response indicates that there are no DynamoDB tables present in your AWS account.

# By following these steps and executing the appropriate AWS CLI commands, you will be able to successfully delete 
# the DynamoDB tables created for this exercise.