from tkinter import Tk, ttk, filedialog

from collocations.find_collocations import find_collocations
from preparation import preparation_stage


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("PyLingvo")
        self.minsize(640, 400)

        self.labelFrame = ttk.LabelFrame(self, text="Open Directory")
        self.labelFrame.grid(column=0, row=1, padx=20, pady=20)
        self.filename = None

        self.display_browse_button()


    def display_browse_button(self):
        self.browse_button = ttk.Button(self.labelFrame,
                                        text="Browse A Directory",
                                        command=self.file_dialog)
        self.browse_button.grid(column=1, row=1)

    def file_dialog(self):
        self.filename = filedialog.askdirectory(title="Select A File")
        self.label = ttk.Label(self.labelFrame, text="")
        self.label.grid(column=1, row=2)
        self.label.configure(text=self.filename)
        self.filename = preparation_stage(self.filename)
        self.collocations_button_click()

    def collocations_button_click(self):
        collocations = lambda: find_collocations(self.filename)
        self.collocations_button = ttk.Button(text='Get collocations',
                                              command=collocations)
        self.collocations_button.grid(column=14, row=14)


root = Root()
root.mainloop()
