from ui.showData import *
from ui.addBook import *
from ui.sellBook import *
from ui.analysisBook import *
from ui.visualization import *

class BookGui:
    def __init__(self,root):
        self.root = root
        self.root.title("Book Store Management System")
        self.root.geometry("900x700")
        self.root.configure(bg="#1f3c68")

        create_tables()

        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Times New Roman", 16, "bold"), padding=[8, 5])
        style.map("TNotebook.Tab",
                  background=[('selected', '#2980b9')],
                  foreground=[('selected', 'black')])

        self.tab_control = ttk.Notebook(root)

        self.add_book_tab = AddBook(self.tab_control)
        self.sell_book_tab = SellBook(self.tab_control)
        self.analysis_tab = Analysis(self.tab_control)
        self.show_data_tab = ShowData(self.tab_control)
        self.visualizations_tab = Visualization(self.tab_control)

        self.tab_control.add(self.add_book_tab.get_frame(), text="Add Book")
        self.tab_control.add(self.sell_book_tab.get_frame(), text="Sell Book")
        self.tab_control.add(self.analysis_tab.get_frame(), text="Analysis")
        self.tab_control.add(self.show_data_tab.get_frame(), text="Show Data")
        self.tab_control.add(self.visualizations_tab.get_frame(), text="Visualizations")

        self.tab_control.pack(expand=1, fill="both")