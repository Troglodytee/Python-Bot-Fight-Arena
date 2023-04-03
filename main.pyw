from tkinter import Button, Canvas, Entry, Frame, Label, Listbox, Scale, Tk
from tkinter.messagebox import showerror
from importlib.util import spec_from_file_location, module_from_spec
from sys import argv as PATH, modules as MODULES
from os import listdir
from random import randint


PATH = PATH[0][:-8]
FONT = "Consolas 10"
RULES = [
    ("GridWidth", 10, int),
    ("GridHeight", 10, int),
    ("StartHp", 3, int),
    ("MaxHp", 3, int),
    ("StartDamages", 1, int),
    ("MaxDamages", 1, int),
    ("FaceDamages", 0, float),
    ("SideDamages", 0.5, float),
    ("BackDamages", 1, float),
    ("NRotations", 1, int),
    ("NMoves", 1, int),
    ("NAttacks", 1, int),
]
CANVAS_COLUMSPAN = 5
LISTBOXES_ROWSPAN = 6
LISTBOXES_HEIGHT = 20


class Window:
    def __init__(self):
        self.__last_cell = [None, None]
        self.__window = Tk()
        self.__window.title("Bots Arena")
        frame = Frame(
            self.__window,
            borderwidth=0,
        )
        frame.grid(
            row=0,
            column=0,
            rowspan=2,
            sticky="nw",
        )
        self.__canvas = Canvas(
            frame,
            width=501,
            height=501,
            bg="white",
        )
        self.__canvas.grid(
            row=0,
            column=0,
            columnspan=CANVAS_COLUMSPAN,
            sticky="nw",
        )
        self.__canvas.bind("<Button-1>", self.__change_wall)
        self.__canvas.bind("<B1-Motion>", self.__change_wall)
        self.__button_start = Button(
            frame,
            text="Start / End",
            font=FONT,
            command=self.__start,
        )
        self.__button_start.grid(
            row=1,
            column=0,
            sticky="nw",
        )
        self.__button_start = Button(
            frame,
            text="Pause / Resume",
            font=FONT,
            command=self.__pause,
        )
        self.__button_start.grid(
            row=1,
            column=1,
            sticky="nw",
        )
        self.__button_start = Button(
            frame,
            text="Clear logs",
            font=FONT,
            command=self.__clear_logs,
        )
        self.__button_start.grid(
            row=1,
            column=2,
            sticky="nw",
        )
        self.__scale_fps = Scale(
            frame,
            orient="horizontal",
            from_=1,
            to=144,
            resolution=1,
            length=144,
            showvalue=False,
            command=self.__change_fps,
        )
        self.__scale_fps.grid(
            row=1,
            column=3,
            sticky="nw",
        )
        self.__label_fps = Label(
            frame,
            text="FPS = ?",
            font=FONT,
        )
        self.__label_fps.grid(
            row=1,
            column=4,
            sticky="nw",
        )
        self.__logs = Listbox(
            frame,
            height=10,
            font=FONT,
        )
        self.__logs.grid(
            row=2,
            column=0,
            columnspan=CANVAS_COLUMSPAN,
            sticky="we",
        )
        frame = Frame(
            self.__window,
            borderwidth=0,
        )
        frame.grid(
            row=0,
            column=1,
            sticky="nw",
        )
        Label(
            frame,
            text="Active bots :",
            font=FONT,
        ).grid(
            row=0,
            column=0,
            sticky="n",
        )
        self.__listbox_active_bots = Listbox(
            frame,
            width=30,
            height=LISTBOXES_HEIGHT,
            font=FONT,
        )
        self.__listbox_active_bots.grid(
            row=1,
            column=0,
            rowspan=LISTBOXES_ROWSPAN,
            sticky="nw",
        )
        Button(
            frame,
            text=" < ",
            font=FONT,
            command=self.__add_bot,
        ).grid(
            row=1,
            column=1,
            sticky="nsew",
        )
        Button(
            frame,
            text=" << ",
            font=FONT,
            command=self.__add_all_bots,
        ).grid(
            row=2,
            column=1,
            sticky="nsew",
        )
        Button(
            frame,
            text=" > ",
            font=FONT,
            command=self.__del_bot,
        ).grid(
            row=3,
            column=1,
            sticky="nsew",
        )
        Button(
            frame,
            text=" >> ",
            font=FONT,
            command=self.__del_all_bots,
        ).grid(
            row=4,
            column=1,
            sticky="nsew",
        )
        Button(
            frame,
            text=" ^ ",
            font=FONT,
            command=self.__bot_up,
        ).grid(
            row=5,
            column=1,
            sticky="nsew",
        )
        Button(
            frame,
            text=" v ",
            font=FONT,
            command=self.__bot_down,
        ).grid(
            row=6,
            column=1,
            sticky="nsew",
        )
        Label(
            frame,
            text="All bots :",
            font=FONT,
        ).grid(
            row=0,
            column=2,
            sticky="n",
        )
        self.__listbox_all_bots = Listbox(
            frame,
            width=30,
            height=LISTBOXES_HEIGHT,
            font=FONT,
        )
        self.__listbox_all_bots.grid(
            row=1,
            column=2,
            rowspan=LISTBOXES_ROWSPAN,
            sticky="nw",
        )
        Button(
            frame,
            text="Refresh",
            font=FONT,
            command=self.__refresh_bots,
        ).grid(
            row=LISTBOXES_ROWSPAN+1,
            column=2,
            sticky="nw",
        )
        frame = Frame(
            self.__window,
            borderwidth=0,
        )
        frame.grid(
            row=1,
            column=1,
            sticky="nw",
        )
        self.__entries = []
        n_lines = int(len(RULES)/2+0.5)
        for i in range(len(RULES)):
            label = ""
            for j in RULES[i][0]:
                if 65 <= ord(j) <= 90:
                    label += " "
                label += j
            Label(
                frame,
                text=label[1:]+" :",
                font=FONT,
            ).grid(
                row=i%n_lines*2,
                column=i//n_lines,
                sticky="nw",
            )
            self.__entries += [Entry(
                frame,
                width=30,
                font=FONT,
            )]
            self.__entries[-1].insert(
                0,
                str(RULES[i][1])
            )
            self.__entries[-1].grid(
                row=i%n_lines*2+1,
                column=i//n_lines,
                sticky="nw",
            )
        self.__button_update_rules = Button(
            frame,
            text="Update",
            font=FONT,
            command=self.__update_rules,
        )
        self.__button_update_rules.grid(
            row=n_lines*2,
            column=0,
            sticky="nw",
        )
        self.__refresh_bots()
        self.__arena = Arena(self)
        self.__window.mainloop()

    def get_canvas(self):
        return self.__canvas

    def get_canvas_width(self):
        return int(self.__canvas["width"])

    def get_canvas_height(self):
        return int(self.__canvas["height"])

    def __change_wall(self, event):
        if not self.__arena.is_running():
            size = self.__arena.get_cell_size()
            x = int(event.x/size)
            y = int(event.y/size)
            if not (x == self.__last_cell[0] and y == self.__last_cell[1]):
                self.__last_cell[0] = x
                self.__last_cell[1] = y
                self.__arena.change_wall(x, y)

    def __add_bot(self):
        if self.__arena.is_running():
            showerror("Error", "Can't do that while running.")
        else:
            i = self.__listbox_all_bots.curselection()
            if i != ():
                name = self.__listbox_all_bots.get(i[0])
                self.__arena.add_bot(name)
                self.__listbox_all_bots.delete(i[0])
                self.__listbox_active_bots.insert("end", name)


    def __add_all_bots(self):
        if self.__arena.is_running():
            showerror("Error", "Can't do that while running.")
        else:
            for i in range(self.__listbox_all_bots.size()):
                name = self.__listbox_all_bots.get(0)
                self.__arena.add_bot(name)
                self.__listbox_all_bots.delete(0)
                self.__listbox_active_bots.insert("end", name)

    def __del_bot(self):
        if self.__arena.is_running():
            showerror("Error", "Can't do that while running.")
        else:
            i = self.__listbox_active_bots.curselection()
            if i != ():
                name = self.__listbox_active_bots.get(i[0])
                self.__arena.del_bot(name)
                self.__listbox_active_bots.delete(i[0])
                self.__listbox_all_bots.insert("end", name)

    def __del_all_bots(self):
        if self.__arena.is_running():
            showerror("Error", "Can't do that while running.")
        else:
            for i in range(self.__listbox_active_bots.size()):
                name = self.__listbox_active_bots.get(0)
                self.__arena.del_bot(name)
                self.__listbox_active_bots.delete(0)
                self.__listbox_all_bots.insert("end", name)

    def __bot_up(self):
        if self.__arena.is_running():
            showerror("Error", "Can't do that while running.")
        else:
            i = self.__listbox_active_bots.curselection()
            if i != () and i[0] > 0:
                name = self.__listbox_active_bots.get(i[0])
                self.__listbox_active_bots.delete(i[0])
                self.__listbox_active_bots.insert(i[0]-1, name)
                self.__arena.bot_up(i[0])

    def __bot_down(self):
        if self.__arena.is_running():
            showerror("Error", "Can't do that while running.")
        else:
            i = self.__listbox_active_bots.curselection()
            if i != () and i[0] < self.__listbox_active_bots.size()-1:
                name = self.__listbox_active_bots.get(i[0])
                self.__listbox_active_bots.delete(i[0])
                self.__listbox_active_bots.insert(i[0]+1, name)
                self.__arena.bot_down(i[0])

    def __refresh_bots(self):
        self.__listbox_all_bots.delete(0, "end")
        for i in listdir(f"{PATH}Bots"):
            if i[-3:] == ".py":
                name = i[:-3]
                valid = True
                for j in range(self.__listbox_active_bots.size()):
                    if self.__listbox_active_bots.get(j) == name:
                        valid = False
                        break
                if valid:
                    self.__listbox_all_bots.insert("end", name)

    def __update_rules(self):
        if self.__arena.is_running():
            showerror("Error", "Can't do that while running.")
        else:
            for i in range(len(RULES)):
                valid = True
                try:
                    value = RULES[i][2](self.__entries[i].get())
                    if value < 0:
                        valid = False
                    else:
                        self.__arena.set_rule(RULES[i][0], value)
                except:
                    valid = False
                if not valid:
                    showerror("Error", f"'{RULES[i][0]}' have an invalid value.")
                    break
            self.__last_cell[0] = None
            self.__last_cell[1] = None
            self.__arena.resize()

    def __change_fps(self, event):
        fps = self.__scale_fps.get()
        self.__label_fps["text"] = f"FPS = {fps}"
        self.__arena.change_fps(fps)

    def __start(self):
        self.__arena.start()

    def __pause(self):
        self.__arena.pause()

    def __clear_logs(self):
        self.__logs.delete(0, "end")

    def add_logs(self, text):
        self.__logs.insert("end", text)
        if self.__logs.size() > 500:
            self.__logs.delete(0)


class Arena:
    def __init__(self, parent):
        self.__parent = parent
        self.__rules = {}
        for i in RULES:
            self.__rules[i[0]] = i[1]
        self.__grid = []
        self.__bots = []
        self.__cell_size = 0
        self.__delay = 1000
        self.__is_running = 0
        self.__pause = 0
        self.resize()

    def is_running(self):
        return self.__is_running

    def get_rule(self, rule):
        if rule in self.__rules:
            return self.__rules[rule]

    def set_rule(self, rule, value):
        if rule in self.__rules:
            self.__rules[rule] = value

    def get_cell_size(self):
        return self.__cell_size

    def resize(self):
        width = self.get_rule("GridWidth")
        height = self.get_rule("GridHeight")
        for i in self.__grid:
            del i[:]
        del self.__grid[:]
        self.__grid = [[[1, None] for x in range(width)] for y in range(height)]
        self.__clear_bots()
        self.__cell_size = min(
            self.__parent.get_canvas_width()//self.get_rule("GridWidth"),
            self.__parent.get_canvas_height()//self.get_rule("GridHeight"),
        )
        self.__display_grid()

    def change_wall(self, x, y):
        if 0 <= x < self.get_rule("GridWidth") and 0 <= y < self.get_rule("GridHeight"):
            self.__grid[y][x][0] = 1-self.__grid[y][x][0]
            if self.__grid[y][x][0]:
                self.__clear_wall(x, y)
            else:
                self.__display_wall(x, y)

    def __clear_wall(self, x, y):
        if self.__grid[y][x][1] != None:
            self.__parent.get_canvas().delete(self.__grid[y][x][1])
            self.__grid[y][x][1] = None

    def __display_wall(self, x, y):
        canvas = self.__parent.get_canvas()
        self.__clear_wall(x, y)
        self.__grid[y][x][1] = canvas.create_rectangle(
            self.__cell_size*x+2,
            self.__cell_size*y+2,
            self.__cell_size*(x+1)+2,
            self.__cell_size*(y+1)+2,
            fill="black",
            width=0,
        )

    def add_bot(self, name):
        spec = spec_from_file_location(name, f"{PATH}Bots\\{name}.py")
        module = module_from_spec(spec)
        MODULES[name] = module
        spec.loader.exec_module(module)
        self.__bots += [{
            "Bot" : module.Bot(),
            "DisplayId" : None,
            "Attributs" : {},
            "Module" : module,
            "Name" : name,
        }]

    def del_bot(self, name):
        for i in range(len(self.__bots)):
            if self.__bots[i]["Name"] == name:
                module = self.__bots[i]["Module"]
                del module
                self.__bots[i]["Attributs"].clear()
                self.__bots[i].clear()
                del self.__bots[i]
                break

    def bot_up(self, i):
        self.__bots[i-1], self.__bots[i] = self.__bots[i], self.__bots[i-1]

    def bot_down(self, i):
        self.__bots[i], self.__bots[i+1] = self.__bots[i+1], self.__bots[i]

    def __clear_bots(self):
        canvas = self.__parent.get_canvas()
        for i in self.__bots:
            if i["DisplayId"] != None:
                canvas.delete(i["DisplayId"])
                i["DisplayId"] = None

    def __display_bot(self, i):
        canvas = self.__parent.get_canvas()
        if self.__bots[i]["DisplayId"] != None:
            canvas.delete(self.__bots[i]["DisplayId"])
        orientation = self.__bots[i]["Attributs"]["Orientation"]
        x = self.__cell_size*self.__bots[i]["Attributs"]["X"]+2
        y = self.__cell_size*self.__bots[i]["Attributs"]["Y"]+2
        if orientation == 0:
            self.__bots[i]["DisplayId"] = canvas.create_polygon(
                x+self.__cell_size/2,
                y+self.__cell_size/10,
                x+self.__cell_size*0.8,
                y+self.__cell_size*0.9,
                x+self.__cell_size/5,
                y+self.__cell_size*0.9,
                fill="blue",
                width=0,
            )
        elif orientation == 1:
            self.__bots[i]["DisplayId"] = canvas.create_polygon(
                x+self.__cell_size/10,
                y+self.__cell_size/5,
                x+self.__cell_size*0.9,
                y+self.__cell_size/2,
                x+self.__cell_size/10,
                y+self.__cell_size*0.8,
                fill="blue",
                width=0,
            )
        elif orientation == 2:
            self.__bots[i]["DisplayId"] = canvas.create_polygon(
                x+self.__cell_size/5,
                y+self.__cell_size/10,
                x+self.__cell_size*0.8,
                y+self.__cell_size/10,
                x+self.__cell_size/2,
                y+self.__cell_size*0.9,
                fill="blue",
                width=0,
            )
        else:
            self.__bots[i]["DisplayId"] = canvas.create_polygon(
                x+self.__cell_size/10,
                y+self.__cell_size/2,
                x+self.__cell_size*0.9,
                y+self.__cell_size/5,
                x+self.__cell_size*0.9,
                y+self.__cell_size*0.8,
                fill="blue",
                width=0,
            )

    def __display_grid(self):
        canvas = self.__parent.get_canvas()
        canvas.delete("all")
        width = self.get_rule("GridWidth")
        height = self.get_rule("GridHeight")
        for i in range(width+1):
            canvas.create_line(
                self.__cell_size*i+2,
                2,
                self.__cell_size*i+2,
                self.__cell_size*height+3,
                fill="black",
            )
        for i in range(height+1):
            canvas.create_line(
                2,
                self.__cell_size*i+2,
                self.__cell_size*width+2,
                self.__cell_size*i+2,
                fill="black",
            )

    def change_fps(self, fps):
        self.__delay = 1000//fps

    def __end(self):
        self.__is_running = 0
        self.__clear_bots()

    def start(self):
        if self.__is_running:
            self.__end()
        elif len(self.__bots) < 2:
            showerror("Error", "Not enought bots.")
        else:
            positions = []
            for y in range(self.get_rule("GridWidth")):
                for x in range(self.get_rule("GridHeight")):
                    if self.__grid[y][x][0]:
                        positions += [(x, y)]
            if len(positions) < len(self.__bots):
                showerror("Error", "Not enough positions available to place all the bots.")
            else:
                arena_infos = {
                    "Width" : self.get_rule("GridWidth"),
                    "Height" : self.get_rule("GridHeight"),
                    "FaceDamages" : self.get_rule("FaceDamages"),
                    "SideDamages" : self.get_rule("SideDamages"),
                    "BackDamages" : self.get_rule("BackDamages"),
                    "NRotations" : self.get_rule("NRotations"),
                    "NMoves" : self.get_rule("NMoves"),
                    "NAttacks" : self.get_rule("NAttacks"),
                    "MaxHp" : self.get_rule("MaxHp"),
                    "MaxDamages" : self.get_rule("MaxDamages"),
                    "Grid" : [[x[0] for x in y] for y in self.__grid],
                }
                for i in self.__bots:
                    i["Attributs"].clear()
                    j = randint(0, len(positions)-1)
                    i["Attributs"]["X"] = positions[j][0]
                    i["Attributs"]["Y"] = positions[j][1]
                    i["Attributs"]["Orientation"] = randint(0, 3)
                    i["Attributs"]["Hp"] = self.get_rule("StartHp")
                    i["Attributs"]["Damages"] = self.get_rule("StartDamages")
                    del positions[j]
                    i["Bot"].init(arena_infos, i["Attributs"])
                self.__is_running = 1
                self.__run()

    def __run(self):
        if self.__is_running and not self.__pause:
            canvas = self.__parent.get_canvas()
            l = []
            for i in self.__bots:
                if i["Attributs"]["Hp"] > 0:
                    l += [i["Name"]]
            if len(l) < 2:
                if len(l) == 0:
                    self.__parent.add_logs("Draw")
                else:
                    self.__parent.add_logs(l[0]+" wins the fight")
                self.__end()
            else:
                l = []
                for i in self.__bots:
                    l += [i["Attributs"]]
                multiplicators = [
                    self.get_rule("FaceDamages"),
                    self.get_rule("SideDamages"),
                    self.get_rule("BackDamages"),
                ]
                for i in range(len(self.__bots)):
                    a = self.__bots[i]["Attributs"]
                    try:
                        commands = self.__bots[i]["Bot"].run(a, l[:i]+l[i+1:]).upper()
                        name = self.__bots[i]["Name"]
                        if commands == None:
                            self.__parent.add_logs(name+" do nothing")
                        else:
                            n_actions = [
                                self.get_rule("NRotations"),
                                self.get_rule("NMoves"),
                                self.get_rule("NAttacks"),
                            ]
                            width = self.get_rule("GridWidth")
                            height = self.get_rule("GridHeight")
                            self.__parent.add_logs(f"{name} : '{commands}'")
                            for j in commands.split(";"):
                                line = j.split(" ")
                                if len(line) > 0 and line[0] != "":
                                    if line[0] == "LEFT":
                                        if n_actions[0] > 0:
                                            a["Orientation"] = (a["Orientation"]-1)%4
                                            n_actions[0] -= 1
                                            self.__parent.add_logs(name+" turn left")
                                        else:
                                            self.__parent.add_logs(name+" try to do a rotation but can no longer at this turn")
                                    elif line[0] == "RIGHT":
                                        if n_actions[0] > 0:
                                            a["Orientation"] = (a["Orientation"]-1)%4
                                            n_actions[0] -= 1
                                            self.__parent.add_logs(name+" turn right")
                                        else:
                                            self.__parent.add_logs(name+" try to do a rotation but can no longer at this turn")
                                    elif line[0] == "FORWARD":
                                        if n_actions[1] > 0:
                                            moves = ((0, -1), (1, 0), (0, 1), (-1, 0))[a["Orientation"]]
                                            new_x = a["X"]+moves[0]
                                            new_y = a["Y"]+moves[1]
                                            if 0 <= new_x < width and 0 <= new_y < height:
                                                if self.__grid[new_y][new_x][0]:
                                                    valid = True
                                                    for k in self.__bots:
                                                        if k["Attributs"]["X"] == new_x and k["Attributs"]["Y"] == new_y:
                                                            valid = False
                                                            break
                                                    if valid:
                                                        a["X"] = new_x
                                                        a["Y"] = new_y
                                                        n_actions[1] -= 1
                                                        self.__parent.add_logs(name+" move forward")
                                                    else:
                                                        self.__parent.add_logs(name+" try to move on an occuped cell")
                                                else:
                                                    self.__parent.add_logs(name+" try to move in a wall")
                                            else:
                                                self.__parent.add_logs(name+" try to move out of the grid")
                                        else:
                                            self.__parent.add_logs(name+" try to move but can no longer at this turn")
                                    elif line[0] == "ATTACK":
                                        if n_actions[2] > 0:
                                            moves = ((0, -1), (1, 0), (0, 1), (-1, 0))[a["Orientation"]]
                                            x = a["X"]+moves[0]
                                            y = a["Y"]+moves[1]
                                            for k in self.__bots:
                                                if k["Name"] != name and k["Attributs"]["X"] == x and k["Attributs"]["Y"] == y:
                                                    if k["Attributs"]["Orientation"] == a["Orientation"]:
                                                        m = multiplicators[2]
                                                    elif k["Attributs"]["Orientation"]+2 == a["Orientation"] or k["Attributs"]["Orientation"]-2 == a["Orientation"]:
                                                        m = multiplicators[0]
                                                    else:
                                                        m = multiplicators[1]
                                                    damages = a["Damages"]*m
                                                    k["Attributs"]["Hp"] -= damages
                                                    self.__parent.add_logs(f"{name} attack {k['Name']} and deal {damages} damages")
                                                    if k['Attributs']['Hp'] > 0:
                                                        self.__parent.add_logs(f"{k['Name']} has now {k['Attributs']['Hp']} Hp")
                                                    elif k["DisplayId"] != None:
                                                        canvas.delete(k["DisplayId"])
                                            n_actions[2] -= 1
                                        else:
                                            self.__parent.add_logs(name+" try to attack but can no longer at this turn")
                                    else:
                                        self.__parent.add_logs(name+" used an unknow command")
                                self.__display_bot(i)
                    except:
                        self.__parent.add_logs(name+" encountered an error")
                canvas.after(self.__delay, self.__run)

    def pause(self):
        if self.__is_running:
            self.__pause = 1-self.__pause
            if not self.__pause:
                self.__run()


window = Window()
