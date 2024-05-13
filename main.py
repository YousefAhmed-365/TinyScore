import tkinter as tk

from tkinter import ttk
from tkinter import messagebox

class TinyScore:
    def __init__(self):
        self.init_default_layout()
        
    def init_default_layout(self):
        # Init window
        self.root = tk.Tk()
        self.root.title("TinyScore")
        self.root.geometry()
        self.root.resizable(False, False)

        img = tk.PhotoImage(file='assets/Logo.png')
        self.root.iconphoto(False, img)

        # Init default layout
        style = ttk.Style()
        style.theme_use("clam")

        self.left_frame = ttk.Frame(self.root, width = 700)
        self.left_frame.pack_propagate(False)
        self.left_frame.columnconfigure((0, 1, 2, 3), weight = 1, uniform = "a")
        self.left_frame.rowconfigure(0, weight = 3, uniform = "a")
        self.left_frame.rowconfigure(1, weight = 1, uniform = "a")

        self.main_table_frame = ttk.Frame(self.left_frame)
        self.main_control_frame = ttk.Frame(self.left_frame)
        self.main_control_frame.grid_propagate(False)
        self.main_control_frame.columnconfigure((0, 1, 2, 3), weight = 1, uniform = "a")
        self.main_control_frame.rowconfigure((0, 1), weight = 1, uniform = "a")

        self.main_table = ttk.Treeview(self.main_table_frame, columns = ["name", "score"], show = "headings", selectmode = "browse")
        self.main_table.heading("name", text = "Name")
        self.main_table.heading("score", text = "Score")

        self.name_inp_label = ttk.Label(self.main_control_frame, text = "Name")
        self.name_inp = ttk.Entry(self.main_control_frame)
        self.add_name_btn = ttk.Button(self.main_control_frame, text = "ADD")

        self.score_inp_label = ttk.Label(self.main_control_frame, text = "Score")
        self.score_inp = ttk.Entry(self.main_control_frame)
        self.add_score_btn = ttk.Button(self.main_control_frame, text = "ADD")
        self.del_entry_btn = ttk.Button(self.main_control_frame, text = "DEL")

        self.right_frame = ttk.Frame(self.root, width = 100)
        self.right_frame.pack_propagate(False)

        self.rank_btn = ttk.Button(self.right_frame, text = "Rank")

        # Events Binding
        self.add_name_btn.configure(command = self.add_entry)
        self.add_score_btn.configure(command = self.inc_entry)
        self.del_entry_btn.configure(command = self.del_entry)

        self.rank_btn.configure(command = self.calc_rank)
        
        # Pack components
        self.left_frame.grid(row = 0, column = 0, sticky = "ns")
        self.right_frame.grid(row = 0, column = 1, sticky = "ns")
        self.main_table_frame.grid(row = 0, column = 0, columnspan = 4, sticky = "news", padx = 5, pady = (5, 0))
        self.main_control_frame.grid(row = 1, column = 0, columnspan = 4, sticky = "news", padx = 5, pady = (0, 5))

        self.name_inp_label.grid(row = 0, column = 0, pady = (5, 0))
        self.name_inp.grid(row = 0, column = 1, columnspan = 2, pady = (5, 0), sticky = "news")
        self.add_name_btn.grid(row = 0, column = 3, pady = (5, 0))

        self.score_inp_label.grid(row = 1, pady = (5, 0), column = 0)
        self.score_inp.grid(row = 1, column = 1, pady = (5, 0), sticky = "news")
        self.add_score_btn.grid(row = 1, pady = (5, 0), column = 2)
        self.del_entry_btn.grid(row = 1, pady = (5, 0), column = 3)

        self.main_table.grid(row = 0, column = 0, sticky = "news")
        
        self.rank_btn.pack(padx = (0, 5), pady = 5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_app_closing)

        self.root.mainloop()
    
    def on_app_closing(self):
        if messagebox.askyesno("Exit", "Do you want to exit TinyScore?"):
            self.root.destroy()
        else:
            pass

    def add_entry(self):
        inp = self.name_inp.get()
        isExists = False

        if len(inp) > 0:
            for item in self.main_table.get_children():
                if self.main_table.item(item)["values"][0] == inp:
                    isExists = True
                    break
            if isExists:
                messagebox.showerror("Name Error", f"\'{inp}\' already exists")
            else:
                self.main_table.insert(parent = "", index = tk.END, values = (inp, 0))

        else:
            messagebox.showerror("Name Error", "Name can't be empty")

    def del_entry(self):
        selected_item = self.main_table.focus()
        if len(selected_item) > 0:
            self.main_table.delete(selected_item)
        else:
            messagebox.showerror("Deletion Error", "Select item to delete")

    def inc_entry(self):
        selected_item = self.main_table.focus()
        if len(selected_item) > 0:
            inc_num = self.score_inp.get()
            if inc_num.isnumeric():
                self.main_table.item(selected_item, values = (self.main_table.item(selected_item)["values"][0], int(self.main_table.item(selected_item)["values"][1]) + int(inc_num)))
            else:
                messagebox.showerror("Score Error", "Invalid score")
        else:
            messagebox.showerror("Score Error", "Select item to add score to")
    
    def calc_rank(self):
        itemsIDs = self.main_table.get_children()
        if len(itemsIDs) == 0:
            messagebox.showerror("Rank Error", "The table is empty")
            return
        
        items = []
        
        for item in itemsIDs:
            items.append(self.main_table.item(item)["values"])
        
        items = sorted(items, key = lambda x: x[1], reverse = True)

        rank_text = ""
        counter = 1
        for item in items:
            rank_text += f"#{counter} {item[0]} : {item[1]}\n"
            counter += 1
        
        messagebox.showinfo("Rank", rank_text)

if __name__ == "__main__":
    app = TinyScore()