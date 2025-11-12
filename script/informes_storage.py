# script/informes_storage.py
"""
Módulo para guardar y cargar configuraciones de informes
"""

import json
import os
from datetime import datetime


class InformesConfigStorage:
    """Gestor de almacenamiento de configuraciones de informes"""

    def __init__(self, storage_dir="informes_guardados"):
        """
        Inicializa el gestor de almacenamiento

        Args:
            storage_dir: Directorio donde se guardarán las configuraciones
        """
        self.storage_dir = storage_dir
        self.auto_save_dir = os.path.join(storage_dir, "auto_save")
        self._ensure_storage_dir()
        self._ensure_auto_save_dir()

    def _ensure_auto_save_dir(self):
        """Crea el directorio de auto-guardado si no existe"""
        if not os.path.exists(self.auto_save_dir):
            os.makedirs(self.auto_save_dir)

    def _ensure_storage_dir(self):
        """Crea el directorio de almacenamiento si no existe"""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

    def guardar_configuracion(self, nombre, informe_nombre, filtros, ordenaciones, campos_seleccionados, descripcion=""):
        """
        Guarda una configuración de informe

        Args:
            nombre: Nombre de la configuración (será el nombre del archivo)
            informe_nombre: Nombre del informe base
            filtros: Lista de filtros aplicados
            ordenaciones: Lista de ordenaciones aplicadas
            campos_seleccionados: Lista de campos seleccionados
            descripcion: Descripción opcional de la configuración

        Returns:
            bool: True si se guardó correctamente, False en caso de error
        """
        try:
            configuracion = {
                "nombre": nombre,
                "descripcion": descripcion,
                "informe_base": informe_nombre,
                "filtros": filtros,
                "ordenaciones": ordenaciones,
                "campos_seleccionados": campos_seleccionados,
                "fecha_creacion": datetime.now().isoformat(),
                "fecha_modificacion": datetime.now().isoformat(),
                "version": "1.0"
            }

            # Generar nombre de archivo seguro
            filename = self._generar_nombre_archivo(nombre)
            filepath = os.path.join(self.storage_dir, filename)

            # Guardar como JSON
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(configuracion, f, indent=2, ensure_ascii=False)

            print(f"✅ Configuración guardada: {filepath}")
            return True

        except Exception as e:
            print(f"❌ Error al guardar configuración: {e}")
            return False

    def cargar_configuracion(self, nombre):
        """
        Carga una configuración guardada

        Args:
            nombre: Nombre de la configuración (o nombre de archivo)

        Returns:
            dict: Configuración cargada o None si hay error
        """
        try:
            filename = self._generar_nombre_archivo(nombre)
            filepath = os.path.join(self.storage_dir, filename)

            if not os.path.exists(filepath):
                print(f"❌ Configuración no encontrada: {nombre}")
                return None

            with open(filepath, 'r', encoding='utf-8') as f:
                configuracion = json.load(f)

            print(f"✅ Configuración cargada: {nombre}")
            return configuracion

        except Exception as e:
            print(f"❌ Error al cargar configuración: {e}")
            return None

    def listar_configuraciones(self):
        """
        Lista todas las configuraciones guardadas

        Returns:
            list: Lista de diccionarios con información de configuraciones
        """
        configuraciones = []

        try:
            for filename in os.listdir(self.storage_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.storage_dir, filename)

                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            config = json.load(f)

                        configuraciones.append({
                            'nombre': config.get('nombre', filename[:-5]),
                            'descripcion': config.get('descripcion', ''),
                            'informe_base': config.get('informe_base', ''),
                            'fecha_creacion': config.get('fecha_creacion', ''),
                            'fecha_modificacion': config.get('fecha_modificacion', ''),
                            'num_filtros': len(config.get('filtros', [])),
                            'num_ordenaciones': len(config.get('ordenaciones', [])),
                            'num_campos': len(config.get('campos_seleccionados', []))
                        })
                    except:
                        # Ignorar archivos corruptos
                        continue

        except Exception as e:
            print(f"❌ Error al listar configuraciones: {e}")

        return sorted(configuraciones, key=lambda x: x['fecha_modificacion'], reverse=True)

    def eliminar_configuracion(self, nombre):
        """
        Elimina una configuración guardada

        Args:
            nombre: Nombre de la configuración

        Returns:
            bool: True si se eliminó correctamente, False en caso de error
        """
        try:
            filename = self._generar_nombre_archivo(nombre)
            filepath = os.path.join(self.storage_dir, filename)

            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"✅ Configuración eliminada: {nombre}")
                return True
            else:
                print(f"❌ Configuración no encontrada: {nombre}")
                return False

        except Exception as e:
            print(f"❌ Error al eliminar configuración: {e}")
            return False

    def actualizar_configuracion(self, nombre, filtros, ordenaciones, campos_seleccionados):
        """
        Actualiza una configuración existente

        Args:
            nombre: Nombre de la configuración
            filtros: Nuevos filtros
            ordenaciones: Nuevas ordenaciones
            campos_seleccionados: Nuevos campos seleccionados

        Returns:
            bool: True si se actualizó correctamente, False en caso de error
        """
        try:
            # Cargar configuración existente
            config = self.cargar_configuracion(nombre)
            if not config:
                return False

            # Actualizar datos
            config['filtros'] = filtros
            config['ordenaciones'] = ordenaciones
            config['campos_seleccionados'] = campos_seleccionados
            config['fecha_modificacion'] = datetime.now().isoformat()

            # Guardar de nuevo
            filename = self._generar_nombre_archivo(nombre)
            filepath = os.path.join(self.storage_dir, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            print(f"✅ Configuración actualizada: {nombre}")
            return True

        except Exception as e:
            print(f"❌ Error al actualizar configuración: {e}")
            return False

    def exportar_configuracion(self, nombre, destino):
        """
        Exporta una configuración a un archivo específico

        Args:
            nombre: Nombre de la configuración
            destino: Ruta del archivo destino

        Returns:
            bool: True si se exportó correctamente, False en caso de error
        """
        try:
            config = self.cargar_configuracion(nombre)
            if not config:
                return False

            with open(destino, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            print(f"✅ Configuración exportada a: {destino}")
            return True

        except Exception as e:
            print(f"❌ Error al exportar configuración: {e}")
            return False

    def importar_configuracion(self, origen):
        """
        Importa una configuración desde un archivo

        Args:
            origen: Ruta del archivo origen

        Returns:
            bool: True si se importó correctamente, False en caso de error
        """
        try:
            with open(origen, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # Guardar en el storage
            nombre = config.get('nombre', 'Configuración Importada')
            return self.guardar_configuracion(
                nombre,
                config.get('informe_base', ''),
                config.get('filtros', []),
                config.get('ordenaciones', []),
                config.get('campos_seleccionados', []),
                config.get('descripcion', '')
            )

        except Exception as e:
            print(f"❌ Error al importar configuración: {e}")
            return False

    def _generar_nombre_archivo(self, nombre):
        """
        Genera un nombre de archivo seguro a partir del nombre de la configuración

        Args:
            nombre: Nombre de la configuración

        Returns:
            str: Nombre de archivo seguro
        """
        # Eliminar caracteres no válidos
        nombre_limpio = "".join(c for c in nombre if c.isalnum() or c in (' ', '-', '_')).strip()
        nombre_limpio = nombre_limpio.replace(' ', '_')

        # Asegurar extensión .json
        if not nombre_limpio.endswith('.json'):
            nombre_limpio += '.json'

        return nombre_limpio

    def auto_guardar_informe(self, informe_nombre, filtros, ordenaciones, campos_seleccionados, agrupaciones=None, agregaciones=None, modo_visualizacion="detalle"):
        """
        Guarda automáticamente la configuración actual de un informe
        Esta configuración se carga automáticamente al seleccionar el informe

        Args:
            informe_nombre: Nombre del informe (ej: "Listado de Partes")
            filtros: Lista de filtros aplicados
            ordenaciones: Lista de ordenaciones aplicadas
            campos_seleccionados: Lista de campos seleccionados
            agrupaciones: Lista de agrupaciones (opcional)
            agregaciones: Lista de agregaciones (opcional)
            modo_visualizacion: Modo de visualización ("detalle" o "resumen")

        Returns:
            bool: True si se guardó correctamente
        """
        try:
            configuracion = {
                "informe_nombre": informe_nombre,
                "filtros": filtros,
                "ordenaciones": ordenaciones,
                "campos_seleccionados": campos_seleccionados,
                "agrupaciones": agrupaciones or [],
                "agregaciones": agregaciones or [],
                "modo_visualizacion": modo_visualizacion,
                "fecha_modificacion": datetime.now().isoformat()
            }

            # Generar nombre de archivo basado en el nombre del informe
            filename = self._generar_nombre_archivo(f"autosave_{informe_nombre}")
            filepath = os.path.join(self.auto_save_dir, filename)

            # Guardar como JSON
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(configuracion, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            print(f"⚠ Error al auto-guardar configuración de '{informe_nombre}': {e}")
            return False

    def auto_cargar_informe(self, informe_nombre):
        """
        Carga automáticamente la última configuración guardada de un informe

        Args:
            informe_nombre: Nombre del informe

        Returns:
            dict: Configuración cargada o None si no existe
        """
        try:
            filename = self._generar_nombre_archivo(f"autosave_{informe_nombre}")
            filepath = os.path.join(self.auto_save_dir, filename)

            if not os.path.exists(filepath):
                return None

            with open(filepath, 'r', encoding='utf-8') as f:
                configuracion = json.load(f)

            return configuracion

        except Exception as e:
            print(f"⚠ Error al auto-cargar configuración de '{informe_nombre}': {e}")
            return None
