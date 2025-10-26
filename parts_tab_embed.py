import customtkinter
from tkinter import ttk
from script.modulo_db import get_parts_list

class PartsTab(customtkinter.CTkFrame):
    def __init__(self, master, user, password, schema, **kwargs):
        super().__init__(master, **kwargs)
        self.user = user
        self.password = password
        self.schema = schema
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        lbl = customtkinter.CTkLabel(self, text="Listado de partes", font=("",16,"bold"))
        lbl.pack(pady=(10,5))
        cols = ("id","codigo","ot","red","tipo","cod_trabajo","descripcion","created_at")
        frame = customtkinter.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", height=15)
        for c, w in zip(cols, (60,110,120,120,120,140,300,180)):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w, anchor="w")
        yscroll = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscroll.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self.btn_reload = customtkinter.CTkButton(self, text="Recargar", command=self._load_data)
        self.btn_reload.pack(pady=(0,10))

    def _load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        rows = get_parts_list(self.user, self.password, self.schema, limit=200)
        for r in rows:
            r2 = list(r)
            if len(r2) > 7 and r2[7] is not None:
                r2[7] = str(r2[7])
            self.tree.insert("", "end", values=r2)

if __name__ == "__main__":
    import customtkinter
    app = customtkinter.CTk()
    app.title("HydroFlow Manager - Partes (embebido)")
    app.geometry("1200x600")
    tab = PartsTab(app, "aperez", "WGueXNk9", "cert_dev")
    tab.pack(fill="both", expand=True)
    app.mainloop()