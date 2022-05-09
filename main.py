
from tkinter import *
from tkinter import messagebox

# configuratie ticketbestelbox
root = Tk()
root.title("FC Syntra Genk")
root.geometry("1000x600")
root.config(bg='DodgerBlue2')


# kader voor lijnen
my_canvas = Canvas(root, width=900, height=600, background="DodgerBlue3")
my_canvas.pack()

# lijnen in het kader met beginpunt x-as, beginpunt y-as, eindpunt y-as,lengte, kleur, breedte
my_canvas.create_line(900, 0, 400, 250, fill="white", width=10)
my_canvas.create_line(900, 0, 400, 400, fill="SteelBlue2", width=10)
my_canvas.create_line(900, 0, 400, 600, fill="RoyalBlue4", width=10)



# blueprint
class clsTicketSales:
    def __init__(self, window):
        self.cellnumber = Label(window, text="Geef de tribune in ")
        self.cellnumber.config(bg="DodgerBlue3", fg="white")
        self.cellnumber.place(relx="0.1", rely="0.4")
        self.cellnumber_entry = Entry(window)
        self.cellnumber_entry.place(relx="0.5", rely="0.4")
        self.tprice = Label(window, text="Geef de rij in:")
        self.tprice.config(bg="DodgerBlue3", fg="white")
        self.tprice.place(relx="0.1", rely="0.5")
        self.options = ["A = 50 euro", "B = 75 euro", "C = 100 euro"]
        self.option = StringVar()
        self.option.set('Rij...')
        self.optionsbox = OptionMenu(window, self.option, *self.options)
        self.optionsbox.place(relx="0.5", rely="0.5")
        self.nr_tickets = Label(window, text="Aantal tickets")
        self.nr_tickets.config(bg="DodgerBlue3", fg="white")
        self.nr_tickets.place(relx="0.1", rely="0.6")
        self.nr_tickets_entry = Spinbox(window, from_=0, to=50, width="5")
        self.nr_tickets_entry.place(relx="0.5", rely="0.6")
        self.calculate = Button(window, text="Totaalprijs Tickets", width="20", command=self.calculate)
        self.calculate.place(relx="0.1", rely="0.7")
        self.clearbtn = Button(window, text="Clear", width="12", command=self.clear)
        self.clearbtn.place(relx="0.5", rely="0.7")
        self.frame = Frame(window, width=400, height=50, relief="groove", borderwidth=2)
        self.frame.place(relx="0.1", rely="0.8")
        self.answer = Label(self.frame, text=" ")
        self.answer.place(relx="0.3", rely="0.3")

    # functie berekening totaalprijs
    def calculate(self):

        numbertickets = int(self.nr_tickets_entry.get())


        # foutmelding bij foutieve invoer
        try:
            if len(self.cellnumber_entry.get()) > 100 or len(self.cellnumber_entry.get()) < 1:
                raise ValueError
            elif self.option.get() == "Rij...":
                raise ValueError
            elif self.option.get() == "A = 50 euro":
                result = 50 * int(self.nr_tickets_entry.get())
                final = result
                self.answer.config(text=final)
            elif self.option.get() == "B = 75 euro":
                result = 75 * int(self.nr_tickets_entry.get())
                final = result
                self.answer.config(text=final)
            elif self.option.get() == "C = 100 euro":
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



clsTicketSales(root)
root.mainloop()