"""
Módulo: src/inventario.py
Descripción: Servicio externo de consulta de inventario.
Propósito en TDD: Actúa como la interfaz del sistema externo. 
En las pruebas unitarias se reemplaza por un Doble de Prueba (Mock).
"""


class ServicioInventario:
    def consultar_stock(self, id_producto: str) -> int:
        """
        Consulta la cantidad disponible de un producto en la base de datos central o API.
        Lanza NotImplementedError porque en pruebas unitarias debe ser MOCKEADO.
        """
        raise NotImplementedError("El servicio real no está conectado. Debe usar un Mock en pruebas unitarias.")
