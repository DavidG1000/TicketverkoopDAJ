
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd ="root",
  database ="fcsyntra"
)
mycursor = db.cursor()

def toon_database_stadion():
    mycursor.execute("SELECT PlaatsID,tribune,rij,stoel,reserved,prijsTicket FROM stadion  WHERE reserved = 'Nee'")
    for x in mycursor:
        print(x)

toon_database_stadion()
def toon_tribunelijst():
    mycursor.execute("SELECT DISTINCT tribune FROM stadion  WHERE reserved = 'Nee'")
    tribunelijst = [x for x, in mycursor]
    print(tribunelijst)



# configuration ticketorderbox
ticket = Tk()
ticket.title("FC Syntra Genk")
ticket.state('zoomed')
#ticket.geometry("1000x600")
ticket.config(bg='DodgerBlue2')
ticket.grid_rowconfigure(0, weight=1)
ticket.grid_columnconfigure(0, weight=1)

# Title
L_Title = Label(ticket, text= "FC Syntra - Ticket", fg='White', bg ='DodgerBlue2', font=('Helvetica',50))
L_Title.pack(pady = 20)


# canvas for lines
my_canvas = Canvas(ticket, width=3000, height=1000, background="DodgerBlue3")
my_canvas.grid_rowconfigure(0, weight=1)
my_canvas.grid_columnconfigure(0, weight=1)
my_canvas.pack(padx= 5, pady = 60
               )

# lines in the canvas with startingpoint x-as, startingpoint y-as, endpoint x-as, length, color and width
my_canvas.create_line(900, 0, 400, 250, fill="white", width=10)
my_canvas.create_line(900, 0, 400, 400, fill="SteelBlue2", width=10)
my_canvas.create_line(900, 0, 400, 600, fill="RoyalBlue4", width=10)


#configuration image stadion
stadion = Image.open("stadion.png")
resized = stadion.resize((450,280), Image.ANTIALIAS)
new_stadion = ImageTk.PhotoImage(resized)
new_stadion_label = Label(ticket, image=new_stadion, bg ="DodgerBlue3")
new_stadion_label.place(x=800, y=270)



class TicketSales:
    def __init__(self, window):

        #settings text choose the tribune
        self.tribune = Label(window, text="Kies de tribune / vak: ")
        self.tribune.config(bg="DodgerBlue3", fg="white")
        self.tribune.place(relx="0.1", rely="0.35")

        #gets the tribune-data from the databank and puts it in a list
        mycursor.execute("SELECT DISTINCT tribune FROM stadion  WHERE reserved = 'Nee'")
        self.options = list([x for x, in mycursor])

        #settings optionbox tribune
        self.option = StringVar()
        self.option.set("Tribune....")
        self.optionsbox = OptionMenu(window, self.option, *self.options)
        self.optionsbox.place(relx="0.4", rely="0.35")

        #settings text choose row
        self.rij = Label(window, text="Geef de rij in:")
        self.rij.config(bg="DodgerBlue3", fg="white")
        self.rij.place(relx="0.1", rely="0.45")

        #gets the row-data from the databank and puts it in a list
        mycursor.execute("SELECT DISTINCT rij FROM stadion   WHERE reserved = 'Nee'")
        self.options = list([x for x, in mycursor])

        #settings optionbox row
        self.option = StringVar()
        self.option.set('Rij...')
        self.optionsbox = OptionMenu(window, self.option, *self.options)
        self.optionsbox.place(relx="0.4", rely="0.45")

        #settings text choose chair
        self.chair = Label(window, text="Geef de zitplaats in:")
        self.chair.config(bg="DodgerBlue3", fg="white")
        self.chair.place(relx="0.1", rely="0.55")

        #gets the chair-data from the databank and puts it in a list
        mycursor.execute("SELECT DISTINCT stoel FROM stadion WHERE reserved = 'Nee'")
        self.options = list([x for x, in mycursor])

        #settings optionbox chair
        self.option = StringVar()
        self.option.set('Zitplaats...')
        self.optionsbox = OptionMenu(window, self.option, *self.options)
        self.optionsbox.place(relx="0.4", rely="0.55")

        #spinbox number of tickets
        #self.nr_tickets = Label(window, text="Aantal tickets (max. 4 st.)")
        #self.nr_tickets.config(bg="DodgerBlue3", fg="white")
        #self.nr_tickets.place(relx="0.1", rely="0.65")
        #self.nr_tickets_entry = Spinbox(window, from_=0, to=4, width="5")
        #self.nr_tickets_entry.place(relx="0.4", rely="0.65")

        self.calculate = Button(window, text="Totaalprijs Tickets", width="20", command=self.calculate)
        self.calculate.place(relx="0.4", rely="0.75")
        self.clearbtn = Button(window, text="Clear", width="12", command=self.clear)
        self.clearbtn.place(relx="0.1", rely="0.85")
        self.frame = Frame(window, width=150, height=30, relief="groove", borderwidth=2)
        self.frame.place(relx="0.1", rely="0.75")
        self.answer = Label(self.frame, text=" ")
        self.answer.place(relx="0.3", rely="0.3")

    # functie berekening totaalprijs
    def calculate(self):

        numbertickets = int(self.nr_tickets_entry.get())



        try:
            if len(self.tribune_entry.get()) > 100 or len(self.tribune_entry.get()) < 1:
                raise ValueError
            elif self.option.get() == "Rij...":
                raise ValueError
            elif self.option.get() == "A":
                result = 50 * int(self.nr_tickets_entry.get())
                final = result
                self.answer.config(text=final)
            elif self.option.get() == "B":
                result = 75 * int(self.nr_tickets_entry.get())
                final = result
                self.answer.config(text=final)
            elif self.option.get() == "C":
                result = 100 * int(self.nr_tickets_entry.get())
                final = result
                self.answer.config(text=final)

        # messagebox foutmelding
        except ValueError:
            messagebox.showerror(title="Fout", message="Geef de juiste gegevens in aub")

    # functie wissen ingave
    def clear(self):
        self.cellnumber_entry.delete(0, END)
        self.nr_tickets_entry.delete(0, END)
        self.option.set("Rij...")



TicketSales(ticket)
ticket.mainloop()