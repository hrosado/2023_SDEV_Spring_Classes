
def addition(num_01, num_02):
    answer = num_01 + num_02
    return answer


def main():
    num_01 = int(input("Number 1: "))
    num_02 = int(input("Number 2: "))

    # addition(num_01, num_02)
    answer = addition(num_01, num_02)
    print(answer)


if __name__ == '__main__':
    main()
