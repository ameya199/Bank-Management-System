from tkinter import ttk
import tkinter as tk
import db_con
from tkinter import messagebox
from fileinput import filename
from tkinter import Entry
from tkinter import filedialog as fd




def add_records():
    separate_lines(f, True)


def display_file():
    global f
    separate_lines(f, False)


def validate_file(new_file):
    global f, file_open
    #canvas.delete("all")
    temp = new_file.split('.')
    temp1 = temp.pop()
    #print(temp1)
    if temp1 == "":
        pass
    elif temp1 != "psv":
        messagebox.showwarning("Warning", "Please Select a psv file")
        return False
    else:
        f = open_file(new_file)
        file_open = True
        var = False
        lines = 0
        while True:
            s2 = f.readline()
            if not s2:
                break
            if s2 == "\n":
                continue
            if "|" not in s2:
                continue
            else:
                l = s2.split('|')
                if lines == 0:
                    no_of_feilds = len(l)
                    lines += 1
                else:
                    if no_of_feilds == len(l):
                        lines += 1
                        var = True
                        continue
                    else:
                        var = False
                        messagebox.showwarning("Warning", "Not a valid file")

                        break
        return var


def browse_func():
    new_file = ""
    file_name = fd.askopenfilename()
    for i in file_name:
        if i == '/':
            new_file += '\\\\'
        else:
            new_file += i
    flag = validate_file(new_file)
    if flag:
        '''global canvas
        canvas = tk.Canvas(root, borderwidth=0, selectborderwidth=0, highlightthickness=0)
        global frame
        frame = tk.Frame(canvas, borderwidth=0, highlightthickness=0)'''
        embed_frame()
        display_file()


def display_menu():
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=lambda: browse_func())
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    menubar.add_cascade(label="Add Client", command=lambda : add_client_mainmenu())
    menubar.add_cascade(label="Remove Client", command=lambda : remove_client_mainmenu())
    root.config(menu=menubar)


def open_file(path):
    return open(path, "r")


def set_root_geo(root):
    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry('%dx%d+0+0' % (width, height))
    root.state('zoomed')


def onFrameConfigure(canvas):
    # Reset the scroll region to encompass the inner frame
    canvas.configure(scrollregion=canvas.bbox("all"))


def scrollbar(canvas):
    vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    hsb = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
    canvas.configure(yscrollcommand=vsb.set)
    canvas.configure(xscrollcommand=hsb.set)
    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=frame, anchor="nw")
    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))


def embed_frame():
    global canvas
    canvas = tk.Canvas(root, borderwidth=0, selectborderwidth=0, highlightthickness=0)
    global frame
    frame = tk.Frame(canvas, borderwidth=0, highlightthickness=0)
    scrollbar(canvas)


def print_text(r, s1):
    tk.Label(frame, text=s1).grid(row=r, columnspan="20", sticky="W", ipadx=5)


def show_text_box(r, c):
    global v, text, lis
    for i in range(3):
        if i == 0:
            v.append(tk.StringVar(root))
            m = len(v) - 1
            #v[m].set('fu')
            text[i].append(ttk.OptionMenu(frame, v[m], *choiceso))
            text[i][m].config(width=20)
            lis = []
            lis.append(str(r))
            lis.append(str(c))
            place.append(lis)
            text[i][m].grid(row=r, column=c, padx=10, pady=10, sticky="E")
            c += 1
        else:

            text[i].append(tk.Text(frame, width=25, height=4, highlightthickness=0))
            text[i][m].grid(row=r, column=c, padx=10, pady=10)
            c += 1


def get_client_list():
    choiceso.clear()
    choiceso.append("Choose a Client")
    ret = db_con.get_client_db_list()
    for i in ret:
        choiceso.append(i)
    return ret


def refresh_list():
    ret = get_client_list()
    choiceso.remove("Choose a Client")
    for i in range(len(v)):
        temp = v[i].get()
        text[0][i]['menu'].delete(0, 'end')
        for choice in choiceso:
            text[0][i]['menu'].add_command(label=choice, command=tk._setit(v[i], choice))
        v[i].set(temp)


def add_client_to_db(add_client_mainmenu_text, error):
    client_name = add_client_mainmenu_text.get()
    data = db_con.add_client(client_name)
    error.labelText = data
    error.config(text=data)
    refresh_list()


def remove_client_to_db(checkvalue, r, remove_client_mainmenu_frame):
    for i in range(len(checkvalue)):
        print(checkvalue[i].get())
        if checkvalue[i].get():
            db_con.change_client_flag(choiceso[i])
    refresh_list()
    update_remove(r, remove_client_mainmenu_frame)



def print_table(l, r, flag):
    get_client_list()

    #global frame
    extra_field = ["Client", "Purpose", "Remarks"]
    c = 0
    if not flag[0]:
        for i in l:
            tk.Label(frame, text=i, wraplength=200, justify="left").grid(row=r, column=c, sticky="WE", ipadx=5,
                                                                         ipady=10)
            c += 1

        for i in extra_field:
            tk.Label(frame, text=i).grid(row=r, column=c, ipadx=5, ipady=10, columnspan=1)
            c += 1
        flag[0] = True

    else:
        for i in l:
            if i == "CR":
                tk.Label(frame, text="+", wraplength=200, justify="left", fg="green", font="20").grid(row=r, column=c,
                                                                                                      sticky="WE",
                                                                                                      ipadx=5, ipady=10)
                c += 1
            elif i == "DR":
                tk.Label(frame, text="-", wraplength=200, justify="left", fg="red", font="20").grid(row=r, column=c,
                                                                                                    sticky="WE",
                                                                                                    ipadx=5, ipady=10)
                c += 1
            else:
                tk.Label(frame, text=i, wraplength=200, justify="left").grid(row=r, column=c, sticky="WE", ipadx=5,
                                                                             ipady=10)
                c += 1
        show_text_box(r, c)


def separate_lines(f, add):
    f.seek(0)
    flag = [False]
    r = 0
    while True:
        s2 = f.readline()
        if not s2:
            break
        if s2 == "\n":
            continue
        if "|" not in s2:
            acc_id = s2.split(":")
            if acc_id[0] == "Account Id ":
                t1 = acc_id[1]
                t2 = ""
                for i in range(len(t1)):
                    if t1[i] != " ":
                        t2 = t2 + t1[i]
            if not add:
                print_text(r, s2)
                r += 1
            else:
                continue
        else:
            l = s2.split('|')
            last = l.pop()
            str1 = ""
            for i in last:
                if i != '\n':
                    str1 = str1 + i
            l.append(str1)

            if not add:
                print_table(l, r, flag)
                r += 1
            else:
                if l[0] == "No.":
                    continue
                else:
                    l.append(str(v[r].get()))
                    l.append(text[1][r].get('1.0', tk.END))
                    l.append(text[2][r].get('1.0', tk.END))
                    r += 1
                    print(l)
                    db_con.add_to_db(l, t2)
    if not add:
        b1 = tk.Button(frame, text="Add Records To Database", command=(lambda :add_records()))
        b1.grid(column=5, columnspan=3)


def add_client_mainmenu():
    global root
    t = tk.Toplevel(root)
    t.geometry('300x250')
    t.grab_set()
    add_client_mainmenu_frame = tk.Frame(t, borderwidth=0, highlightthickness=0)
    add_client_mainmenu_frame.pack()
    add_client_mainmenu_text = tk.Entry(add_client_mainmenu_frame, width=40)
    error = tk.Label(add_client_mainmenu_frame, text='')
    add_client_mainmenu_text.grid(row="5",pady="30",ipady="20")
    add_client_mainmenu_button = tk.Button(add_client_mainmenu_frame,text="Add Client", command=(lambda :add_client_to_db(add_client_mainmenu_text, error)), bg="#7f7fff", fg="white")
    add_client_mainmenu_button.grid(row="7")
    error.grid()


def remove_client_mainmenu():
    global root
    r = tk.Toplevel(root)
    r.geometry('500x500')
    r.grab_set()
    remove_client_mainmenu_frame = tk.Frame(r, borderwidth=0, highlightthickness=20)
    remove_client_mainmenu_frame.pack()
    update_remove(r, remove_client_mainmenu_frame)


def update_remove(r, remove_client_mainmenu_frame):
    remove_client_mainmenu_frame.destroy()
    checkvalue = []
    remove_client_mainmenu_frame = tk.Frame(r, borderwidth=0, highlightthickness=20)
    remove_client_mainmenu_frame.pack()
    count = 0
    for i in range(len(choiceso)):
        checkvalue.append(tk.BooleanVar())
        checkvalue[i].set(False)
        if choiceso[i] != "Choose a Client":
            tk.Checkbutton(remove_client_mainmenu_frame, text=choiceso[i], variable=checkvalue[i]).pack()
    remove_client_mainmenu_button = tk.Button(remove_client_mainmenu_frame, text="Remove Client", command=(lambda :remove_client_to_db(checkvalue, r, remove_client_mainmenu_frame)),
                                           bg="#7f7fff", fg="white")
    remove_client_mainmenu_button.pack()


def on_closing():
    global f, file_open, db_open
    if file_open:
        f.close()
    if db_open==0:
        db_con.close_db()
    root.destroy()





root = tk.Tk()
file_open = False
db_open = db_con.open_db()

v = []
choiceso = []
get_client_list()
place = [[]]
text = [[] for i in range(3)]
text1 = [[] for i in range(3)]
purpose = []
remarks = []
cli = []
lis = []
set_root_geo(root)
#canvas = tk.Canvas(root, borderwidth=0, selectborderwidth=0, highlightthickness=0)
#frame = tk.Frame(canvas, borderwidth=0, highlightthickness=0)
#embed_frame(canvas, frame)
frame = ""

display_menu()


root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()