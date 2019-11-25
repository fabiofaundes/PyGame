from tkinter import *

class App1:
    def exitP(self):
        self.wdg1.quit()

    def changeText(self):
        self.txt1['text'] = 'Surpresa'

    def __init__(self, master=None):
        self.wdg1 = Frame(master)
        self.wdg1.pack()        

        self.txt1 = Label(self.wdg1,text="Alo Mundo", width=20, height=3)
        self.txt1.pack()

        self.txt2 = Label(self.wdg1)
        self.txt2['text'] = 'Ola Turma'
        self.txt2['bg'] = 'green'        
        self.txt2.pack()

        self.btnExit = Button(self.wdg1)
        self.btnExit['text'] = 'Exit'
        self.btnExit['command'] = self.exitP
        self.btnExit['width'] = 40
        self.btnExit.pack()

        self.btnChangeText = Button(self.wdg1, text='Mudar Texto', command=self.changeText)
        self.btnChangeText.pack()

        self.canvas1 = Canvas(master, width=200, height=200, cursor='X_cursor',bd=5,bg='green')
        self.canvas1.pack()

        self.canvas1.create_line(10,10,10,100,100,100,10,10, fill='black')
        self.canvas1.create_line(10,10,190,10,190,190,10,190,10,10, fill='black')   
             

App.window.mainloop())

        