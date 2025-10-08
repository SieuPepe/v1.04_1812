import customtkinter
from PIL import Image
from tkinter import filedialog
import tkinter as tk
import ast
import base64
import shutil
import io
from io import BytesIO
import fitz  # PyMuPDF
from collections import Counter
from CTkMessagebox import CTkMessagebox
from script.modulo_db import (get_all_bd,get_option_item_bd,get_id_item_bd,get_id_item_sub_bd, add_register_item,
                              project_directory_db,get_option_item_sub_bd)
from interface.register_element_add_interfaz import AppElementAdd
import os

# Obtener la ruta actual
current_path = os.path.dirname(os.path.realpath(__file__))

# Subir un nivel en la estructura de carpetas
parent_path = os.path.dirname(current_path)

customtkinter.set_appearance_mode("dark")

class AppRegisterAdd(customtkinter.CTkToplevel):#Toplevel
    width = 800
    height = 550


    def __init__(self, select_data):
        super().__init__()
        password = select_data[1]
        user = select_data[0]
        schema = select_data[2]

        self.paths_photo = []
        self.file_paths = []
        self.photo_base64 = []
        self.pdf_base64 = []
        self.id_next = 0
        self.current_page = 0
        self.total_pages = 0


        self.title("Añadir item")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        common_fg_color = "#171717"

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #almacena codigo arqueta
        self.code_label = customtkinter.CTkLabel(self, text="CÓDIGO:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.code_label.grid(row=0, column=0, padx=(30,5), pady=(30,10), sticky= "e")
        register_data = get_all_bd(user, password, "tbl_inventario", schema)
        if len(register_data)==0:
            id_last=0
        else:
            id_last = max(sublist[0] for sublist in register_data)
        self.id_next = id_last+1
        code=f"A-{self.id_next:04d}"
        code_value=tk.StringVar(value=code)
        self.code_entry = customtkinter.CTkEntry(self, textvariable=code_value,
                                                         fg_color=common_fg_color,text_color="#FFFFFF", state="disabled")
        self.code_entry.grid(row=0, column=1, padx=(5,30), pady=(30,10), sticky= "ew")

        #almacena municipio
        self.locality_label = customtkinter.CTkLabel(self, text="MUNICIPIO:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.locality_label.grid(row=1, column=0, padx=(30,5), pady=10, sticky= "e")
        locality_value=get_option_item_bd(user, password, "tbl_municipios", schema, 'NAMEUNIT')
        locality_value.sort(key=str.lower)
        self.locality_option = customtkinter.CTkOptionMenu(self,
                                                         dynamic_resizing=False,
                                                         values=locality_value)
        self.locality_option.grid(row=1, column=1, padx=(5,5), pady=10, sticky= "ew")

        #almacena descripción
        self.description_label = customtkinter.CTkLabel(self, text="DESCRIPCIÓN:",
                                                         anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                         width= 50)
        self.description_label.grid(row=2, column=0, padx=(30,5), pady=10, sticky= "e")
        self.description_entry = customtkinter.CTkTextbox(self, fg_color=common_fg_color,
                                                        border_width=2, border_color="#565B5E",text_color="#FFFFFF")
        self.description_entry.grid(row=2, column=1, padx=(5,30), pady=10, sticky= "ew")

        # almacena elementos
        self.elements_register_label = customtkinter.CTkLabel(self, text="ELEMENTOS DE LA ARQUETA:",
                                                        anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                        width=50)
        self.elements_register_label.grid(row=3, column=0, padx=(30, 5), pady=10, sticky="e")
        self.elements_register_button = customtkinter.CTkButton(self, text="Añadir elementos",
                                                             command=lambda:self.add_element_data(select_data), width=50)
        self.elements_register_button.grid(row=3, column=1, padx=(5,30), pady=10, sticky= "ew")

        # añadir fotos
        self.photos_register_label = customtkinter.CTkLabel(self, text="FOTOGRAFIAS:",
                                                        anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                        width=50)
        self.photos_register_label.grid(row=4, column=0, padx=(30, 5), pady=10, sticky="e")
        self.photos_register_button = customtkinter.CTkButton(self, text="Añadir fotos",
                                                             command=self.add_photo_data, width=50)
        self.photos_register_button.grid(row=4, column=1, padx=(5,30), pady=10, sticky= "ew")

        # añadir documentacion
        self.documents_register_label = customtkinter.CTkLabel(self, text="DOCUMENTACIÓN:",
                                                        anchor="e", font=customtkinter.CTkFont(size=15, weight="bold"),
                                                        width=50)
        self.documents_register_label.grid(row=5, column=0, padx=(30, 5), pady=10, sticky="e")
        self.documents_register_button = customtkinter.CTkButton(self, text="Añadir documentación (max 3.5MB)",
                                                             command=self.add_document_data, width=50)
        self.documents_register_button.grid(row=5, column=1, padx=(5,30), pady=10, sticky= "ew")

        # boton de guardar
        save_path = parent_path +"/source/guardar.png"
        self.save_image = customtkinter.CTkImage(Image.open(save_path))
        self.save_button = customtkinter.CTkButton(self, text="Guardar",image=self.save_image, compound="left",fg_color="green",
                                                   font=("default", 14, "bold"),
                                                   command=lambda: self.save(select_data),  height=40)
        self.save_button.grid(row=6, column=0, padx=(30,1), pady=10, sticky= "ew")

        # boton de cancelar
        cancel_path = parent_path +"/source/cancelar.png"
        self.cancel_image = customtkinter.CTkImage(Image.open(cancel_path))
        self.cancel_button = customtkinter.CTkButton(self, text="Cancelar",image=self.cancel_image, compound="left",fg_color="red",
                                                   font=("default", 14, "bold"),
                                                   command=self.cancel,  height=40)
        self.cancel_button.grid(row=6, column=1, padx=(10,30), pady=10, sticky= "ew")
        self.lift()

    def add_element_data(self, select_data):
        appAux = AppElementAdd(select_data)
        appAux.grab_set()
        self.wait_window(appAux)  # Esperar a que se cierre la ventana secundaria
        self.items_hidro, self.items_register = appAux.get_items()
        CTkMessagebox(title="Successfull Message!",
                      message="Se han agregado los elementos hidráulicos y no hidráulicos de la arqueta",
                      icon="check")


    def add_photo_data(self):
        # abrir cuadro de dialogo para seleccionar la imagen
        self.paths_photo = filedialog.askopenfilenames(
            title="Selecciona una imagen",
            filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if len(self.paths_photo)>0:
            for path in self.paths_photo:
                # Cargar la imagen seleccionada
                imagen = Image.open(path)
                original_width, original_height = imagen.size
                # Calcular el nuevo ancho manteniendo la proporción
                aspect_ratio = original_width / original_height
                new_width = int(200* aspect_ratio)
                imagen = imagen.resize((new_width, 200))
                # Convertir la imagen a un objeto BytesIO
                buffered = BytesIO()
                imagen.save(buffered, format="PNG")
                # Codificar la imagen a Base64
                image_base64 = base64.b64encode(buffered.getvalue()).decode()
                self.photo_base64.append(image_base64)
            CTkMessagebox(title="Successfull Message!", message="Se han subido "+str(len(self.photo_base64))+" fotografias al registro",
                          icon="check")

        else:
            CTkMessagebox(title="Warning Message!", message="No se ha seleccionado ningún archivo",
                          icon="warning")


    def add_document_data(self):
        self.file_paths = filedialog.askopenfilenames(title="Seleccionar PDFs",
                                                 filetypes=[("Archivos PDF", "*.pdf")])
        if self.file_paths:
            for file_path in self.file_paths:
                file_size = os.path.getsize(file_path)  # Obtener el tamaño del archivo en bytes
                # Comprobar si el archivo supera 3.5 MB (3,500,000 bytes)
                if file_size > 3500000:
                    CTkMessagebox(title="Error",
                                  message=f"El archivo {os.path.basename(file_path)} supera los 3.5 MB y no se puede subir.",
                                  icon="warning")
                    continue  # Saltar este archivo y pasar al siguiente
                else:
                    # Cargar el PDF completo
                    self.load_pdf_document(file_path)
                    pdf_pages=[]
                    for i in range(self.total_pages):
                        base64_page=self.convert_page(i)
                        pdf_pages.append(base64_page)
                    self.pdf_base64.append(pdf_pages)

            CTkMessagebox(title="Successfull Message!",
                                      message="Se han subido " + str(len(self.pdf_base64)) + " PDFs al registro",
                                      icon="check")
        else:
            CTkMessagebox(title="Warning Message!", message="No se ha seleccionado ningún archivo",
                              icon="warning")


    def load_pdf_document(self, file_path):
        # Cargar el documento PDF completo
        self.pdf_document = fitz.open(file_path)
        self.total_pages = self.pdf_document.page_count  # Total de páginas
        self.current_page = 0  # Comenzar desde la primera página


    def convert_page(self, page_num):
        if self.pdf_document:
            # Asegurarse de que el número de página esté en el rango correcto
            if 0 <= page_num < self.total_pages:
                page = self.pdf_document.load_page(page_num)

                # Convertir la página a una imagen (pixmap)
                pix = page.get_pixmap()

                # Convertir la imagen a un objeto PIL para mostrarla en tkinter
                image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                # Convertir la imagen a base64 y agregarla a la lista
                base64=self.save_image_as_base64(image)

                return base64


    def save_image_as_base64(self, image):
        #Convierte la imagen PIL a base64 y la guarda en una lista.
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")  # Guardar la imagen en el buffer en formato PNG
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        return img_base64


    def cancel(self):
        self.destroy()


    def save(self, select_data):
        id_project=get_id_item_bd(select_data[0], select_data[1], "tbl_proyectos", select_data[2],
                                        "codigo", select_data[2])
        code_value = self.code_entry.get()
        id_locality= get_id_item_bd(select_data[0], select_data[1], "tbl_municipios", select_data[2],
                                        "NAMEUNIT", self.locality_option.get())
        description = self.description_entry.get("1.0", "end-1c")
        items_hidro = getattr(self, 'items_hidro', [])
        items_register = getattr(self, 'items_register', [])
        # Asegurarse de que path_img y path_pdf existan
        path_img = getattr(self, 'paths_photo', [])  # Si no existe, inicializa vacía
        img_64 = getattr(self, 'photo_base64', [])  # Si no existe, inicializa vacía
        path_pdf = getattr(self, 'file_paths', [])  # Si no existe, inicializa vacía
        pdf_64 = getattr(self, 'pdf_base64', [])  # Si no existe, inicializa vacía

        data_inventory=[code_value,id_project,id_locality,description]

        rel_budget_hidro = []
        data_element_hidro = []
        data_element_budget_hidro = []
        data_no_budget_hidro=[]
        if len(items_hidro)!=0:
            list_items = [ast.literal_eval(item) for item in items_hidro]
            for item in list_items:
                sub_data=[]
                id_type=2
                id_project_item=id_project
                id_inventory=self.id_next
                n_line=int(item[1].replace("L-",""))
                if item[3]=='input':
                    connection=0
                else:
                    position=str(item[3])
                    position=position[0:2]
                    connection=next((i+1 for i, item in enumerate(list_items) if position in item), None)
                n_order=int(item[0].replace("P",""))
                id_type_element=get_id_item_bd(select_data[0], select_data[1], "tbl_cata_hidra_tipo", select_data[2],
                                            "tipo_elemento", item[4])
                model=item[2].replace(item[1]+"_","")
                id_catalog_element=get_id_item_sub_bd(select_data[0], select_data[1], "tbl_catalogo_hidraulica", select_data[2], "id_tipo_hidraulica",str(id_type_element),"modelo",model)
                if item[5] == 'Nueva':
                    status_element = 0
                else:
                    status_element = 1
                id_orientation = get_id_item_bd(select_data[0], select_data[1], "tbl_inv_orientacion", select_data[2],
                                                 "orientacion", item[6])
                id_material = get_id_item_bd(select_data[0], select_data[1], "tbl_inv_material", select_data[2],
                                                 "material", item[7])
                sub_data.append(id_type)
                sub_data.append(id_project_item)
                sub_data.append(id_inventory)
                sub_data.append(n_line)
                sub_data.append(connection)
                sub_data.append(id_type_element)
                sub_data.append(id_catalog_element)
                sub_data.append(n_order)
                sub_data.append(status_element)
                sub_data.append(id_orientation)
                sub_data.append(id_material)
                data_element_hidro.append(sub_data)
                cod_budget = get_option_item_sub_bd(select_data[0], select_data[1], "tbl_catalogo_hidraulica", select_data[2],
                                       "cod_partida", id_catalog_element, "id")
                if status_element == 0:
                    if cod_budget[0] == '-':
                        data_no_budget_hidro.append(model)
                    else:
                        rel_budget_hidro.append(id_catalog_element)

            sum_budget_hidro = Counter(rel_budget_hidro)
            for key, value in sum_budget_hidro.items():
                cod_budget = get_option_item_sub_bd(select_data[0], select_data[1], "tbl_catalogo_hidraulica", select_data[2], "cod_partida", key , "id")
                id_budget =  get_id_item_bd(select_data[0], select_data[1], "tbl_pres_precios", select_data[2], "codigo", cod_budget[0])
                data_element_budget_hidro.append([id_budget,value,id_project,self.id_next,0])

        sum_budget_regis = {}
        data_element_register = []
        data_element_budget_regis = []
        data_no_budget_regis = []
        if len(items_register)!=0:
            list_items = [ast.literal_eval(item) for item in items_register]
            for item in list_items:
                sub_data = []
                id_type = 1
                id_project_item = id_project
                id_inventory = self.id_next
                id_type_element = get_id_item_bd(select_data[0], select_data[1], "tbl_cata_regis_tipo", select_data[2],
                                                 "tipo", item[2])
                model=item[0]
                id_catalog_element=get_id_item_sub_bd(select_data[0], select_data[1], "tbl_catalogo_registros", select_data[2], "id_tipo_registro",str(id_type_element),"modelo",model)
                n_element=int(item[1].replace(" ud","").replace("s",""))
                sub_data.append(id_type)
                sub_data.append(id_project_item)
                sub_data.append(id_inventory)
                sub_data.append(n_element)
                sub_data.append(id_type_element)
                sub_data.append(id_catalog_element)
                data_element_register.append(sub_data)
                cod_budget = get_option_item_sub_bd(select_data[0], select_data[1], "tbl_catalogo_registros", select_data[2], "cod_partida", id_catalog_element, "id")
                if cod_budget[0] == '-':
                    data_no_budget_regis.append(model)
                else:
                    sum_budget_regis[id_catalog_element] = n_element

            for key, value in sum_budget_regis.items():
                cod_budget = get_option_item_sub_bd(select_data[0], select_data[1], "tbl_catalogo_registros", select_data[2], "cod_partida", key , "id")
                id_budget =  get_id_item_bd(select_data[0], select_data[1], "tbl_pres_precios", select_data[2], "codigo", cod_budget[0])
                data_element_budget_regis.append([id_budget,value,id_project,self.id_next,0])

        data_photo = []
        if len(path_img)!=0 and len(img_64)!=0:
            list_items=list(zip(path_img,img_64))
            for item in list_items:
                sub_data = []
                id_type = 2
                id_project_item = id_project
                id_inventory = self.id_next
                item_base64=item[1]
                item_path=item[0]
                sub_data.append(id_project_item)
                sub_data.append(id_inventory)
                sub_data.append(id_type)
                sub_data.append(item_base64)
                sub_data.append(item_path)
                data_photo.append(sub_data)

        data_pdf = []
        if len(path_pdf)!=0 and len(pdf_64)!=0:
            list_items=list(zip(path_pdf,pdf_64))
            for item in list_items:
                sub_data = []
                id_project_item = id_project
                id_inventory = self.id_next
                item_base64=str(item[1])
                item_path=item[0]
                sub_data.append(id_project_item)
                sub_data.append(id_inventory)
                sub_data.append(item_base64)
                sub_data.append(item_path)
                data_pdf.append(sub_data)

        data_no_budget = data_no_budget_hidro+data_no_budget_regis

        try:
            #copiamos en la carpeta 02.salidas las plantillas con la nomenclatura establecida
            #recolectamoscodigos de nomenclatura
            site = self.locality_option.get()
            site = site[0:3].upper()
            code_string = code_value.replace("-","")
            schema = select_data[2]
            #consultamos directorio de proyecto
            project_directory = project_directory_db(select_data[0], select_data[1],select_data[2])
            project_directory = str(project_directory[0])
            #definimos rutas de los archivos originales
            site_original = "DC_GRAFICA/CAD/zz.plantillas/XXXXX-ARTA-YYY-ZZZZZ-PLA-RED-01-SituacionYEmplaz-R01.dwg"
            geometry_original = "DC_GRAFICA/CAD/zz.plantillas/XXXXX-ARTA-YYY-ZZZZZ-PLA-RED-02-GeometriaYmateri-R01.dwg"
            site_original_path = project_directory+'/'+site_original
            geometry_original_path = project_directory+'/'+geometry_original
            #definimos rutas de los archivos nuevos
            site_name=os.path.basename(site_original_path).replace("XXXXX",schema).replace("YYY",site).replace("ZZZZZ",code_string)
            geometry_name = os.path.basename(geometry_original_path).replace("XXXXX",schema).replace("YYY",site).replace("ZZZZZ",code_string)
            output_directory  = "DC_GRAFICA/CAD/02.salidas"
            site_destination_path = project_directory+'/'+output_directory+'/'+site_name
            geometry_destination_path = project_directory+'/'+output_directory+'/'+geometry_name
            #confirmamos que existe el directorio donde se copiaran los archivos
            if not os.path.exists(project_directory+'/'+output_directory):
                os.makedirs(project_directory+'/'+output_directory)
            #copiamoslos archivos
            shutil.copy(site_original_path, site_destination_path)
            shutil.copy(geometry_original_path, geometry_destination_path)

            #añadimos registro en la bbdd
            result=add_register_item(select_data[0], select_data[1],select_data[2],data_inventory,data_pdf,data_photo,data_element_hidro,data_element_register, data_element_budget_hidro,data_element_budget_regis)

            if len(data_no_budget) != 0:
                mssg = "Los siguientes elementos no tienen asociado una partrida y no se pueden asignar al presupuesto: \n"  + "\n".join(data_no_budget)
                CTkMessagebox(title="Error Message!", message=mssg,
                              icon="cancel")

            if result == 'ok':
                mssg = "Se ha añadido el registro a la base de datos "
                self.destroy()
                CTkMessagebox(title="Successfull Message!", message=mssg,
                              icon="check")
            else:
                mssg = "ERROR: " + str(result)
                self.destroy()
                CTkMessagebox(title="Error Message!", message=mssg,
                              icon="cancel")

        except Exception as e:
            mssg = f"Error al copiar o abrir el archivo: {e}"
            CTkMessagebox(title="Warning Message!", message=mssg,
                          icon="warning")
