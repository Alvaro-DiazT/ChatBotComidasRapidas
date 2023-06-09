from builtins import bool
from tkinter import *
from ChatBot import obtenerRespuesta, nombreBot
import csv
import sys



BG_GRIS = "#ABB2B9"
BG_COLOR = "#17202A"
COLOR_TEXTO = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

class AplicacionChat:

    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("ChatBot Comidas Rapidas")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=500, height= 550, bg=BG_COLOR)

        #head label
        head_label = Label(self.window, bg=BG_COLOR, fg=COLOR_TEXTO,
                           text="Welcome", font= FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        #tiny divider
        line = Label(self.window, width=450, bg=BG_GRIS)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        #text widget
        self.text_widget = Text(self.window, width=20, height=2, bg= BG_COLOR,
                                fg=COLOR_TEXTO, font= FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        #scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        #bottom label
        bottom_label = Label(self.window, bg=BG_GRIS, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        #message entry box
        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=COLOR_TEXTO, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # send button
        send_button = Button(bottom_label, text="Enviar", font=FONT_BOLD, width=20,
                             bg=BG_GRIS, command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)



    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "Tú")


    def _insert_message(self, msg, sender):

        if not msg:
            return


        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure( state=DISABLED)

        respuestaBot=obtenerRespuesta(msg)
        msg2 = f"{nombreBot}: {respuestaBot}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)

        conversacion.append({'Usuario': msg, 'Chatbot': respuestaBot})



        # Escribe la lista de conversación en un archivo CSV
        with open('conversacion.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['Usuario', 'Chatbot'])
            writer.writeheader()
            for linea in conversacion:
                writer.writerow(linea)
        with open('conversacion.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)
        if respuestaBot == "hasta luego":
            sys.exit(0)
        return








conversacion = []
if __name__ == "__main__":
    app = AplicacionChat()
    app.run()
