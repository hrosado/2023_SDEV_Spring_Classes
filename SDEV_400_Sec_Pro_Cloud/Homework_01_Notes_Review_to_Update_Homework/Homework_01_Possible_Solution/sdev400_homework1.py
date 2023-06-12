"""
| __filename__ = "sdev400_homework1.py"
| __coursename__ = "SDEV 400 - Secure Programming in the Cloud"
| __author__ = "Craig Poma"
| __copyright__ = "Craig Poma"
| __credits__ = ["Craig Poma"]
| __license__ = "MIT"
| __version__ = "1.0.0"
| __maintainer__ = "Craig Poma"
| __email__ = "craig.poma@faculty.umgc.edu"
| __status__ = "Baseline"
| __docformat__ = 'reStructuredText'

:blackboldunderline:`REQUIREMENTS:`

Assignment general requirements for options / menu items:
 * Creates a S3 bucket with the name consisting of your firstname, lastname and a \
random 6-digit suffix.

    * :boldred:`ERROR CHECKING` - First and Last name can only contain valid **name** characters \
    (i.e. A-Z, a-z, and -). The application does not allow a name to have an apostrophe \
    (**'**) as it is not DNS safe. A name should not contain numbers except for the \
    randomly generated 6-digit suffix.
    * :boldred:`ERROR CHECKING` - Bucket names can only be 3 - 63 characters in length
    * :boldred:`ERROR CHECKING` - Should not create a bucket with the same name that \
    already exists. Bucket names must be unique.
 * Puts objects in a previously created bucket.

    * Implemented to use the error.log that application generates while running. This could be \
    enhanced to ask for a specific file to be uploaded, but this wasn't a requirement.
 * Deletes an object in a bucket.

    * All objects in the bucket will be listed. There is no **paging**, the list could be long.
    * :boldred:`ERROR CHECKING` - You cannot select a bucket outside of the range of listed \
    buckets for the object source.
    * :boldred:`ERROR CHECKING` - You cannot select an object outside of the range of listed \
    objects to delete.
 * Deletes a bucket.

    * All available buckets will be listed. There is no **paging**, the list could be long.
    * Bucket must be empty.
    * :boldred:`ERROR CHECKING` - The application will print an error if the selected bucket \
    is not empty.
    * :boldred:`ERROR CHECKING` - You cannot select a bucket outside of the range of listed \
    buckets for target bucket.
 * Copies and object from one bucket to another.

    * All available buckets will be listed. There is no **paging**, the list could be long.
    * Source and Destination bucket selected must be different.
    * :boldred:`ERROR CHECKING` - If the user attempts to select the same Destination as the \
    Source an error message will be printed.
    * :boldred:`ERROR CHECKING` - You cannot select a bucket outside of the range of listed \
    buckets for Source or Destination.
    * :boldred:`ERROR CHECKING` - You cannot select an object outside of the range of listed \
    objects to copy.
 * Downloads an existing object from a bucket.

   * All objects in the bucket will be listed. There is no **paging**, the list could be long.
   * Will download the selected object an place it in the current directory. The file \
    downloaded will be named **temp_file**
 * Exit the program. Upon exit, the application should list the date and time

"""

import datetime
import logging
import random
import re
import string
import sys
import boto3
from botocore.exceptions import ClientError

REGION = 'us-east-1'
####################################################################
# Catch Exceptions and write them to log file in current folder.
####################################################################
logging.basicConfig(filename='./error.log',
                    format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='w', # Overwrite the log file
                    level=logging.INFO)
# # set up logging to console
# console = logging.StreamHandler()
# console.setLevel(logging.DEBUG)
# # set a format which is simpler for console use
# formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
# console.setFormatter(formatter)
# # add the handler to the root logger
# logging.getLogger('').addHandler(console)
####################################################################

def generic_output_msg(log_message=None):
    """
    Write log to file and screen/console

    :param log_message(str): String to output to logs file and screen/console
    :rtype: **None**
    :return: **None**
    """
    if log_message is not None:
        logging.info(log_message)
        print("\r\n")
        print('*' * 100, "\r\n", log_message)
        print('*' * 100, "\r\n")

def validate_name(default_prompt=None):
    """
    Capture and Validate Name meets naming requirement

    :param default_prompt(str): Value string to place in the input prompt
    :rtype: **str**
    :return: **selection(str)**: Name (First or Last) validated to match \
    A-Z, a-z, and -. Must be DNS compliant so, apostrophe (') not treated as a \
    valid name character (i.e. O'Brian will not work - it isn't DNS compliant).\
    Name will be returned lowercase to match S3 requirement of lowercase bucket\
    names.
    """

    valid_input = 0
    while not valid_input:
        selection = str(input(default_prompt))
        # Handle A-Z a-z and - in name
        if not re.fullmatch('^[a-z A-Z]+(-[a-z A-Z]+)?$', selection):
            print("\r\n")
            print('*' * 93, "\r\n",
                  'Your name contains invalid characters')
            print('*' * 93)
        else:
            valid_input = 1

    # Lowering the case of the name entered to be compliant with S3 rules
    return selection.lower()

def validate_constraint(default_prompt=None, zero_valid=True,
                        exit_on_error=True, max_range=None):
    """
    Capture and Validate value types

    :param default_prompt(str): Message prompt for requesting value.
    :param zero_valid(bool): Is zero (0) a valid value? Default: True
    :param max_range(bool): Bound the value entered to less than this range, if set. Default: None

    :rtype: **int**
    :return: **selection(int)**: if valid integer entered.
    :rtype: **str**
    :return: **selection(str)**: 'ERROR', if invalid integer entered.
    """

    try:
        selection = int(input(default_prompt))
        if selection == 0 and not zero_valid:
            print("\r\n")
            print('*' * 88, "\r\n",
                  'You input an',
                  'invalid constraint value.', "\r\n",
                  'Values for this constraint should be positive integers',
                  'and non-zero.')
            print('*' * 88, "\r\n")
            selection = "ERROR"
        elif selection < 0:
            print("\r\n")
            print('*' * 88, "\r\n",
                  'You input an',
                  'invalid constraint value.', "\r\n",
                  'Values should be positive integers.')
            print('*' * 88, "\r\n")
            selection = "ERROR"

        if max_range is not None and selection > max_range:
            print("\r\n")
            print('*' * 88, "\r\n",
                  'You input a',
                  'range too large for expected completion.')
            print('*' * 88, "\r\n")
            selection = "ERROR"
    except ValueError as _:
        print("\r\n")
        print('*' * 88, "\r\n",
              'You input an',
              'invalid constraint value. \r\n Values should be digits.')
        print('*' * 88, "\r\n")
        selection = "ERROR"

    if selection == 'ERROR' and exit_on_error:
        sys.exit()

    return selection

def confirm_continue(default_prompt=' Do you want to continue? (Y or N):',
                     exit_message='Thanks for trying the '
                     + ' Application. You have selected to exit.',
                     seperator_count=88, exit_app=True):
    """
    Confirm user wishes to proceed

    :param default_prompt(str): Value string to place in the input prompt. \
    Default: Do you want to continue? (Y or N):
    :param exit_message(str): Value string to place if application exit \
    occurs. Default: Thanks for trying the Application. \
    You have selected to exit.
    :param seperator_count(str): Border of * chars count surrounding \
    messages. Default: 88
    :param exit_app(bool): Should application exit on 'No'. Default: True
    :rtype: **str**
    :return:  **selection(str)**: Returns YES if successful.
    """
    valid_answer_set = ['Y', 'YES', 'N', 'NO']
    # User Input
    selection = None
    while selection not in valid_answer_set:
        selection = str(input(default_prompt)).upper()
        if selection not in valid_answer_set:
            print("",
                  " #######################################",
                  ' Please make a valid selection Y or N',
                  " #######################################", "", sep='\r\n')
    if selection in ['N', 'NO']:
        print("\r\n")
        print('*' * seperator_count, "\r\n",
              exit_message)
        print('*' * seperator_count)
        if exit_app:
            sys.exit(0)

    if selection == 'Y':
        selection = 'YES'

    return selection

def create_bucket(bucket_name=None, s3_handle=None, region=None):
    """
    Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :red:`Based off AWS S3 Sample - create_bucket.py - Dated 2019-06-24`

    :param bucket_name(str): Bucket to create
    :param s3_handle(boto3.session.Session.client('s3')): Access object to S3
    :param region(str): String region to create bucket in, e.g., 'us-west-2'
    :rtype: **bool**
    :return: True if bucket created, else False
    :raises: **AttributeError:** S3 Handle not initialized for access to AWS S3
    :raises: **botocore.exceptions.ClientError.AllAccessDisabled:** S3 Access Disabled
    """

    try:
        # us-east-1 is the default region and will cause an error if you attempt to specify it.
        if region == 'us-east-1':
            region = None

        if region is None:
            s3_handle.create_bucket(Bucket=bucket_name)
        else:
            s3_handle = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_handle.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as client_exception:
        logging.error(client_exception)
        return False
    except AttributeError as _:
        log_message = 's3_handle is not initialized for connection to AWS S3'
        generic_output_msg(log_message)
        sys.exit()

    return True

def list_buckets(s3_handle=None):
    """
    List the objects in an Amazon S3 bucket

    :red:`Based off AWS S3 Sample - s3-python-example-list-buckets.py - Dated 2018-06-25`

    :param s3_handle(boto3.session.Session.client('s3')): Access object to S3
    :return: None
    :raises: **AttributeError:** S3 Handle not initialized for access to AWS S3
    :raises: **botocore.exceptions.ClientError.AllAccessDisabled:** S3 Access Disabled
    """

    buckets = []
    try:
        # Call S3 to list current buckets
        response = s3_handle.list_buckets()
        # Get a list of all bucket names from the response
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        # Print out the bucket list
        # print("Bucket List: %s" % buckets)
    except ClientError as client_exception:
        # AllAccessDisabled error == bucket not found
        logging.error(client_exception)
    except AttributeError as _:
        log_message = 's3_handle is not initialized for connection to AWS S3'
        generic_output_msg(log_message)
        sys.exit()

    return buckets

def delete_bucket(bucket_name=None, s3_handle=None):
    """Delete an empty S3 bucket

    If the bucket is not empty, the operation fails.

    :red:`Based off AWS S3 Sample - delete_bucket.py - Dated 2019-2-12`

    :param bucket_name(str): Bucket to delete
    :param s3_handle(boto3.session.Session.client('s3')): Access object to S3
    :rtype: **bool**
    :return: True if the referenced bucket was deleted, otherwise False
    :raises: **AttributeError:** S3 Handle not initialized for access to AWS S3
    :raises: **botocore.exceptions.ClientError.AllAccessDisabled:** S3 Access Disabled
    """

    try:
        s3_handle.delete_bucket(Bucket=bucket_name)
    except ClientError as client_exception:
        logging.error(client_exception)
        return False
    except AttributeError as _:
        log_message = 's3_handle is not initialized for connection to AWS S3'
        generic_output_msg(log_message)
        sys.exit()

    return True

def put_object(dest_bucket_name=None, dest_object_name=None, src_data=None, s3_handle=None):
    """
    Add an object to an Amazon S3 bucket

    The src_data argument must be of type bytes or a string that references
    a file specification.

    :red:`Based off AWS S3 Sample - put_object.py - Dated 2019-2-15`

    :param dest_bucket_name(str): Destination bucket location
    :param dest_object_name(str): Object name when placed into bucket
    :param src_data(str): String reference to file for upload
    :param src_data(bytes): bytes of data for upload
    :param s3_handle(boto3.session.Session.client('s3')): Access object to S3
    :rtype: **bool**
    :return: True if src_data was added to dest_bucket/dest_object, otherwise False
    :raises: **AttributeError:** S3 Handle not initialized for access to AWS S3
    :raises: **botocore.exceptions.ClientError.AllAccessDisabled:** S3 Access Disabled
    :raises: **botocore.exceptions.ClientError.NoSuchKey:** Source/Destination Bucket does not exist
    :raises: **botocore.exceptions.ClientError.InvalidRequest:** Invalid request
    """

    # Construct Body= parameter
    if isinstance(src_data, bytes):
        object_data = src_data
    elif isinstance(src_data, str):
        try:
            object_data = open(src_data, 'rb')
            # possible FileNotFoundError/IOError exception
        except FileNotFoundError as file_exception:
            logging.error(file_exception)
            return False
        except IOError as file_exception:
            logging.error(file_exception)
            return False
    else:
        log_message = 'Type of {} for the argument \'src_data\' is not supported.'\
            .format(str(type(src_data)))
        generic_output_msg(log_message)
        return False

    try:
        s3_handle.put_object(Bucket=dest_bucket_name, Key=dest_object_name, Body=object_data)
    except ClientError as client_exception:
        # AllAccessDisabled error == bucket not found
        # NoSuchKey or InvalidRequest error == (dest bucket/obj == src bucket/obj)
        logging.error(client_exception)
        return False
    except AttributeError as _:
        log_message = 's3_handle is not initialized for connection to AWS S3'
        generic_output_msg(log_message)
        sys.exit()
    finally:
        if isinstance(src_data, str):
            object_data.close()
    return True

def get_bucket_selection(s3_handle=None, bucket_prompt='Which bucket?:'):

    """
    Select a Bucket

    :param s3_handle(boto3.session.Session.client('s3')): Access object to S3
    :param bucket_prompt(str): Prompt for bucket input request
    :rtype: **str**
    :return: **selection(str)**: Bucket name selected
    """
    # Get Existing buckets
    existing_buckets = list_buckets(s3_handle=s3_handle)
    print(bucket_prompt)
    selection = None
    if len(existing_buckets) == 0:
        log_message = 'You have no buckets.'
        generic_output_msg(log_message)
    else:
        bucket_index = 0
        for a_bucket in existing_buckets:
            print("{}. {}".format(bucket_index, a_bucket))
            bucket_index = bucket_index + 1
        selection = 'ERROR'
        while len(selection.strip(string.digits)) != 0:
            selection = str(validate_constraint(default_prompt="Enter bucket number:",
                                                zero_valid=True, exit_on_error=False,
                                                max_range=bucket_index - 1))

        selection = existing_buckets[int(selection)]
    return selection

def create_s3_bucket_by_name(s3_handle=None, region=None):
    """
    Create a bucket based on user first and last name plus random 6 digit suffix.\
    If the name ends up be greater than 63 characters an error will be logged. \
    Bucket names must be between 3 and 63 characters in length.

    :param s3_handle(boto3.session.Session.client('s3')): Access object to S3
    :param region(str): String region to create bucket in, e.g., 'us-west-2'
    :rtype: **None**
    :return: **None**
    """

    # Get Existing bucket to prevent duplication.
    existing_buckets = list_buckets(s3_handle=s3_handle)

    first_name = validate_name(' What is your first name? ')
    confirm_continue()
    last_name = validate_name(' What is your last name? ')
    confirm_continue()

    # Make a name + 6 digit bucket, Note: randint() is inclusive
    # Creates a S3 bucket with the name consisting of your firstname, lastname and a
    # random 6-digit suffix.
    bucket_set = [first_name + last_name + '-' + str(random.randint(100000, 999999))]
    # Done as a for loop to support multiple bucket creation modification, if required.
    for new_bucket_name in bucket_set:

        # Bucket names must be between 3 and 63 characters long.
        if len(new_bucket_name) >= 3 and len(new_bucket_name) <= 63:
            # Create a bucket in a specified region
            if new_bucket_name not in existing_buckets \
                    and create_bucket(bucket_name=new_bucket_name,
                                      region=region, s3_handle=s3_handle):
                log_message = 'Created bucket {} in region {}.'.format(new_bucket_name, region)
                generic_output_msg(log_message)
            elif new_bucket_name in existing_buckets:
                log_message = 'Bucket {} exists in region {}.'.format(new_bucket_name, region)
                generic_output_msg(log_message)
        else:
            log_message = 'Bucket {} not compliant with 3 - 63 character name constraint of {}.'\
                .format(new_bucket_name, region)
            generic_output_msg(log_message)

def upload_object_to_bucket(s3_handle=None):
    """
    Upload error.log to selected bucket

    :param s3_handle(boto3.session.Session.client('s3')): Access object to S3
    :rtype: **None**
    :return: **None**
    """
    selected_bucket = get_bucket_selection(s3_handle=s3_handle,
                                           bucket_prompt="Which bucket should the "
                                                         + "object be placed?")

    if put_object(dest_bucket_name=selected_bucket,
                  dest_object_name='error.log',
                  src_data='./error.log', s3_handle=s3_handle):
        log_message = 'error.log was uploaded to {}.'.format(selected_bucket)
        generic_output_msg(log_message)

def select_bucket_object(bucket_name=None, s3_handle=None):
    """
    List the objects in an Amazon S3 bucket. Allows the user to select one for action.

    :red:`Based off AWS S3 Sample - list_objects.py - Dated 2019-2-13`

    :param bucket_name(str): Bucket to query and list object contained
    :param s3_handle(boto3.session.Session.client('s3')): Access object to S3
    :rtype: **dict**
    :return: selection(dict): Selected bucket object. If error, return None.
    :raises: **AttributeError:** S3 Handle not initialized for access to AWS S3
    :raises: **botocore.exceptions.ClientError.AllAccessDisabled:** S3 Access Disabled
    """

    selection = None
    try:
        response = s3_handle.list_objects_v2(Bucket=bucket_name)
        if response['KeyCount'] > 0:
            # List the object names
            bucket_index = 0
            for a_bucket_object in response['Contents']:
                print("{}. {}".format(bucket_index, a_bucket_object["Key"]))
                bucket_index = bucket_index + 1
            selection = 'ERROR'
            while len(selection.strip(string.digits)) != 0:
                selection = str(validate_constraint(default_prompt="Enter object number:",
                                                    zero_valid=True, exit_on_error=False,
                                                    max_range=bucket_index - 1))
            selection = response['Contents'][int(selection)]

    except ClientError as client_exception:
        # AllAccessDisabled error == bucket not found
        logging.error(client_exception)
    except AttributeError as _:
        log_message = 's3_handle is not initialized for connection to AWS S3'
        generic_output_msg(log_message)
        sys.exit()

    return selection

def delete_a_bucket_object(s3_handle=None):
    """
    Delete an object from a bucket

    :red:`Based off AWS S3 Sample - delete_object.py - Dated 2019-2-12`

    :param s3_handle(boto3.session.Session.client('s3')): Access object to S3
    :rtype: **None**
    :return: **None**
    :raises: **AttributeError:** S3 Handle not initialized for access to AWS S3
    :raises: **botocore.exceptions.ClientError.AllAccessDisabled:** S3 Access Disabled
    """

    selected_bucket = get_bucket_selection(s3_handle=s3_handle,
                                           bucket_prompt="Which bucket would you like "
                                                         + "to delete from?")

    selected_object = select_bucket_object(bucket_name=selected_bucket,
                                           s3_handle=s3_handle)
    try:
        if selected_object is not None:
            s3_handle.delete_object(Bucket=selected_bucket,
                                    Key=selected_object['Key'])
            log_message = 'Deleted object {} from bucket {}.'.format(selected_object['Key'],
                                                                     selected_bucket)
            generic_output_msg(log_message)
        else:
            log_message = 'The bucket {} is empty.'.format(selected_bucket)
            generic_output_msg(log_message)
    except ClientError as client_exception:
        logging.error(client_exception)
    except AttributeError as _:
        log_message = 's3_handle is not initialized for connection to AWS S3'
        generic_output_msg(log_message)
        sys.exit()

def delete_a_bucket(s3_handle=None):
    """
    Delete a bucket

    :red:`Based off AWS S3 Sample - delete_bucket.py - Dated 2019-2-12`

    :param s3_handle(boto3.session.Session.client('s3')): Access object to S3
    :rtype: **None**
    :return: **None**
    :raises: **AttributeError:** S3 Handle not initialized for access to AWS S3
    :raises: **botocore.exceptions.ClientError.AllAccessDisabled:** S3 Access Disabled
    """

    selected_bucket = get_bucket_selection(s3_handle=s3_handle,
                                           bucket_prompt="Which bucket would you like to delete?")
    try:
        response = s3_handle.list_objects_v2(Bucket=selected_bucket)
        if response['KeyCount'] > 0:
            log_message = 'The bucket {} is not empty'.format(selected_bucket) \
                          + ' you must first delete the {} '.format(len(response['Contents'])) \
                          + 'object(s) from the bucket.'
            generic_output_msg(log_message)

        else:
            s3_handle.delete_bucket(Bucket=selected_bucket)
            log_message = 'Deleted bucket {}'.format(selected_bucket)
            generic_output_msg(log_message)
    except ClientError as client_exception:
        logging.error(client_exception)
    except AttributeError as _:
        log_message = 's3_handle is not initialized for connection to AWS S3'
        generic_output_msg(log_message)
        sys.exit()

def copy_bucket_object(s3_handle=None):
    """
    Copy an object from one bucket to another

    :red:`Based off AWS S3 Sample - copy_object.py - Dated 2019-2-12`

    :param s3_handle(boto3.session.Session.client('s3')): Access object to S3
    :rtype: **None**
    :return: **None**
    :raises: **AttributeError:** S3 Handle not initialized for access to AWS S3
    :raises: **botocore.exceptions.ClientError.AllAccessDisabled:** S3 Access Disabled
    """

    source_bucket = get_bucket_selection(s3_handle=s3_handle,
                                         bucket_prompt="Which bucket will be the source bucket?")
    try:
        response = s3_handle.list_objects_v2(Bucket=source_bucket)
        if response['KeyCount'] == 0:
            log_message = 'The bucket {} is empty, you must select a bucket with objects' \
                .format(source_bucket)
            generic_output_msg(log_message)
        else:
            selected_object = select_bucket_object(bucket_name=source_bucket,
                                                   s3_handle=s3_handle)

            destination_bucket = source_bucket
            while source_bucket == destination_bucket:
                destination_bucket = get_bucket_selection(s3_handle=s3_handle,
                                                          bucket_prompt="Which bucket will be the"
                                                                        + " destination bucket?")
                if source_bucket == destination_bucket:
                    log_message = 'Source Bucket and Destination Bucket cannot be the same!'
                    generic_output_msg(log_message)
            try:
                copy_source = {'Bucket': source_bucket, 'Key': selected_object['Key']}
                s3_handle.copy_object(CopySource=copy_source, Bucket=destination_bucket,
                               Key=selected_object['Key'])

                log_message = 'Copied Object {} from Source {} to Destination {}'\
                    .format(selected_object['Key'], source_bucket, destination_bucket)
                generic_output_msg(log_message)

            except ClientError as client_exception:
                logging.error(client_exception)
    except ClientError as client_exception:
        logging.error(client_exception)
    except AttributeError as _:
        log_message = 's3_handle is not initialized for connection to AWS S3'
        generic_output_msg(log_message)
        sys.exit()

def get_bucket_object(s3_handle=None):
    """
    Get an object from a bucket

    :red:`Based off AWS S3 Sample - get_object.py - Dated 2019-2-13`

    :param s3_handle(boto3.session.Session.client('s3')): Access object to S3
    :rtype: **None**
    :return: **None**
    :raises: **AttributeError:** S3 Handle not initialized for access to AWS S3
    :raises: **botocore.exceptions.ClientError.AllAccessDisabled:** S3 Access Disabled
    """

    source_bucket = get_bucket_selection(s3_handle=s3_handle,
                                         bucket_prompt="Which bucket will be the source bucket?")
    try:
        response = s3_handle.list_objects_v2(Bucket=source_bucket)
        if response['KeyCount'] == 0:
            log_message = 'The bucket {} is empty'.format(source_bucket) \
                          + ', you must select a bucket with objects'
            generic_output_msg(log_message)
        else:
            selected_object = select_bucket_object(bucket_name=source_bucket,
                                                   s3_handle=s3_handle)

            try:
                # Download the file from S3
                s3_handle.download_file(source_bucket, selected_object['Key'], 'temp_file')
                # print(open('temp_file').read())
                log_message = 'Object {} from Source {}'.format(selected_object['Key'],
                                                                source_bucket) \
                              + ' downloaded as ./temp_file'
                generic_output_msg(log_message)
            except ClientError as client_exception:
                # AllAccessDisabled error == bucket or object not found
                logging.error(client_exception)
    except ClientError as client_exception:
        logging.error(client_exception)
    except AttributeError as _:
        log_message = 's3_handle is not initialized for connection to AWS S3'
        generic_output_msg(log_message)
        sys.exit()

def main():
    """ SDEV400 - Homework 1 - Using S3 """

    # Create S3 Handle for interfacing with AWS
    s3_handle = boto3.client('s3')
    #   Menu
    print('*' * 88)
    print(' Welcome to the Python SDEV400 Homework 1 Application.')
    print('*' * 88)

    while True:
        print(' What would you like to do today? ')
        print(" \t a. Creates a S3 bucket with the name consisting of your firstname, lastname"
              + " and a random 6-digit suffix. ")
        print(" \t b. Put an object (current error.log) in a previously created bucket. ")
        print(" \t c. Delete an object in a bucket. ")
        print(" \t d. Delete a bucket.")
        print(" \t e. Copy and object from one bucket to another. ")
        print(" \t f. Downloads an existing object from a bucket. ")
        print(" \t q. Exit the program. ")
        selection = input("Enter selection: ")
        if selection.upper() == "A":
            # Creates a S3 bucket with the name consisting of your firstname,
            # lastname and a random 6-digit suffix.
            create_s3_bucket_by_name(s3_handle=s3_handle, region=REGION)
        elif selection.upper() == "B":
            # Puts objects in a previously created bucket.
            upload_object_to_bucket(s3_handle=s3_handle)
        elif selection.upper() == "C":
            # Deletes an object in a bucket.
            delete_a_bucket_object(s3_handle=s3_handle)
        elif selection.upper() == "D":
            # Deletes a/the bucket.
            delete_a_bucket(s3_handle=s3_handle)
        elif selection.upper() == "E":
            # Copies and object from one bucket to another.
            copy_bucket_object(s3_handle=s3_handle)
        elif selection.upper() == "F":
            # Downloads an existing object from a bucket.
            get_bucket_object(s3_handle=s3_handle)
        elif selection.upper() == "Q":
            # Exit the program. Upon exit, the application should list the date and time.
            current_data_time = datetime.datetime.now()
            formatted_date_time = current_data_time.strftime("%m-%d-%Y %H:%M:%S")
            print("\r\n")
            print('*' * 88, "\r\n",
                  'Thanks for trying the Python SDEV400 Homework 1 Application.',
                  'You have selected to exit ', "\r\n",
                  'the application. Have a nice day.')
            print('*' * 88)
            print("\r\n")
            print('*' * 88)
            print("\tExit time: {}".format(formatted_date_time))
            print('*' * 88)
            print("\r\n")
            break
        else:
            print("\r\n")
            print('*' * 88, "\r\n",
                  'Please enter a valid option a - f or q to Quit.')
            print('*' * 88)
            print("\r\n")
            continue

if __name__ == '__main__':
    main()
