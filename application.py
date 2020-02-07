#!/usr/bin/python3
#
# This is the graphical user interface for the metadata extractor cli software.
# It is compliant with the cli software, although being awful because I didn't 
# care about the interface design.
#
# Rafael Campos Nunes <rafaelnunes@engineer.com>
#


import os
import sys
import subprocess
import platform

from tkinter import LEFT, RIGHT
from tkinter import N, W, E, S
from tkinter import Tk, filedialog, messagebox
from tkinter.ttk import Frame, Label, Entry, Button, Combobox


class Application:
    def __init__(self, master=None):
        self.config()

        self.main_window = Frame(master, padding="3 3 12 12")
        self.main_window['width'] = 350
        self.main_window.grid(column=0, row=0, sticky=(N, W, E, S))

        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        ############## INPUT ELEMENTS ################
        self.l_dir_input = Label(self.main_window)
        self.l_dir_input['text'] = 'Input directory'
        self.l_dir_input.grid(column=1, row=1, sticky=(E))

        self.e_input_dir = Entry(self.main_window)
        self.e_input_dir['width'] = 60
        self.e_input_dir.grid(column=2, row=1, sticky=(W, E))

        self.b_browse_input = Button(self.main_window)
        self.b_browse_input['text'] = 'Browse'
        self.b_browse_input.bind("<1>", lambda event,  e=self.e_input_dir:
                                 self.browse(event, e))
        self.b_browse_input.grid(column=2, row=2, sticky=E)

        ############## OUTPUT ELEMENTS ################
        self.l_dir_output = Label(self.main_window)
        self.l_dir_output['text'] = 'Output directory'
        self.l_dir_output.grid(column=1, row=3, sticky=(E))

        self.e_output_dir = Entry(self.main_window)
        self.e_output_dir['width'] = 60
        self.e_output_dir.grid(column=2, row=3, sticky=(W, E))

        self.b_browse_output = Button(self.main_window)
        self.b_browse_output['text'] = 'Browse'
        self.b_browse_output.bind("<1>", lambda event,  e=self.e_output_dir:
                                  self.browse(event, e))
        self.b_browse_output.grid(column=2, row=4, sticky=E)                                  

        ############## PARSER ELEMENTS ################
        self.l_parsers = Label(self.main_window)
        self.l_parsers['text'] = 'Select a parser'
        self.l_parsers.grid(column=1, row=5, sticky=(W))

        self.c_parsers = Combobox(self.main_window)
        self.c_parsers['values'] = self.parsers
        self.c_parsers['width'] = 60
        self.c_parsers.grid(column=2, row=5, sticky=(E))
        
        selected = 0
        if len(self.parsers) > 0:
            selected = len(self.parsers)-1

        self.c_parsers.current(selected)

        ############## BUTTON ELEMENTS ################
        self.button_container = Frame(self.main_window)
        self.button_container.grid(column=2, row=8, sticky=E)

        self.b_start = Button(self.button_container)
        self.b_start['text'] = "Start extraction"
        self.b_start['command'] = self.start
        self.b_start.pack(side=LEFT, padx='5')

        self.b_exit = Button(self.button_container)
        self.b_exit['text'] = "Exit"
        self.b_exit['command'] = self.exit
        self.b_exit.pack(side=RIGHT)

        for child in self.main_window.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def config(self):
        """
        Sets up common variables used within the GUI
        """
        if platform.system() == "Windows":
            self.python = 'python'
        else:
            self.python = 'python3'

        b = ''
        (_, _, filenames) = next(os.walk('.'))

        for filename in filenames:
            if filename == 'cli.py':
                b = os.path.abspath(filename)
                break

        self.binary = b
        self.parsers = []

        try:
            print(self.python, self.binary)
            r = subprocess.check_output([self.python, self.binary, '-lp'])
            # The output will always have a trailing element after split so I
            # might as well add the all option.
            self.parsers = r.decode(encoding='utf-8').split('\n')
            self.parsers[-1] = 'all'
        except subprocess.CalledProcessError as e:
            messagebox.showerror('Error', 'Couldn\'t configure the software.' +
                                 ' It will now autoterminate.')
            print(e)                        
            sys.exit(1)

    def start(self):
        """
        Init application with the parameters of the GUI
        """
        self.idir = self.e_input_dir.get()
        self.odir = self.e_output_dir.get()
        self.parser = self.c_parsers.get()

        r = subprocess.call([self.python, self.binary, '-d', self.idir,
                            '-p', self.parser, '-o', self.odir])

        if r == 0:
            messagebox.showinfo('Success', 'The extraction was a success')
        else:
            messagebox.showerror('Error', 'The extraction was not a success')

    def exit(self):
        sys.exit()

    def browse(self, event, element):
        """
        """
        folder = filedialog.askdirectory()
        element.insert(0, folder)


if __name__ == "__main__":
    root = Tk()
    root.title('Metadata Extractor')

    Application(master=root)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass