from tkinter import *
import os
import webbrowser
from query import query

DATA = os.path.join(os.path.abspath(__file__), "..", "data")
VIEW = 0
URLS = {}
CURRENT_SEARCH = ''
INDEX = ''


def search():
    global CURRENT_SEARCH, URLS, DATA, VIEW
    global URLS
    postfix = ''
    if stemmed and stopwords:
        postfix = '_stopwords_stemming'
    elif stemmed:
        postfix = '_stemming'
    elif stopwords:
        postfix = '_stopwords'
    search_term = field.get()
    if search_term != CURRENT_SEARCH:
        VIEW = 0
    URLS = query(DATA, postfix, search_term)
    CURRENT_SEARCH = search_term
    start_row = 3
    if 'btn' in locals():
    for i in range(10):
        btn[i].grid_forget()
        label[i].grid_forget()
    btn = [i for i in range(10)]
    label = [i for i in range(10)]
    current_urls = [i for i in range(10)]
    print(VIEW)
    for i in range(10):
        try:
            current_urls[i] = URLS[VIEW+i][1]
        except Exception:
            Label(app, text='').grid(row=start_row, column=0, columnspan=2)
            start_row += 2
            continue
        Label(app, text=URLS[VIEW+i][0],
              width=90).grid(row=start_row, column=0)
        btn[i] = Button(app, text="Visit Page", width=5, padx=10,
                        borderwidth=1)
        btn[i].grid(row=start_row, column=1)
        label[i] = Label(app, text="")
        label[i].grid(row=start_row+1, column=0)
        start_row += 2
    prev_btn = Button(app, text="Previous", width=5, padx=10, borderwidth=1,
                      command=decrease_results)
    prev_btn.grid(row=start_row, column=0)
    next_btn = Button(app, text="Next", width=5, padx=10, borderwidth=1,
                      command=increase_results)
    next_btn.grid(row=start_row, column=1)
    btn[1].configure(command=lambda: webbrowser.open(current_urls[1]))
    btn[0].configure(command=lambda: webbrowser.open(current_urls[0]))
    btn[2].configure(command=lambda: webbrowser.open(current_urls[2]))
    btn[3].configure(command=lambda: webbrowser.open(current_urls[3]))
    btn[4].configure(command=lambda: webbrowser.open(current_urls[4]))
    btn[5].configure(command=lambda: webbrowser.open(current_urls[5]))
    btn[6].configure(command=lambda: webbrowser.open(current_urls[6]))
    btn[7].configure(command=lambda: webbrowser.open(current_urls[7]))
    btn[8].configure(command=lambda: webbrowser.open(current_urls[8]))
    btn[9].configure(command=lambda: webbrowser.open(current_urls[9]))


def increase_results():
    global VIEW
    VIEW += 10
    search()


def decrease_results():
    global VIEW
    VIEW += 10
    search()


app = Tk()
stemmed = ''
stopwords = ''
app.title('Muhlenberg Search')
app.geometry('800x600+10+40')
app.iconbitmap(os.path.join(os.path.dirname(__file__), 'muhlenberg.ico'))
heading = Label(
    app, text='Welcome to Muhlenberg search!\tPlease enter a query to begin.', justify='center')
heading.grid(row=0, column=0, columnspan=2)
stem_checkbox = Checkbutton(
    app, text="Stemmed", variable=stemmed, onvalue=True, offvalue=False)
stopwords_checkbox = Checkbutton(
    app, text="Stopwords", variable=stopwords, onvalue=True, offvalue=False)
stem_checkbox.grid(row=1, column=0)
stopwords_checkbox.grid(row=1, column=1)
field = Entry(app, textvariable="Search Muhlenberg.edu",
              justify='center', width=90)
field.grid(row=2, column=0, columnspan=2)
search_btn = Button(app, text="Search", command=search,
                    fg='#ffffff', bg='#a41e34')
search_btn.grid(row=2, column=2, padx=5)
app.mainloop()
