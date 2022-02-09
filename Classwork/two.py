"""Date: 1/25/2022
    Classroom Example
    """
import one

print("top-level in two.py")
one.func()
    
if __name__ == '__main__':
    print("two.py is being run directly")
else:
    print("two.py is being imported into another module")
