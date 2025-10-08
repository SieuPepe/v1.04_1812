import customtkinter
from interface.item_budget_sub_interfaz import AppItemGroupBudgetMod
from script.modulo_db  import get_all_bd


customtkinter.set_appearance_mode("dark")

class AppSelectGroup(customtkinter.CTkToplevel):
    width = 400
    height = 200

    def __init__(self, select_data):
        super().__init__()

        self.title("HydroFlow Manager")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        password = select_data[1]
        user = select_data[0]
        schema = select_data[2]

        self.grid_columnconfigure(0,weight=1)
        self.select_label = customtkinter.CTkLabel(self,
                                                         text="SELECCIONAR GRUPO DE PARTIDAS",
                                                         anchor="center", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width=50)
        self.select_label.grid(row=0, padx=(30, 30), pady=(30,10), sticky="news")

        #crea seleccionable para elegir grupo de partida
        group_items = get_all_bd(user, password, "tbl_pres_grupo_partidas", schema)
        group_items_filter = [elemento[1]+" - "+elemento[4] for elemento in group_items]
        self.group_option = customtkinter.CTkOptionMenu(self,
                                                           dynamic_resizing=False,
                                                           values=group_items_filter)
        self.group_option.grid(row=1,  padx=(30,30), pady=(10,30), sticky= "news")

        self.ok_button = customtkinter.CTkButton(self, text="Abrir grupo de partidas", command=lambda:self.group_event(select_data), width=200)
        self.ok_button.grid(row=2, padx=(30,30), pady=(10,30), sticky= "news")
      

    def group_event(self, select_data):
        code_group=self.group_option.get()
        code_group=code_group.split(" - ")[0]
        self.withdraw()
        appAux = AppItemGroupBudgetMod(select_data,code_group)
        appAux.grab_set()
        self.wait_window(appAux)
        self.deiconify()

