from tkinter import Tk, ttk, filedialog, Text, END
from collocations.find_collocations import collocations_stage
from preparation import preparation_stage

FONT = '-*-lucidatypewriter-medium-r-*-*-*-140-*-*-*-*-*-*'


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("PyLingvo")
        self.minsize(640, 6)

        self.style = ttk.Style()
        self.style.configure('W.TLabelframe.Label',
                             font=(FONT, 20, 'bold'))
        self.style.configure('W.TButton', font=(FONT, 20, 'bold'))

        self.labelFrame = ttk.LabelFrame(self, text="Open Directory",
                                         style='W.TLabelframe')
        self.labelFrame.grid(column=0, row=1, padx=20, pady=20)
        self.filename = None
        self.dir_to_write = None

        self.display_browse_button()

    def display_browse_button(self):
        self.browse_button = ttk.Button(self.labelFrame,
                                        text="Browse A Directory",
                                        command=self.file_dialog,
                                        style='W.TButton')
        self.browse_button.grid(column=1, row=1)

    def read_file_dialog(self):
        self.filename = filedialog.askdirectory(title="Select A File")
        self.label = ttk.Label(self.labelFrame, text="",
                               style='W.TLabelframe.Label')
        self.label.grid(column=1, row=2)
        self.label.configure(text=self.filename)
        self.filename = preparation_stage(self.filename)
        self.result_field = Text(self, height=5, width=50)
        self.result_field.grid(row=8, column=3, columnspan=6)
        self.display_collocations_button()

    def write_file_dialog(self):
        self.dir_to_write = None
        # implement as below, think about logic

    def collocations(self):
        text_to_show = collocations_stage(self.filename, )
        self.result_field.insert(END, 'Collocations found: \n')
        self.result_field.insert(END, text_to_show + '\n')

    def display_collocations_button(self):
        self.collocations_button = ttk.Button(text='Get collocations',
                                              command=self.collocations,
                                              style='W.TButton')
        self.collocations_button.grid(column=0, row=15, padx=5, pady=10)


root = Root()
root.mainloop()
