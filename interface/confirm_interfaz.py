import customtkinter

class ConfirmationDialog(customtkinter.CTkToplevel):
    def __init__(self, parent, confirm_callback):
        super().__init__(parent)
        self.title("Information")
        self.geometry("300x150")
        self.resizable(False, False)
        self.attributes('-topmost', True)

        self.label = customtkinter.CTkLabel(self, text="Por favor, confirme que desea realizar la operación.")
        self.label.pack(pady=20)

        self.button_frame = customtkinter.CTkFrame(self)
        self.button_frame.pack(pady=10, padx=20)

        self.confirm_button = customtkinter.CTkButton(self.button_frame, text="Yes", command=lambda: self.on_confirm(confirm_callback), width=100)
        self.confirm_button.pack(side="left", expand=True, padx=10)

        self.cancel_button = customtkinter.CTkButton(self.button_frame, text="No", command=self.destroy,width=100)
        self.cancel_button.pack(side="right", expand=True, padx=10)

        self.lift()

    def on_confirm(self, confirm_callback):
        confirm_callback()  # Llama al callback de confirmación
