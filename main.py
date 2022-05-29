# get tkinter module
import tkinter
from tkinter import *
from tkinter import messagebox

# get image module
from PIL import ImageTk, Image

# make database connection
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="fcsyntra"
)
mycursor = db.cursor()

options_tribune = []
options_rij = []
options_zitplaats = []



# test database connection
def toon_database_stadion():
    mycursor.execute("SELECT PlaatsID,tribune,rij,stoel,reserved,prijsTicket FROM stadion")
    for x in mycursor:
        print(x)


# run test
toon_database_stadion()


# function choose tribune
def keuze_tribune():
    # settings text :choose the tribune
    tribune = Label(ticket, text="Kies de tribune / vak: ")
    tribune.config(bg="DodgerBlue3", fg="white")
    tribune.place(relx="0.1", rely="0.35")

    # gets the free tribune-data from the databank and puts it in a list
    mycursor.execute("SELECT DISTINCT tribune FROM stadion  WHERE reserved = 'Nee'")
    options_tribune = list([x for x, in mycursor])

    # settings optionmenu tribune and command
    tribune_keuze = StringVar()
    tribune_keuze.set("Tribune...")
    optionsbox = OptionMenu(ticket, tribune_keuze, *options_tribune,
                            command=keuze_rij) # returns the chosen parameter value_tribune and run function keuze_rij
    optionsbox.place(relx="0.4", rely="0.35")


# function choose row
def keuze_rij(value_tribune):
    # changes the chosen parameter value_tribune to the global variabele var_tribune for the row function and print test
    global var_tribune
    var_tribune = value_tribune
    print("Dit is de gekozen tribune als variable: ", var_tribune)
    # gets the free row-data from the chosen tribune from the databank and puts it in a list
    mycursor.execute("SELECT DISTINCT rij FROM stadion WHERE tribune = '" + value_tribune + "' AND reserved = 'Nee'")
    options_rij = list([x for x, in mycursor])

    # settings text choose row
    rij = Label(ticket, text="Geef de rij in:")
    rij.config(bg="DodgerBlue3", fg="white")
    rij.place(relx="0.1", rely="0.45")

    # settings optionbox row and command
    rij_keuze = tkinter.StringVar(ticket)
    rij_keuze.set(options_rij[0])
    optionsbox = OptionMenu(ticket, rij_keuze, *options_rij,
                            command=keuze_zitplaats) # returns the chosen parameter value_rij and run funct keuze_zitplaats
    optionsbox.place(relx="0.4", rely="0.45")

# function choose chair
def keuze_zitplaats(value_rij):
    # test print chosen row
    print("Dit is de gekozen rij: ",value_rij)
    # settings text choose chair
    zitplaats = Label(ticket, text="Kies uw zitplaats:")
    zitplaats.config(bg="DodgerBlue3", fg="white")
    zitplaats.place(relx="0.1", rely="0.55")

    # gets the free chair-data from the chosen row from the databank and puts it in a list
    query = "SELECT DISTINCT stoel FROM stadion WHERE tribune =%s AND rij=%s AND reserved = 'Nee' ORDER by stoel"
    waarde = (var_tribune, value_rij,)
    mycursor.execute(query, waarde)

    # settings optionmenu choose chair
    options_zitplaats = list([x for x, in mycursor])
    zitplaats_keuze = IntVar()
    zitplaats_keuze.set(options_zitplaats[0])
    optionsbox = OptionMenu(ticket, zitplaats_keuze, *options_zitplaats)
    optionsbox.place(relx="0.4", rely="0.55")


# clears the entry's
def clear():
    tribune_keuze.set("Tribune...")
    rij_keuze.set(0)
    zitplaats_keuze.set(0)
    answer.config(text="")


# functie berekening totaalprijs
def calculate():
    # numbertickets = int(self.nr_tickets_entry.get())
    # print(self.tribune_keuze, self.rij_keuze, self.zitplaats_keuze)
    # checks if options are actually chosen
    try:
        if tribune_keuze.get() == "Tribune..." or rij_keuze.get() == "Rij..." or zitplaats_keuze.get() == "Zitplaats" \
                                                                                                          "...":
            raise ValueError
        else:
            # gets the chosen ticketID and the ticketprice from the database
            print(tribune_keuze.get(), rij_keuze.get(), zitplaats_keuze.get())
            query = "SELECT plaatsID,prijsTicket FROM stadion WHERE tribune =%s and rij=%s and stoel=%s"
            mycursor.execute(query, (tribune_keuze.get(), rij_keuze.get(), zitplaats_keuze.get()))
            myresult = mycursor.fetchall()
            for x in myresult:
                prijs = (x[1])

            final = f"Ticketnr: {tribune_keuze.get()}{rij_keuze.get()}{zitplaats_keuze.get()}   Prijs: {prijs} euro."
            # final = (self.tribune_keuze.get(),self.rij_keuze.get(),self.zitplaats_keuze.get())
            answer.config(text=final)


    # messagebox foutmelding
    except ValueError:
        messagebox.showerror(title="Fout", message="Geef de juiste gegevens in aub")


# configuration ticketorderbox
ticket = tkinter.Tk()
ticket.title("FC Syntra Genk")
ticket.state("zoomed")
ticket.config(bg='DodgerBlue2')
ticket.grid_rowconfigure(0, weight=1)
ticket.grid_columnconfigure(0, weight=1)

# Title
L_Title = Label(ticket, text="FC Syntra - Ticket", fg='White', bg='DodgerBlue2', font=('Helvetica', 50))
L_Title.pack(pady=20)

# canvas for lines
my_canvas = Canvas(ticket, width=3000, height=1000, background="DodgerBlue3")
my_canvas.grid_rowconfigure(0, weight=1)
my_canvas.grid_columnconfigure(0, weight=1)
my_canvas.pack(padx=5, pady=60
               )

# lines in the canvas with startingpoint x-as, startingpoint y-as, endpoint x-as, length, color and width
my_canvas.create_line(900, 0, 400, 250, fill="white", width=10)
my_canvas.create_line(900, 0, 400, 400, fill="SteelBlue2", width=10)
my_canvas.create_line(900, 0, 400, 600, fill="RoyalBlue4", width=10)

# configuration image stadion tribunes
stadion = Image.open("stadion.png")
resized = stadion.resize((450, 280), Image.ANTIALIAS)
new_stadion = ImageTk.PhotoImage(resized)
new_stadion_label = Label(ticket, image=new_stadion, bg="DodgerBlue3")
new_stadion_label.place(x=800, y=270)


calculate = Button(ticket, text="Bestel ticket: ", width="20", command=calculate)
calculate.place(relx="0.1", rely="0.75")

# clearbutton
clearbtn = Button(ticket, text="Clear", width="12", command=clear)
clearbtn.place(relx="0.1", rely="0.85")

# Ticketprice frame
frame = Frame(ticket, width=200, height=30, relief="groove", borderwidth=2)
frame.place(relx="0.4", rely="0.75")
answer = Label(frame, text="")
answer.place(relx="0.10", rely="0.10")


# start program
keuze_tribune()

ticket.mainloop()


# optional spinbox for number off tickets
# self.nr_tickets = Label(window, text="Aantal tickets (max. 4 st.)")
# self.nr_tickets.config(bg="DodgerBlue3", fg="white")
# self.nr_tickets.place(relx="0.1", rely="0.65")
# self.nr_tickets_entry = Spinbox(window, from_=0, to=4, width="5")
# self.nr_tickets_entry.place(relx="0.4", rely="0.65")