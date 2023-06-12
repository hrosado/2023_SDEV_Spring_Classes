"""
__filename__ = "aws_s3menu.py"
__course__ = "SDEV 400 6380 Secure Programming in the Cloud (2235)"
__author__ = "Hommy Rosado"
__copyright__ = "None"
__credits__ = ["Hommy Rosado"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Hommy Rosado"
__email__ = "hrosado4@student.umgc.edu"
__status__ = "Week 02 | Homework 01 | 5-30-2023"
"""

import io
import datetime
import random
import sys
import logging
import boto3
from botocore.exceptions import ClientError


# def add_items_buckets(file_name, bucket_name, object_name=None):
def add_items_buckets():
    """Exercise add_items_buckets()"""
    s3_client = boto3.resource('s3')

    for bucket in s3_client.buckets.all():
        print(bucket.name)

    bucket_name = input("Please select from the above listed Buckets.\n"
                        + "Bucket name: \n")
    while True:
        try:
            # Upload a new file
            data = open('data/testfile_01.txt', 'rb')
            response = s3_client.Bucket(bucket_name).put_object(
                Key='testfile_01.txt', Body=data)

            if response:
                logging.info('File was uploaded')
                print("File upload was successful.")
                sub_menu()
        except ClientError as error:
            logging.error(error)
            return False
        return True
    # sub_menu()


def delete_items_buckets():
    """Exercise delete_items_buckets()"""
    # Create an S3 client
    s3_client = boto3.client('s3')

    # Call S3 to list current buckets
    response = s3_client.list_buckets()

    # Get a list of all bucket names from the response
    buckets = [bucket['Name'] for bucket in response['Buckets']]

    for bucket in buckets:
        print(bucket)

    bucket_name = 'edu.umuc.sdev400.hommyrosado.photos'
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        # Retrieve the bucket's objects
        objects = response['Contents']
        if objects is not None:
            # List the object names
            logging.info(f'Objects in {bucket_name}')
            for obj in objects:
                logging.info(f'  {obj["Key"]}')
                print(f'  {obj["Key"]}')
            object_name = input("Please select an Object from above.\n"
                                + "Full object pathname: \n")

            try:
                s3_client.delete_object(Bucket=bucket_name, Key=object_name)
                logging.info('File was deleted')
                print("\nFile deletion was successful.")
                sub_menu()
            except ClientError as error:
                logging.error(error)
                return False
            return True

    except ClientError as error:
        # AllAccessDisabled error == bucket not found
        logging.error(error)
        return None
    return response['Contents']


def copy_items_buckets():
    """Exercise copy_items_buckets()"""
    # Create an S3 client
    s3_client = boto3.client('s3')

    # Call S3 to list current buckets
    response = s3_client.list_buckets()

    # Get a list of all bucket names from the response
    buckets = [bucket['Name'] for bucket in response['Buckets']]

    for bucket in buckets:
        print(bucket)

    print("Please select from the above listed Buckets.\n")
    # bucket_name = 'edu.umuc.sdev400.hommyrosado.photos'
    # Assign these values before running the program
    source_bucket_name = input("Please enter source Bucket name: \n")
    response = s3_client.list_objects_v2(Bucket=source_bucket_name)
    # Retrieve the bucket's objects
    objects = response['Contents']
    if objects is not None:
        # List the object names
        logging.info(f'Objects in {source_bucket_name}')
        for obj in objects:
            logging.info(f'  {obj["Key"]}')
            print(f'  {obj["Key"]}')
        source_object_name = input("Please select an Object from above.\n"
                                   + "Full object pathname: \n")

    for bucket in buckets:
        print(bucket)

    destination_bucket_name = input("Please enter destination Bucket name: \n")
    destination_object_name = source_object_name

    # Construct source bucket/object parameter
    try:
        s3_resource = boto3.resource('s3')
        s3_resource.Object(destination_bucket_name, destination_object_name).copy_from(
            CopySource=f'{source_bucket_name}/{source_object_name}'
        )
        print('Object copied!')
    except ClientError as error:
        logging.error(error)
        print(error)
        return False


def download_items_buckets():
    """Exercise download_items_buckets()"""
    # Create an S3 client
    s3_client = boto3.client('s3')
    s3_resource = boto3.resource('s3')

    # Call S3 to list current buckets
    response = s3_client.list_buckets()

    # Get a list of all bucket names from the response
    buckets = [bucket['Name'] for bucket in response['Buckets']]

    for bucket in buckets:
        print(bucket)

    bucket_name = 'edu.umuc.sdev400.hommyrosado.photos'
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        # Retrieve the bucket's objects
        objects = response['Contents']
        if objects is not None:
            # List the object names
            logging.info(f'Objects in {bucket_name}')
            for obj in objects:
                logging.info(f'  {obj["Key"]}')
                print(f'  {obj["Key"]}')
            object_name = input("Please select an Object from above.\n"
                                + "Full object pathname: \n")
            try:
                s3_object = s3_resource.Object(bucket_name, object_name)
                with io.BytesIO() as file:
                    s3_object.download_fileobj(file)
                    file.seek(0)
                    print(f'Downloaded content:\n{file.read()}')
                # s3_client.delete_object(Bucket=bucket_name, Key=object_name)
                logging.info('File was downloaded')
                print("\nFile download was successful.")
                sub_menu()
            except ClientError as error:
                logging.error(error)
                return False
            return True

    except ClientError as error:
        # AllAccessDisabled error == bucket not found
        logging.error(error)
        return None
    return response['Contents']


def create_bucket():
    """Create a bucket."""
    # Allow the user an option to exit
    user_choice = input("\nWould you like to Create an S3 Bucket? Y/N\n")
    if len(user_choice) != 1:
        print("Please try again.")
        create_bucket()
    elif user_choice.lower() == 'n':
        main_menu()
    elif user_choice.lower() != 'n' and user_choice.lower() != 'y':
        print("Please try again.")
        create_bucket()
    # else user_choice.lower() == 'y':
    else:
        # if len(user_choice) == 1:
        print(
            f'\nYour single character input was: {user_choice.upper()} \n')
        if user_choice.upper() == 'N':
            print("You will be returned to the Main Menu. ...")
            main_menu()
        elif user_choice.upper() != 'Y':
            print("\nYou entered an invalid character.\n")
            create_bucket()
        else:
            # Request parameters for the S3 Bucket
            print("Please follow the prompts: \n")
            # Need to test inputs
            first_name = input("Please provide the firstname: \n")
            first_name = first_name.lower()
            # Need to test inputs
            last_name = input("Please provide the lastname: \n")
            last_name = last_name.lower()
            # Create random six numbers
            numran = random.random()
            numran = str(numran)
            numrangen = str(numran[2:8])

            bucket_name = "edu.umuc.sdev400." + first_name + last_name + "-" \
                          + numrangen
            # Create an S3 client
            # Below code is from AWS
            try:
                s3_client = boto3.client('s3')
                s3_client.create_bucket(Bucket=bucket_name)
            except ClientError as error:
                logging.error(error)
                return False
            print(f"S3 Bucket name is:  {bucket_name} \n")
            print_buckets()


def delete_bucket():
    """Delete a bucket."""
    buckets = list_buckets()

    print("Select from the following buckets:\n")
    for bucket in buckets:
        print("\t" + bucket)

    # Assign this value before running the program
    bucket_name = input("Enter bucket name:\n")
    if bucket_name in buckets:
        print("success!")
        # Set up logging
        logging.basicConfig(level=logging.DEBUG,
                            format='%(levelname)s: %(asctime)s: %(message)s')

        # Delete the bucket
        s3_client = boto3.client('s3')
        try:
            s3_client.delete_bucket(Bucket=bucket_name)
            print("success!")
            logging.info(f'{bucket_name} was deleted')
            main_menu()
        except ClientError as error:
            logging.error(error)
            return False
    else:
        print("Failure!\n Please select again.")
        delete_bucket()


def exit_application():
    """Exit the application and provide user with a timestamp."""
    # dd/mm/YY H:M:S
    now = datetime.datetime.now()
    date_string = now.strftime("%m/%d/%Y %H:%M:%S")
    print(f"EXIT time: {date_string}")
    sys.exit()


def list_buckets():
    """Iterate through buckets and provide user with a list of buckets."""
    print("List all S3 Buckets.")

    # Create an S3 client
    s3_client = boto3.client('s3')
    # Call S3 to list current buckets
    response = s3_client.list_buckets()
    # Get a list of all bucket names from the response
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    return buckets


def print_buckets():
    """print_buckets()"""
    buckets = list_buckets()
    print('Existing buckets:')
    for obj in buckets:
        print(obj)
    # print(buckets)
    main_menu()


def list_all_items_buckets():
    """List all items in buckets."""
    print("Still working this out.")


def main_menu():
    """Provides user with a main-menu display."""
    user_selection = input("\n******************************************\n"
                           + "Please select from the following options:\n"
                           + "1. List all Buckets (L)\n"
                           + "2. Create an S3 Bucket (C)\n"
                           + "3. Delete an S3 Bucket (D)\n"
                           + "4. S3 Specific Actions - Submenu (S)\n"
                           + "5. Exit (Q)\n"
                           + "******************************************\n")

    if user_selection == '1':
        print("User selection: " + user_selection)
        print_buckets()
    elif user_selection == '2':
        print("User selection: " + user_selection)
        create_bucket()
    elif user_selection == '3':
        print("User selection: " + user_selection)
        delete_bucket()
    elif user_selection == '4':
        print("User selection: " + user_selection)
        sub_menu()
    elif user_selection == '5':
        print("User selection: " + user_selection)
        exit_application()


def sub_menu():
    """Provides user with a sub-menu display."""
    # Set these values before running the program
    # bucket_name = 'BUCKET_NAME'
    # file_name = 'FILE_NAME'

    sub_menu_selection = input("\n00000000000000000000000000000000000000000\n"
                               + "Please select from the submenu options:\n"
                               + "1. List all items in all Buckets (B)\n"
                               + "2. Add items to a Bucket (A)\n"
                               + "3. Delete items in a Bucket (D)\n"
                               + "4. Copy items in a Bucket (C)\n"
                               + "5. Download items from a Bucket (D)\n"
                               + "6. Return to Main Menu (M)\n"
                               + "7. Exit (Q)\n"
                               + "00000000000000000000000000000000000000000\n")

    if sub_menu_selection == '1':
        print("You selected to list all items in all Buckets\n User selection: "
              + sub_menu_selection)
        list_all_items_buckets()
        # add_items_buckets(file_name, bucket_name, object_name=None)
    elif sub_menu_selection == '2':
        print("You selected to Add items to a Bucket\n User selection: "
              + sub_menu_selection)
        add_items_buckets()
        # add_items_buckets(file_name, bucket_name, object_name=None)
    elif sub_menu_selection == '3':
        # 2. Delete items in a Bucket (D)\n"
        print("You selected to Delete items in a Bucket\n User selection: "
              + sub_menu_selection)
        delete_items_buckets()
    elif sub_menu_selection == '4':
        # 3. Copy items in a Bucket (C)\n"
        print("You selected to Copy items in a Bucket\n User selection: "
              + sub_menu_selection)
        copy_items_buckets()
    elif sub_menu_selection == '5':
        # "4. Download items from a Bucket (L)\n"
        print("You selected to Download items from a Bucket\n User selection: "
              + sub_menu_selection)
        download_items_buckets()
    elif sub_menu_selection == '6':
        # 5. Return to Main Menu (M)\n"
        print("You selected to Return to the Main Menu\n User selection: "
              + sub_menu_selection)
        main_menu()
    elif sub_menu_selection == '7':
        # 6. Exit (Q)\n"
        print("You selected to Exit the Application\n User selection: "
              + sub_menu_selection)
        exit_application()


main_menu()
