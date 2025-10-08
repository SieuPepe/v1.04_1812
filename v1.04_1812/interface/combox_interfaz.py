from interface.confirm_interfaz import *
import customtkinter

customtkinter.set_appearance_mode("dark")

class ScrollableCheckBoxFrame(customtkinter.CTkScrollableFrame):

    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.checkbox_list = []

        for i, item in enumerate(item_list):
            self.add_item(item)


    def add_item(self, item):
        checkbox = customtkinter.CTkCheckBox(self, text=item)

        if self.command is not None:
            checkbox.configure(command=self.command)

        checkbox.grid(row=len(self.checkbox_list), column=0, pady=(10, 10),sticky="w")
        self.checkbox_list.append(checkbox)


    def get_checked_items(self):

        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]

    def uncheck_all(self):
        for checkbox in self.checkbox_list:
                checkbox.deselect()

    def check_all(self):
        for checkbox in self.checkbox_list:
                checkbox.select()


class AppCombox(customtkinter.CTkToplevel):
    width = 700
    height = 500

    def __init__(self, item_list, callback):
        super().__init__()

        self.callback = callback

        self.selected_items = []

        self.title("Seleccionar items")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        widthButton1 = int(self.width / 2) - 40
        self.check_button = customtkinter.CTkButton(self, text="Select All", width=widthButton1,
                                                    command= self.check_all)
        self.check_button.grid(row=0, padx=20, pady=20, sticky="nw")
        self.uncheck_button = customtkinter.CTkButton(self, text="Unselect All", width=widthButton1,
                                                      command= self.uncheck_all)
        self.uncheck_button.grid(row=0, padx=20, pady=20, sticky="ne")

        widthFrame = int(self.width - 80)
        heightFrame = int(self.height - 200)
        self.scrollable_checkbox_frame = ScrollableCheckBoxFrame(master=self, width=widthFrame, height=heightFrame,
                                                                 command=self.checkbox_frame_event,
                                                                 item_list=item_list)
        self.scrollable_checkbox_frame.grid(row=1, padx=20, pady=10)

        widthButton2 = int(self.width / 2) - 80
        self.cancel_button = customtkinter.CTkButton(self, text="Cancel", width=widthButton2,
                                                     command=self.destroy)
        self.cancel_button.grid(row=2, padx=60, pady=20, sticky="nw")
        self.save_button = customtkinter.CTkButton(self, text="Ok", width=widthButton2,
                                                   command=self.confirm_save)
        self.save_button.grid(row=2, padx=60, pady=20, sticky="ne")

        self.lift()

    def check_all(self):
        self.scrollable_checkbox_frame.check_all()

    def uncheck_all(self):
        self.scrollable_checkbox_frame.uncheck_all()

    def checkbox_frame_event(self):
        list_check = self.scrollable_checkbox_frame.get_checked_items()

        return list_check

    def confirm_save(self):
        confirmation_dialog = ConfirmationDialog(self, self.save)

    def save(self):
        # Recoge los ítems seleccionados
        self.selected_items = self.scrollable_checkbox_frame.get_checked_items()
        self.callback(self.selected_items)
        self.destroy()