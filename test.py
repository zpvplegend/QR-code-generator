import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
import os
import uuid
import shutil

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("400x400")
        self.window.title("QR code generator")
        self.elements()
        self.current_option = None
        self.response=None
        

    def run(self):
        self.window.mainloop()

    def elements(self):
        label = ttk.Label(master=self.window, text="  QR CODE GENERATOR  ")
        label.pack()

        self.menu = ttk.Combobox(master=self.window, values=['Text', 'URL', 'Text & URL'])
        self.menu.place(x=125, y=100)

        self.btn = ttk.Button(master=self.window, text="GENERATE", command=self.generate)
        self.btn.place(x=165, y=300)

        self.textbox1 = tk.Text(master=self.window, height=3)
        self.textbox2 = tk.Text(master=self.window, height=1)
        self.textbox3 = tk.Text(master=self.window, height=3)

        self.menu.bind("<<ComboboxSelected>>", self.on_combo_select)

    def on_combo_select(self, event=None):
        selected_option = self.menu.get().lower()
        
        
        if self.current_option:
            self.current_option.place_forget()

        if selected_option == "text":
            self.current_option = self.textbox1

        elif selected_option == "url":
            self.textbox2.delete('1.0',tk.END)
            self.current_option = self.textbox2
            self.textbox2.insert('1.0', 'https://')

        elif selected_option == 'text & url':
            self.textbox3.delete('1.0',tk.END)
            self.current_option = self.textbox3
            self.textbox3.insert('1.0','https://')

        
        if self.current_option:
            self.current_option.place(x=0, y=150)

    def generate(self):
        self.data = 'https://api-ninjas.com'
        self.fmt = 'png'

        if self.current_option == self.textbox1:
            self.api_url = f'https://api.api-ninjas.com/v1/qrcode?data={self.textbox1.get("1.0",tk.END)}&format=png'
            self.format()
            self.validation()

        if self.current_option==self.textbox2:
            self.api_url = f'https://api.api-ninjas.com/v1/qrcode?data={self.textbox2.get("1.0",tk.END)}&format=png'
            self.format()
            self.validation()

        if self.current_option==self.textbox3:
            self.api_url = f'https://api.api-ninjas.com/v1/qrcode?data={self.textbox3.get("1.0",tk.END)}&format=png'
            self.format()
            self.validation()

        self.response = requests.get(self.api_url, headers={'X-Api-Key': 'YOUR_API_KEY',  'Accept': 'image/png'}, stream=True)
        
        self.validation()

    def validation(self):
        
        if self.response and self.response.status_code == requests.codes.ok:
            if not os.path.exists('codes'):
                os.makedirs('codes')
                
            random_file_name = str(uuid.uuid4()) + '.png'
            
            with open(os.path.join('codes', random_file_name), 'wb') as out_file:
                shutil.copyfileobj(self.response.raw, out_file)
            
            os.startfile(os.path.join('codes', random_file_name))

            messagebox.showinfo("Code generated!","Done!, the image has been saved in the 'codes' folder ")
    
    def format(self):
        self.api_url=self.api_url.format(self.data,self.fmt)

app = GUI()
app.run()