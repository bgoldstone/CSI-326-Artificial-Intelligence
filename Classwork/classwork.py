from msilib.schema import LockPermissions
import random
from typing import List
from webbrowser import get


def main() -> None:
    numbers = [random.randint(-100, 100) for _ in range(100)]
    newList = [num for num in numbers if num >= 0]
    numbersWithThree = [num for num in range(1, 1001) if '3' in str(num)]
    print(f"Numbers: {numbers}")
    print(f"New List: {newList}")
    print(f'Numbers With Three: {numbersWithThree}')
    print("Space count:", getCountOfSpaces("Hello, World. I am Ben!"))
    print("Remove Vowels:", removeVowels("Hello World!"))
    print("Less than 4 letters:", lessThan4Letters(
        "Hello Professor Silveyra, I am in AI Class today. What about you?"))


def getCountOfSpaces(string: str) -> int:
    return len(string.split())


def removeVowels(words: str) -> str:
    return "".join([char for char in words if char not in ['a', 'e', 'i', 'o', 'u']])


def lessThan4Letters(words: str) -> List:
    return [word for word in words.split() if len(word) < 4]


if __name__ == '__main__':
    main()
