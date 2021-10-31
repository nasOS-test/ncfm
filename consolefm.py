"""

Console file manager

Made by scratcher-402

"""

from readchar import readkey

def eprint(escape): print("\033"+escape, end="")
def clear(): eprint("[2J\033[0;0H")
def pleasewait(): clear(); print("Please Wait")
def cup(x,y):
    x = str(x)
    y = str(y)
    eprint("["+y+";"+x+"H")
import os
columns = os.get_terminal_size().columns
lines = os.get_terminal_size().lines
pages = []
def gen_listdir(path="."):
 listdir = [".."]
 for file in os.listdir():
  listdir.append(file)
 global pages
 pages = []
 i = -1
 templist = []
 for file in listdir:
    i += 1
    templist.append(file)
    try:
        st1 = i == len(listdir)%len(pages) and len(pages) == len(listdir)//(lines-3)
    except: st1 = False
    if i == lines-4 or i == len(listdir)-1 or st1:
        pages.append(templist)
        templist = []
        i = -1
gen_listdir()
page = 0
filefocus = 0
def draw_ui():
    clear()
    print("\033[43;30;1mPress H for help\033[0m")
    i = -1
    for file in pages[page]:
        i += 1
        if filefocus == i:
            eprint("[47;30m")
        if len(file) > columns:
            print(file[:columns])
        else:
            print(file)
        if filefocus == i:
            eprint("[0m")
    if len(pages[page]) < lines-3:
        for a in range(0, len(pages[page])-lines+2):
            print()
    print(f"\033[43;30;1mPage {page+1}/{len(pages)}\033[0m", end="\n")
draw_ui()
while True:
    k = readkey()
    if k == "q" or k == "Q":
        exit()
    if k == '\x1b[C' and page+1 <= len(pages)-1:
        page += 1
        filefocus = 0
        draw_ui()
    if k == '\x1b[D' and page-1 >= 0:
        page -= 1
        filefocus = 0
        draw_ui()
    if k == '\x1b[B' and filefocus+1 < len(pages[page]):
        filefocus += 1
        cup(0, filefocus+2)
        eprint("[47;30m")
        print(pages[page][filefocus]+" "*(columns-len(pages[page][filefocus])))
        eprint("[0m")
        cup(0, filefocus+1)
        print(pages[page][filefocus-1]+" "*(columns-len(pages[page][filefocus-1])))
        cup(lines-1,0)
    if k == '\x1b[A' and filefocus > 0:
        filefocus -= 1
        cup(0, filefocus+2)
        eprint("[47;30m")
        print(pages[page][filefocus]+" "*(columns-len(pages[page][filefocus])))
        eprint("[0m")
        cup(0, filefocus+3)
        print(pages[page][filefocus+1]+" "*(columns-len(pages[page][filefocus+1])))
        cup(0, lines-1)
    if k == " " or k == "\r":
        try:
            prev_dir = os.getcwd()
            os.chdir(os.getcwd()+"/"+pages[page][filefocus])
            gen_listdir()
            page = 0
            filefocus = 0
        except NotADirectoryError:
            clear()
            print("Please enter a program to run this file. \n\n")
            prog = input("> ")
            os.spawnlp(os.P_WAIT, prog, prog, pages[page][filefocus])
            draw_ui()
        except PermissionError:
            clear()
            print("Permission Denied \n\n Press any key")
            readkey()
            os.chdir(prev_dir)
        draw_ui()
    if k == "h" or k == "H":
        clear()
        print(""" arrow keys - navigate
space/enter - open file or directory
d - delete file
m - mkdir
q - exit

(press any key)""")
        readkey()
        draw_ui()
    if k == "d" or k == "D":
        clear()
        print("Are you sure you want to delete this file? \n\n"+pages[page][filefocus]+"\n\nPress any key to continue, q to cancel")
        k = readkey()
        if not k == "q" or k == "Q":
            try: os.remove(os.getcwd()+"/"+pages[page][filefocus])
            except IsADirectoryError:
                for root, dirs, files in os.walk(os.getcwd()+"/"+pages[page][filefocus], topdown=False):
                    for name in files:
                        print("Deleting file "+name)
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        print("Deleting directory "+name)
                        os.rmdir(os.path.join(root, name))
            gen_listdir()
        draw_ui()
    if k == "m" or k == "M":
        clear()
        print("Directory name: \n\n")
        a = input("> ")
        os.mkdir(os.getcwd()+"/"+a)
        gen_listdir()
        draw_ui()