import customtkinter
from CTkMessagebox import CTkMessagebox
from interface.item_budget_mod_interfaz import AppItemBudgetMod
from interface.item_budget_add_interfaz import AppItemBudgetAdd
from interface.item_budget_sub_interfaz import AppGroupBudgetAdd
from interface.select_group_budget_interfaz import AppSelectGroup
from script.modulo_db import get_all_bd

customtkinter.set_appearance_mode("dark")


class AppBudgetUpdate(customtkinter.CTkToplevel):

    def __init__(self, select_data):
        super().__init__()
        self.title("Modificar presupuesto")
        self.geometry("750x150")
        self.resizable(False, False)
        self.attributes('-topmost', True)

        self.label = customtkinter.CTkLabel(self, text="Seleccione la operación para modificar el presupuesto")
        self.label.pack(pady=(30,10))


        self.mod_button = customtkinter.CTkButton(self, text="Modificar partida",
                                                            font=customtkinter.CTkFont(size=13, weight="bold"),
                                                            command=lambda :self.mod_event(select_data), width=100)
        self.mod_button.pack(side="left", expand=True, padx=10)

        self.add_button = customtkinter.CTkButton(self, text="Añadir partida",
                                                            font=customtkinter.CTkFont(size=13, weight="bold"),
                                                            command=lambda: self.add_event(select_data), width=100)
        self.add_button.pack(side="left", expand=True, padx=10)

        self.mod_group_button = customtkinter.CTkButton(self, text="Modificar grupo de partidas",
                                                            font=customtkinter.CTkFont(size=13, weight="bold"),
                                                            command=lambda: self.mod_group_event(select_data),width=100)
        self.mod_group_button.pack(side="right", expand=True, padx=10)

        self.create_button = customtkinter.CTkButton(self, text="Crear grupo de partidas",
                                                            font=customtkinter.CTkFont(size=13, weight="bold"),
                                                            command=lambda: self.create_event(select_data),width=100)
        self.create_button.pack(side="right", expand=True, padx=10)

        self.lift()


    def mod_event(self,select_data):
        self.withdraw()
        appAux = AppItemBudgetMod(select_data)
        appAux.grab_set()
        self.wait_window(appAux)
        self.deiconify()


    def add_event(self,select_data):
        self.withdraw()
        appAux = AppItemBudgetAdd(select_data)
        appAux.grab_set()
        self.wait_window(appAux)
        self.deiconify()


    def create_event(self,select_data):
        self.withdraw()
        appAux = AppGroupBudgetAdd(select_data)
        appAux.grab_set()
        self.wait_window(appAux)
        self.deiconify()


    def mod_group_event(self,select_data):
        n_group=len(get_all_bd(select_data[0], select_data[1], "tbl_pres_grupo_partidas", select_data[2]))
        print(n_group)
        if n_group==0:
            CTkMessagebox(title="Warning Message!", message=f"Error: No hay grupos de partidas para modificar",
                          icon="warning")
        else:
            self.withdraw()
            appAux = AppSelectGroup(select_data)
            appAux.grab_set()
            self.wait_window(appAux)
            self.deiconify()





