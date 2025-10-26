import customtkinter


class AppOperation(customtkinter.CTkToplevel):
    def __init__(self,  mssg):
        super().__init__()
        self.title("Operación")
        self.geometry("400x130")
        self.resizable(True, False)
        self.attributes('-topmost', True)

        self.label = customtkinter.CTkLabel(self, text=mssg,)
        self.label.pack(pady=15)

        self.button_frame = customtkinter.CTkFrame(self)
        self.button_frame.pack(pady=10, padx=20)

        self.confirm_button = customtkinter.CTkButton(self.button_frame, text="Si", command=self.save, width=100)
        self.confirm_button.pack(side="left", expand=True, padx=10)

        self.cancel_button = customtkinter.CTkButton(self.button_frame, text="No", command=self.destroy,width=100)
        self.cancel_button.pack(side="right", expand=True, padx=10)

        self.lift()

    def save(self):
        self.result="Yes"
        self.destroy()# Llama al callback de confirmación

    def get_result(self):
        return self.result


