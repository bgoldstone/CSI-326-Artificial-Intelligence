"""
list_comprehension.py
List Comprehension problems for homework assignment #2.
Date: 2/1/2022
Author: Ben Goldstone
"""


def main():
    """
    main - Main function
    """

    # cat
    cat = ["cat" for _ in range(500)]
    print(f'Length: {len(cat)}, cat[0]: {cat[0]}, cat[499]: {cat[499]}')

    # Countdown
    count = [x for x in range(100, 0, -1)]
    print(f'\nLength: {len(count)}\nCountdown: \n{count}')

    # one_hundred_squares
    one_hundred_squares = [[x**2 for x in range(1, 101)] for _ in range(100)]
    print(
        f'Length: {len(one_hundred_squares)}, one_hundred_squares[0:5]: {one_hundred_squares[0][0:5]}, one_hundred_squares[95:] {one_hundred_squares[99][95:]}')
    # print("\n\n" + str(one_hundred_squares))

    # word count
    string = "Today is Monday and it is not very hot"
    word_count = [len(word) for word in string.split()]
    print(word_count)


if __name__ == "__main__":
    main()
