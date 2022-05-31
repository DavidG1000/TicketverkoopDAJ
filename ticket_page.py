# ############################## TICKET PAGE ###################################### #
# This page is the ticket page from the website FC SYNTRA                           #
# In this GUI supporters can bye stadion-tickets. Tickets are logged in a database  #
# Members/supporters can make a selection on tribune, row and chairs.               #
# Only free chairs are read-in from the db and visualised.                          #
# ################################################################################# #

# get tkinter module
import tkinter
from tkinter import *
from tkinter import messagebox


#from main_login_page import get_id_supp
#print(get_id_supp())

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

# declare lists/variables
options_tribune = []
options_rij = []
options_stoel = []
var_tribune = ""
var_rij = 0
var_stoel = 0
# voorlopig lidnummer
lidNummer = 3

# function test database connection
def toon_database_stadion():
    mycursor.execute("SELECT PlaatsID,tribune,rij,stoel,reserved,prijsTicket FROM stadion")
    for x in mycursor:
        print(x)

# run test database connection
toon_database_stadion()


# function choose tribune
def keuze_tribune():
    # settings text :choose the tribune
    tribune = Label(ticket, text="Kies eerst tribune / vak: ",font=('Helvetica',12))
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
    # changes the chosen parameter value_tribune to the global variabele var_tribune for the row function
    global var_tribune
    var_tribune = value_tribune

    # gets the free row-data from the chosen tribune from the databank and puts it in a list
    mycursor.execute("SELECT DISTINCT rij FROM stadion WHERE tribune = '" + value_tribune + "' AND reserved = 'Nee'")
    options_rij = list([x for x, in mycursor])

    # settings text choose row
    rij = Label(ticket, text="Kies daarna rij:",font=('Helvetica',12))
    rij.config(bg="DodgerBlue3", fg="white")
    rij.place(relx="0.1", rely="0.45")

    # settings optionbox row and command
    rij_keuze = tkinter.StringVar(ticket)
    rij_keuze.set(options_rij[0])
    optionsbox = OptionMenu(ticket, rij_keuze, *options_rij,
                            command=keuze_stoel) # returns the chosen parameter value_rij and run funct. keuze_zitplaats
    optionsbox.place(relx="0.4", rely="0.45")

# function choose chair
def keuze_stoel(value_rij):
    # changes the chosen parameter value_rij to the global variabele var_rij for the chair function
    global var_rij
    var_rij = value_rij

    # settings text choose chair
    stoel = Label(ticket, text="Kies daarna stoelnummer:",font=('Helvetica',12))
    stoel.config(bg="DodgerBlue3", fg="white")
    stoel.place(relx="0.1", rely="0.55")

    # gets the free chair-data from the chosen row from the databank and puts it in a list
    query = "SELECT DISTINCT stoel FROM stadion WHERE tribune =%s AND rij=%s AND reserved = 'Nee' ORDER by stoel"
    waarde = (var_tribune, value_rij,)
    mycursor.execute(query, waarde)

    # settings optionmenu choose chair
    options_stoel = list([x for x, in mycursor])
    stoel_keuze = IntVar()
    stoel_keuze.set(options_stoel[0])
    optionsbox = OptionMenu(ticket, stoel_keuze, *options_stoel,command=bevestig_keuze_stoel)
    optionsbox.place(relx="0.4", rely="0.55")

# changes the chosen parameter value_stoel to the global variabele var_stoel for the get_ticket function
def bevestig_keuze_stoel(value_stoel):
    global var_stoel
    var_stoel = value_stoel


# function gets the ticket price and print
def get_ticket():
    print("Gekozen tribune",var_tribune)
    print("Gekozen rij",var_rij)
    print("Gekozen stoel",var_stoel)

    # checks if options are actually chosen else raise error
    try:
        if var_tribune == "" or var_rij == 0 or var_stoel == 0:
            raise ValueError
        else:
            # gets the chosen ticketID and the ticketprice from the database
            print(var_tribune, var_rij, var_stoel)
            query = "SELECT plaatsID,prijsTicket,reserved FROM stadion WHERE tribune =%s and rij=%s and stoel=%s"
            mycursor.execute(query, (var_tribune, var_rij, var_stoel))
            myresult = mycursor.fetchall()
            for x in myresult:
                # second check if chair is free
                if x[2] != "Nee":
                    final = "Deze stoel is niet vrij"
                    answer.config(text=final)
                else:
                    #gets the price from the db
                    prijs = (x[1])
                    final = f"Ticketnr: {var_tribune}{var_rij}{var_stoel}   Prijs: {prijs} euro."
                    answer.config(text=final)
                    # popup messagebox are you sure
                    text_MsgBox = "Ticket "+var_tribune+str(var_rij)+str(var_stoel)+" bestellen"
                    MsgBox = messagebox.askquestion(text_MsgBox, "Bent u zeker ?")
                    if MsgBox == 'yes':
                        # sends the ticketorder to the table stadion
                        query = "UPDATE stadion SET reserved = 'Ja' WHERE tribune =%s and rij=%s and stoel=%s"
                        mycursor.execute(query, (var_tribune, var_rij, var_stoel))
                        # Inserts the Plaats_ID x[1] and lidNumber_ID. in the tabel  reservatie
                        print("Lidnummer en ticketid: ", lidNummer, x[0])
                        query = "INSERT INTO reservatie (lidNummer, plaatsID) VALUES (%s,%s)"

                        val = [lidNummer, x[0]]
                        mycursor.execute(query, val)
                        print("Ticket: ",var_tribune, var_rij, var_stoel," is besteld")
                        db.commit()

    # messagebox foutmelding
    except ValueError:
        messagebox.showerror(title="Fout", message="Geef de juiste gegevens in aub")


# configuration ticketorderbox
ticket = Tk()
ticket.title("FC Syntra Genk")
ticket.state("zoomed")
ticket.config(bg='DodgerBlue2')
ticket.grid_rowconfigure(0, weight=1)
ticket.grid_columnconfigure(0, weight=1)

# Title
header = "FC Syntra - Ticket - "+"Lidnummer: "+str(lidNummer)
L_Title = Label(ticket, text=header, fg='White', bg='DodgerBlue2', font=('Helvetica', 30))
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
new_stadion_label.place(relx=0.62, rely=0.36)


bestel = Button(ticket, text="Bestel ticket: ", width="20", font=('Helvetica',9), command=get_ticket)
bestel.place(relx="0.1", rely="0.75")


# Ticketprice frame
frame = Frame(ticket, width=200, height=30, relief="groove", borderwidth=2)
frame.place(relx="0.4", rely="0.745")
answer = Label(frame, text="")
answer.place(relx="0.10", rely="0.10")

# start program
keuze_tribune()

ticket.mainloop()

