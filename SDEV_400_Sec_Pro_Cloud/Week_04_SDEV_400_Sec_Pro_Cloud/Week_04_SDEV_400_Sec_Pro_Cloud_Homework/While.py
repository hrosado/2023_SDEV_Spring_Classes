

def test_input_example(test_answer):
    if test_answer == '2':
        return False


def input_example():
    test_answer = input("Enter value: \n")
    test_input_example(test_answer, result)
    if test_input_example:
        print()
    else:
        print()


input_example()
