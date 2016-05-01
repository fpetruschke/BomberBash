import tkinter as tk

import sys
import random
import threading

#Defining Font style
LARGE_FONT = ("Helvetica", 12)
MEDIUM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

# default values for gamefield size
rowValue = 5
colValue = 5

'''BomberBash class'''
# initialising class
# inherits from tk.TK class
class BomberBash(tk.Tk):
    # init method: works like constructor
    # self: standard implied parameter
    # *args: arguments --> any number or variable
    # **kwargs: keyword arguments --> e.g. dictionaries
    def __init__(self,*args, **kwargs):

        # call the init again
        tk.Tk.__init__(self,*args,**kwargs)

        # setting the windows size
        tk.Tk.minsize(self, width=400, height=300)
        tk.Tk.maxsize(self, width=500, height=400)

        # define container as a tk.Frame
        container = tk.Frame(self)

        # pack: packs the element just into wherever is place for it
        # fill: fills the entire space, expand: can get bigger than initialised
        container.pack(side="top", fill="both", expand=True)
        # gird: you can define exactly where the element should be placed
        # 0 = minimum size, weight: priority level
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        '''PAGES - all pages must be defined inside the F tupel !!!'''
        # dictionary for all the frames
        self.frames = {}
        for F in (PageMainMenu, PageGameStart, PageSettings, PageCredits):
            # initial page which will be run
            frame = F(container, self)
            self.frames[F] = frame
            #assigning the frame to the grid with row and column
            # empty rows/columns will be ignored
            # sticky: north south east west: direction to align + stretch
            frame.grid(row=0, column=0, sticky="nsew")

        # decide what page/frame will be shown
        self.show_frame(PageMainMenu)

    # method for switching pages
    # takes self and name of the container/frame content
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

'''PageMainMenu class'''
# inherits from tk.Frame class
# represents the "PageMainMenu"
class PageMainMenu(tk.Frame):
    #initialize method
    # parent: main class
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # defining a label OBJECT
        label = tk.Label(self, text="BomberBash!", font=LARGE_FONT)
        # add the label object to the container
        # padding x and y axis
        label.pack(pady=10, padx=10)

        # creating a button
        # Parameters: self, title, command/function
        # lambda : run command immediately
        button1 = tk.Button(self, text="Spiel starten", command=lambda: controller.show_frame(PageSettings))
        button1.pack()

        button2 = tk.Button(self, text="Credits", command=lambda: controller.show_frame(PageCredits))
        button2.pack()

        button3 = tk.Button(self, text="Spiel beenden", command=lambda: sys.exit(0))
        button3.pack()


# function for call more than one function after button click
# add to the button: command=combie_funcs(funtion1, function2)
def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)

    return combined_func

'''PageSettings class '''
class PageSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # defining a label OBJECT
        label = tk.Label(self, text="Einstellungen", font=LARGE_FONT)
        # add the label object to the container
        # padding x and y axis
        label.pack(pady=10, padx=10)

        labelNote = tk.Label(self, text="Not working yet. Default: 5x5", font=MEDIUM_FONT)
        labelNote.pack(pady=15, padx=10)

        # add vertical and horizontal slider
        verticalSlider = tk.Scale(self, from_=2, to=10, label="Spalten", length=200, tickinterval=1)
        verticalSlider.pack()
        horizontalSlider = tk.Scale(self, from_=2, to=10, label="Zeilen", length=200, tickinterval=1, orient='horizontal')
        horizontalSlider.pack()

        button1 = tk.Button(self, text="Go!", command=lambda: combine_funcs(controller.show_frame(PageGameStart)))
        button1.pack()

        button2 = tk.Button(self, text="zurück", command=lambda: controller.show_frame(PageMainMenu))
        button2.pack()

# initialisation of the button dictionary - MUST be set!
button = [[0 for x in range(999)] for x in range(999)]
lives = 5
highscore = 0

# function for checking the color of the buttons
def changeBtnColor(total, i,x):
    global lives
    global highscore

    event = button[i][x + 99]
    if(lives > 0):
        if(event == 'bomb'):
            highscore = highscore+1
            lives = lives - 2
            if(lives > 0):
                button[i][x].configure(bg="red", text='X')
                print(lives)
            else:
                print('#################')
                print('      DEAD')
                print('-----------------')
                print('Highscore: ' + str(highscore))
                print('#################')
                sys.exit(0)
        elif(event == 'nothing'):
            highscore = highscore + 1
            lives = lives - 1
            if (lives > 0):
                button[i][x].configure(bg="yellow", text='O')
                print(lives)
            else:
                print('#################')
                print('      DEAD')
                print('-----------------')
                print('Highscore: ' + str(highscore))
                print('#################')
                sys.exit(0)
        elif(event == 'bonus'):
            highscore = highscore + 1
            lives = lives + 1
            if (lives > 0):
                button[i][x].configure(bg="green", text='+')
                print(lives)
            else:
                print('#################')
                print('      DEAD')
                print('-----------------')
                print('Highscore: ' + str(highscore))
                print('#################')
                sys.exit(0)
        else:
            highscore = highscore + 1
            button[i][x].configure(bg="gray", text='T')
    else:
        print('DEAD')

'''PageGameStart class'''
class PageGameStart(tk.Frame):
    def showGrid(self, controller):
        global lives
        global rowValue
        global colValue

        rows = rowValue
        cols = colValue

        # defining a label OBJECT
        label = tk.Label(self, text="Züge: " + str(lives) + " - Cols: " + str(cols) + " Rows: " + str(rows),
                         font=LARGE_FONT)
        label.grid(row=0, column=0, sticky="s")

        total = rows * cols

        for i in range(cols):
            for x in range(rows):
                button[i][x] = tk.Button(self, text="", command=lambda i=i, x=x: changeBtnColor(total, i, x), bg="blue")
                button[i][x + 99] = random.choice(['bomb', 'nothing', 'bonus'])
                rowValue = i + 1
                colValue = x + 1
                button[i][x].grid(row=rowValue, column=colValue, sticky="n")

        # creating a button
        # Parameters: self, title, command/function
        # lambda : run command immediately
        buttonBackToMain = tk.Button(self, text="Hauptmenü", command=lambda: controller.show_frame(PageMainMenu))
        buttonBackToMain.grid(row=998, column=0, sticky="n")

        buttonExitGame = tk.Button(self, text="Beenden", command=lambda: sys.exit(0))
        buttonExitGame.grid(row=999, column=0, sticky="n")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.showGrid(controller)


'''PageCredits'''
class PageCredits(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Credits", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        labelText = tk.Label(self, text="BomberBash ist ein kleines Spiel\n"
                                    "in dem es darum geht, Bomben zu vermeiden\n"
                                    "und möglichst lange zu überleben.\n"
                                    "Versuche alle Felder aufzudecken.", font=MEDIUM_FONT)
        labelText.pack(pady=10, padx=10)

        labelCopyr = tk.Label(self, text="(c) 2016 - F.Petruschke", font=SMALL_FONT)
        labelCopyr.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="zurück", command=lambda: controller.show_frame(PageMainMenu))
        button1.pack()

# initialising the main function
app=BomberBash()
#setting icon and title
app.title("BomberBash!")
# DOES NOT WORK WITH .ICO ON LINUX:
#app.iconbitmap()
#app.wm_iconbitmap("/home/petrusp/PycharmProjects/gui/BomberBash/bomb.ico")
#app.iconbitmap(r'/home/petrusp/PycharmProjects/gui/BomberBash/bomb.ico')
# WORKAROUND (not really working)
#img = tk.Image("photo", file="bomb.png")
#app.tk.call('wm','iconphoto',app._w,img)
app.mainloop()