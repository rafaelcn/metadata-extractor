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

from tkinter import Button, Frame, Entry, Label, Tk
from tkinter import filedialog, messagebox
from tkinter import LEFT, RIGHT
from tkinter import N, W, E, S
from tkinter.ttk import Combobox


class Application:
    def __init__(self, master=None):
        self.config()

        self.main_window = Frame(master)
        self.main_window['width'] = 350
        self.main_window.grid(column=0, row=0, sticky=(N, W, E, S))
        self.main_window.pack()

        ############## INPUT ELEMENTS ################
        self.input_elements = Frame(master)
        self.input_elements['pady'] = 20
        self.input_elements['padx'] = 20
        self.input_elements.pack()

        self.l_dir = Label(self.input_elements)
        self.l_dir['text'] = 'Input directory'
        self.l_dir.pack(side=LEFT)

        self.e_input_dir = Entry(self.input_elements)
        self.e_input_dir['width'] = 60
        self.e_input_dir.pack()

        self.b_browse_input = Button(self.input_elements)
        self.b_browse_input['text'] = 'Browse'
        self.b_browse_input.bind("<1>", lambda event,  e=self.e_input_dir:
                                 self.browse(event, e))
        self.b_browse_input.pack(side=RIGHT)

        ############## OUTPUT ELEMENTS ################
        self.output_elements = Frame(master)
        self.output_elements['pady'] = 20
        self.output_elements['padx'] = 20
        self.output_elements.pack()

        self.l_dir = Label(self.output_elements)
        self.l_dir['text'] = 'Output directory'
        self.l_dir.pack(side=LEFT)

        self.e_output_dir = Entry(self.output_elements)
        self.e_output_dir['width'] = 60
        self.e_output_dir.pack()

        self.b_browse_output = Button(self.output_elements)
        self.b_browse_output['text'] = 'Browse'
        self.b_browse_output.bind("<1>", lambda event,  e=self.e_output_dir:
                                  self.browse(event, e))
        self.b_browse_output.pack(side=RIGHT)

        ############## PARSER ELEMENTS ################
        self.parsers_container = Frame(master)
        self.parsers_container.pack()

        self.l_parsers = Label(self.parsers_container)
        self.l_parsers['text'] = 'Select a parser'
        self.l_parsers['padx'] = 10
        self.l_parsers.pack(side=LEFT)

        self.c_parsers = Combobox(self.parsers_container)
        self.c_parsers['values'] = self.parsers
        
        selected = 0
        if len(self.parsers) > 0:
            selected = len(self.parsers)-1

        self.c_parsers.current(selected)
        self.c_parsers.pack(side=RIGHT)

        ############## BUTTON ELEMENTS ################
        self.button_container = Frame(master)
        self.button_container['pady'] = 20
        self.button_container['padx'] = 20
        self.button_container.pack()

        self.b_start = Button(self.button_container)
        self.b_start['text'] = "Start extraction"
        self.b_start['width'] = 15
        self.b_start['command'] = self.start
        self.b_start.pack(side=LEFT)

        self.b_exit = Button(self.button_container)
        self.b_exit['text'] = "Exit"
        self.b_exit['width'] = 15
        self.b_exit['command'] = self.exit
        self.b_exit.pack(side=RIGHT)

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
    Application(master=root)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass