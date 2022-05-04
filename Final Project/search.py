from query import query
import os
DATA = os.path.join(os.path.abspath(__file__), "..", "data")
'''Main Runner for tf_idf'''
if __name__ == '__main__':
    inp = ''
    print('Welcome to the Muhlenberg Search Engine!!\n\n')
    while inp.lower() != 'exit':
        postfix = ''

        inp = input(
            'What is your search term? (type \'exit\' to exit program) ')
        if inp == 'exit':
            continue
        stopwords = input('\nWould you like stopwords? (y/n)')
        stemming = input('\nWould you like stemming? (y/n)')
        if stemming == 'y' and stopwords == 'y':
            postfix = '_stopwords_stemming'
        if stemming == 'y':
            postfix = '_stemming'
        if stopwords == 'y':
            postfix = '_stopwords'
        q = query(DATA, postfix, inp)
        quit_search = ''
        for index, url in enumerate(q):
            if quit_search == 'n':
                break
            print(f'Title: {url[0]}\nLink: {url[1]}\n\n')
            if index % 10 == 0 and index != 0:
                quit_search = input('\nDo you want to see more links? (y/n)')
            if index == len(q):
                print(
                    "No more results! Please enter a new search term if you would like.")
