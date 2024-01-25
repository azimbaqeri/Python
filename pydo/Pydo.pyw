from datetime import date # pour date et heure
from tkinter import * # pour GUI interface
import tkinter as tk
from tkinter import  CENTER, END,  NO, SW, TOP, YES, ttk
from PIL import Image, ImageTk #pour image
import mysql.connector # pour la base de donnée
from tkinter.messagebox import showinfo # pour messagebox
from tkcalendar import DateEntry # pour calendrier


# root window
root = tk.Tk()
root.geometry('600x530')
root.resizable(False, False)
root.title('Todo List Application')
ico = Image.open("logo-mns.png")
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)

#mysql connection et cursor pour la base de donnée
my_connect = mysql.connector.connect(
  host="localhost",
  user="root", 
  passwd="",
  database="todo"
)
my_conn = my_connect.cursor()



#______________________________________Tout les functione___________________________________________________________________________
def Add_list(): 
    if inputtxt.get('1.0',END).strip()!='' and combo.get()!='':
        my_conn.execute(f"INSERT INTO tasks (Title, DueDate, Status) VALUES ('{inputtxt.get('1.0',END)}', '{cal.get()}', '{combo.get()}')")
        auto_load()
        clear_list()
    else:
        tk.messagebox.showinfo(title='INFO', message='Veuillez remplir le champ du titre et sélectionner le statut')
        return None

def auto_load():
    for i in tree.get_children():
        tree.delete(i)
    my_conn.execute("SELECT * FROM tasks order by TaskID DESC")
    for task in my_conn:  
        tree.insert('', 'end',text="1",values=(task[0],task[1],task[2],task[3]))

def Remove_list():
    
    if tree.selection():

        curItem = tree.focus()
        msg = tk.messagebox.askquestion(title='Suppprimer', message='Etes-vous sûr de supprimer la tâche sélectionnée ?')
        if msg =='yes':
            
            my_conn.execute("DELETE FROM tasks where TaskID='"+str(tree.item(curItem)["values"][0])+"'")
            tk.messagebox.showinfo(title='INFO', message='Tâche supprimée !')
            auto_load()  
    else:
        return None
    # list1.delete(list1.curselection())
    
def Marguer_complete():
    if tree.selection() and combo_marguer.get()!='':
        curItem = tree.focus()
        my_conn.execute(f"UPDATE tasks SET Status='{combo_marguer.get()}' where TaskID='{str(tree.item(curItem)['values'][0])}'")
        tk.messagebox.showinfo(title='INFO', message='La tâche est mise à jour !')
        auto_load()
    else:
        tk.messagebox.showinfo(title='INFO', message='Sélectionnez une tâche et sélectionnez le statut dans la liste')
        return None
    # list1.itemconfig(list1.curselection(), fg="green")

combo_marguer = ttk.Combobox(state="readonly",values=["à faire", "en cours", "terminée"], width=20, height=20)
combo_marguer.pack() 
combo_marguer.place(x=310, y=393)

# Button Marguer comme complete 
completeButton = tk.Button(root, 
                        text = "Marquer",  
                        command = Marguer_complete, height=1, width=15, background='#ff6d08') 
completeButton.pack()
completeButton.place(x=465, y=393)


#________________________________________________


def on_treeview_double_clicked(event):
    # Handles double click event on treeview to populate form for editing selected task
    AddButton.place_forget()
    # Get all selected items
    curItem = tree.selection()
    date_info  = tree.item(curItem)['values'][2]
    status_info = tree.item(curItem)['values'][3]
    # Make sure a row is selected
    if not curItem:
        return
    else:
        # Get the first selected item
        # tk.messagebox.showinfo(title='INFO', message=dateinfo)
        inputtxt.delete(1.0, tk.END)
        
        inputtxt.insert(tk.END, str(tree.item(curItem)['values'][1]))
        cal.set_date(date_info)
        
        match status_info:
            case 'à faire':
                combo.current(0)
            case 'en cours':
                combo.current(1)
            case 'terminée':
                combo.current(2)
        
            # str(tree.item(curItem)['values'][0]))  "à faire", "en cours", "terminée"



def clear_list():
    inputtxt.delete(1.0, tk.END)
    cal.set_date(date.today())
    combo.set('') 
    AddButton.place(x=20, y=480)

def update_list():
    curItem = tree.focus()
    my_conn.execute(f"UPDATE tasks SET Title='{inputtxt.get('1.0',END)}', DueDate='{cal.get()}', Status='{combo.get()}' where TaskID='{str(tree.item(curItem)['values'][0])}'")
    tk.messagebox.showinfo(title='INFO', message='La tâche est mise à jour !')

    clear_list()
    auto_load()

    
# -------------------------------------- toutes les element de la fenetre---------------------------------------------------------------------------- 

# Button Effacer  
RemoveButton = tk.Button(root, 
                        text = "Retour",  
                        command = clear_list, height=1, width=15, background='#ff6d08') 
RemoveButton.pack()
RemoveButton.place(x=465, y=480)

# Button mise à jour
updateButton = tk.Button(root, 
                        text = "Mise à jour",  
                        command = update_list, height=1, width=60, background='#ff6d08') 
updateButton.pack()
updateButton.place(x=20, y=480)


# treeview pour afficher les tâches
tree=ttk.Treeview(root, column=("id", "title", "Due Date", "Status"), show='headings', height=8)
tree.column("# 1",anchor=CENTER, stretch=NO, width=0)
tree.heading("# 1", text="ID")
tree.column("# 2", anchor=SW, stretch=YES, width=50)
tree.heading("# 2", text="Title")
tree.column("# 3", anchor=CENTER, stretch=YES, width=50)
tree.heading("# 3", text="Due")
tree.column("# 4", anchor=CENTER, stretch=YES, width=50)
tree.heading("# 4", text="Status")
tree.bind("<Double-1>", on_treeview_double_clicked)
# Crea a scrollbar pour scroller de la fenetre
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
# Configurer l'arborescence pour utiliser la barre de défilement
tree.configure(yscrollcommand=scrollbar.set)

# Placez la barre de défilement sur le côté droit de l'arborescence
scrollbar.pack(side="left", fill="y")
scrollbar.place(y=122, x=563, height=257)
tree.pack(expand=YES, fill="both", padx=20, pady=(120,150))



# Bouton Supprimer l'élément sélectionné
RemoveButton = tk.Button(root, 
                        text = "Suppprimer",  
                        command = Remove_list, height=1, width=10, background='#ff6d08') 
RemoveButton.pack()
RemoveButton.place(x=20, y=390)



#-------------------------------------------ajouter une section de données ---------------------------------------------
separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x')
separator.place(x=20, y=430,width=560)
#____________Titre_______________
inputtxt = tk.Text(root, 
                   height = 1, 
                   width = 10) 
inputtxt.pack(side=TOP , ipadx=0, ipady=0) 
inputtxt.place(x=70, y=445)
lbl = tk.Label(root,height = 1, 
                   width = 5, text='Title : ', background='black', foreground='white')
lbl.pack(side=TOP , ipadx=0, ipady=0) 
lbl.place(x=20, y=445)
 #____________Due Date_______________
cal = DateEntry(root, width=12, year=2024, month=1, day=22,date_pattern='yyyy-MM-dd', 
    background='darkblue', foreground='white', borderwidth=2)
cal.set_date(date.today())
cal.pack(padx=0, pady=0)
cal.place(x=245, y=445)
lbl = tk.Label(root,height = 1, 
                   width = 10, text='Due Date : ', background='black', foreground='white')
lbl.pack(side=TOP , ipadx=0, ipady=0) 
lbl.place(x=160, y=445)
#____________Status_______________
lbl = tk.Label(root,height = 1, 
                   width = 10, text='Status : ', background='black', foreground='white')
lbl.pack(side=TOP , ipadx=0, ipady=0) 
lbl.place(x=350, y=445)    
combo = ttk.Combobox(state="readonly",values=["à faire", "en cours", "terminée"], width=20)
combo.pack() 
combo.place(x=435, y=445)

# _______________ Button Add __________________ 
AddButton = tk.Button(root, 
                        text = "Ajouter",  
                        command = Add_list, height=1, width=79,background='#ff6d08') 
AddButton.pack()
AddButton.place(x=20, y=480)

# text pour modification les taches
lbl = tk.Label(root,height = 1, 
                   width = 55, text='Double-cliquez sur chaque tâche pour la modification', background='black', foreground='white')
lbl.pack(side=TOP , ipadx=0, ipady=0) 
lbl.place(x=-30, y=90)

#_______________Image___________________

canvas_photo = Canvas(root, width = 600, height = 85, bg = 'black', bd=0, highlightthickness=0)
mnslogo = PhotoImage(file='logo-mns.png')
item = canvas_photo.create_image(300, 50, image = mnslogo)
canvas_photo.image = mnslogo
canvas_photo.pack()
canvas_photo.place(x=0, y=0)


# une menu sample pour la fenetre
menu_bar = tk.Menu(root)
menu_bar.config()
menu_file = tk.Menu(menu_bar, tearoff=0, background='white')
menu_file.add_command(label="Sortie", command=root.quit)
menu_bar.add_cascade(label="File", menu=menu_file)
root.config(menu=menu_bar, bg='black')

auto_load()
root.mainloop()
