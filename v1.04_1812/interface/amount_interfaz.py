import customtkinter
import tkinter as tk


class AppAmountAdd(customtkinter.CTkToplevel):
    def __init__(self,  item,ud):
        super().__init__()
        self.title("Añada cantidad")
        self.geometry("500x200")
        self.resizable(True, False)
        self.attributes('-topmost', True)

        self.label = customtkinter.CTkLabel(self, text=item)
        self.label.pack(pady=15)

        self.amount_frame = customtkinter.CTkFrame(self)
        self.amount_frame.pack(pady=10, padx=20)

        self.label = customtkinter.CTkLabel(self.amount_frame, text=ud)
        self.label.pack(side="left", expand=True, padx=10)

        amount_value = tk.StringVar(value=0)
        self.entry = customtkinter.CTkEntry(self.amount_frame, textvariable=amount_value
                                            ,text_color="#FFFFFF")
        self.entry.pack(side="right", expand=True, padx=10)

        self.button_frame = customtkinter.CTkFrame(self)
        self.button_frame.pack(pady=10, padx=20)

        self.confirm_button = customtkinter.CTkButton(self.button_frame, text="Si", command=self.save, width=100)
        self.confirm_button.pack(side="left", expand=True, padx=10)

        self.cancel_button = customtkinter.CTkButton(self.button_frame, text="No", command=self.destroy,width=100)
        self.cancel_button.pack(side="right", expand=True, padx=10)

        self.lift()

    def save(self):
        self.amount=self.entry.get()
        self.destroy()# Llama al callback de confirmación

    def get_items(self):
        return self.amount

