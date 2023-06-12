user_selection: str = input("Enter a number from 1 - 5: \n")


def menu_options(user_selection):
    switcher = {
        1: print("list_buckets()"),
        2: print("create_bucket()"),
        3: print("delete_bucket()"),
        4: print("sub_menu()"),
        5: print("exit_application()")
    }
    # func = switcher.get(user_selection, "Invalid entry")
    return switcher.get(user_selection, "Invalid entry")
    # return func()


menu_options(user_selection)





