import random


def create_bucket():
    """Create a bucket."""
    # Allow the user an option to exit and ensure user input is single string character
    while True:
        user_choice = input("\nWould you like to Create an S3 Bucket? Y/N\n")
        if len(user_choice) == 1:
            print(
                f'\nYour single character input was: {user_choice.upper()} \n')
            if user_choice.upper() == 'N':
                print("You will be returned to the Main Menu. ...")
                exit()
                # main_menu()
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

                bucketname = first_name + last_name + "-" + numrangen
                print(f"S3 Bucket name is:  {bucketname} \n")

        # print("Please enter a single character to continue\n")

    # Prompt user for
    # Uncomment below
    # main_menu()


create_bucket()
