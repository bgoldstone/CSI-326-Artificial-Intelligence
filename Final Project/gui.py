from tkinter import *
import os
import webbrowser
from query import query

DATA = os.path.join(os.path.abspath(__file__), "..", "data")
VIEW = 0
URLS = {}
CURRENT_SEARCH = ''


def search():
    global CURRENT_SEARCH, URLS, DATA, VIEWS
    global URLS
    search_term = field.get()
    if search_term != CURRENT_SEARCH:
        URLS = query(DATA, search_term)
        CURRENT_SEARCH = search_term
    start_row = 2
    for i in range(10):
        Label(app, URLS[VIEW+i], width=90).grid(row=start_row, column=0)
        Button(app, text="Visit Page", width=5, padx=5, command=lambda: webbrowser.open(
            URLS[VIEW+i])).grid(row=start_row, column=1)
        Label(app, "").grid(row=start_row+1, column=0)
        start_row += 2


app = Tk()
app.title('Muhlenberg Search')
app.geometry('600x300+10+40')
app.iconbitmap(os.path.join(os.path.dirname(__file__), 'muhlenberg.ico'))
heading = Label(
    app, text='Welcome to Muhlenberg search!\nPlease enter a query to begin.', justify='center')
heading.grid(row=0, column=0)
field = Entry(app, textvariable="Search Muhlenberg.edu",
              justify='center', width=90)
field.grid(row=1, column=0)
search = Button(app, text="Search", command=search, fg='#ffffff', bg='#a41e34')
search.grid(row=1, column=1, padx=5)
app.mainloop()
