import json
import requests
import tkinter as tk
import tkinter.ttk as ttk
from constants import *

class MainApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Stats")

        self.entry = tk.Entry(self)
        self.entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        self.columnconfigure(0, minsize=150)
        self.columnconfigure(1, minsize=150)
        self.columnconfigure(2, minsize=150)
        self.columnconfigure(3, minsize=150)
        self.button = tk.Button(self, text="Submit", command=self.search)
        self.button.grid(row=0, column=2, padx=5, pady=5, sticky="we")

        options = ["Xbox One", "PS4", "Steam"]
        self.dropVar = tk.StringVar()
        self.dropVar.set("Xbox One")
        self.choice = tk.OptionMenu(self, self.dropVar, *options)
        self.choice.grid(row=0, column=0, padx=5, pady=5, sticky="we")

        self.label1 = tk.Label(self, text="Main Stats:")
        self.label1.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.label2 = tk.Label(self, text="Extended Stats:")
        self.label2.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        self.display = ttk.Treeview(self, columns=3, height=6)
        self.display['show'] = "headings"
        self.display["columns"] = ("1", "2", "3")
        self.display.heading("1", text="Stat Type", anchor="w")
        self.display.column("1", stretch="yes", anchor="w", width=125)
        self.display.heading("2", text="Value", anchor="w")
        self.display.column("2", stretch="yes", anchor="w", width=125)
        self.display.heading("3", text="%", anchor="w")
        self.display.column("3", stretch="yes", anchor="w", width=125)
        self.display.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nswe")

        self.display2 = ttk.Treeview(self, columns=2, height=6)
        self.display2['show'] = "headings"
        self.display2['columns'] = ("1", "2")
        self.display2.heading("1", text="Stat Type", anchor="w")
        self.display2.column("1", stretch="yes", anchor="w", width=125)
        self.display2.heading("2", text="Value", anchor="w")
        self.display2.column("2", stretch="yes", anchor="w", width=125)
        self.display2.grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky="we")

        self.label2 = tk.Label(self, text="Ranked:")
        self.label2.grid(row=6, column=0, padx=5, pady=5, sticky="w")

        self.display3 = ttk.Treeview(self, columns=4, height=3)
        self.display3['show'] = "headings"
        self.display3["columns"] = ("1", "2", "3", "4")
        self.display3.heading("1", text="Duel", anchor="c")
        self.display3.column("1", stretch="yes", anchor="c", width=125)
        self.display3.heading("2", text="Doubles", anchor="c")
        self.display3.column("2", stretch="yes", anchor="c", width=125)
        self.display3.heading("3", text="Solo Standard", anchor="c")
        self.display3.column("3", stretch="yes", anchor="c", width=125)
        self.display3.heading("4", text="Standard", anchor="c")
        self.display3.column("4", stretch="yes", anchor="c", width=125)
        self.display3.grid(row=7, columnspan=4, padx=5, pady=5, sticky="nswe")

    def search(self):
        platforms = {"Xbox One": 3, "PS4": 2, "Steam": 1}
        auth = {"Authorization": "authkey"}
        url = "https://api.rocketleaguestats.com/v1/player"
        data = {"unique_id": self.entry.get(), "platform_id": platforms[self.dropVar.get()]}
        r = requests.get(url, params=data, headers=auth)
        parsed = json.loads(r.text)
        print(parsed)
        self.insert(parsed)

    def insert(self, parsed):
        self.clear()

        total = 0
        for stat in parsed['stats'].keys():
            total = total + parsed['stats'][stat]
        for stat in parsed['stats'].keys():
            value = parsed['stats'][stat]
            value_pct = (value / total) * 100
            self.display.insert('', 'end', values=(str.title(stat), value, "%.2f" % value_pct))

        shot_pct = (parsed['stats']['goals'] / parsed['stats']['shots'])
        mvp_pct = (parsed['stats']['mvps'] / parsed['stats']['wins']) * 100
        self.display2.insert('', 'end', values=("Goals per Shot", "%.2f" % shot_pct))
        self.display2.insert('', 'end', values=("MVP Percentage", "%.2f" % mvp_pct))

        comp = []
        i = 0
        for playlist in parsed['rankedSeasons']['6'].keys():
            comp.append([])
            for value in parsed['rankedSeasons']['6'][playlist]:
                comp[i].append(parsed['rankedSeasons']['6'][playlist][value])
            i = i + 1

        data = []
        for i in range(4):
            data.append([])
            rank = "%s Div %d" % (ranks[comp[i][2]], comp[i][3])
            data[i].append(rank)
            data[i].append("%d MMR" % (comp[i][0]))
            data[i].append("%d Games" % (comp[i][1]))
        for i in range(3):
            self.display3.insert('', 'end', values=(data[0][i], data[1][i], data[2][i], data[3][i]))

    def clear(self):
        for item in self.display.get_children():
            self.display.delete(item)
        for item in self.display2.get_children():
            self.display2.delete(item)
        for item in self.display3.get_children():
            self.display3.delete(item)

    def run(self):
        self.mainloop()

if __name__ == '__main__':
    MainApp().run()
