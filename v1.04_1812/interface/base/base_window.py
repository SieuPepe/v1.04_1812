"""
Clase base para todas las ventanas del sistema.

Elimina duplicación del método cancel() presente en 21 archivos.
"""
import customtkinter


class BaseWindow(customtkinter.CTkToplevel):
    """
    Ventana base para todos los diálogos del sistema.

    Proporciona funcionalidad común como el método cancel()
    que estaba duplicado en 21 archivos diferentes.
    """

    def __init__(self, master, title="Window", **kwargs):
        """
        Inicializa la ventana base.

        Args:
            master: Ventana padre
            title: Título de la ventana
            **kwargs: Argumentos adicionales para CTkToplevel
        """
        super().__init__(master, **kwargs)
        self.title(title)

    def cancel(self):
        """
        Cierra la ventana.

        Este método estaba duplicado en 21 archivos:
        - customer_add_interfaz.py
        - customer_mod_interfaz.py
        - item_aux_add_interfaz.py
        - item_budget_add_interfaz.py
        - ... y 17 más
        """
        self.destroy()


class BaseMainWindow(customtkinter.CTk):
    """
    Ventana principal base para ventanas CTk (no Toplevel).

    Para ventanas principales como AppManager, AppUserProject, etc.
    """

    def __init__(self, title="Application", **kwargs):
        """
        Inicializa la ventana principal.

        Args:
            title: Título de la ventana
            **kwargs: Argumentos adicionales para CTk
        """
        super().__init__(**kwargs)
        self.title(title)
