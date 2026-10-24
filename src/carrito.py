"""
Módulo: src/carrito.py
Descripción: Implementación de la clase CarritoCompras para cumplir HU-01.
"""


class CarritoCompras:
    def __init__(self, servicio_inventario):
        """
        Inicializa el carrito recibiendo el servicio de inventario (Inyección de Dependencias).
        """
        self.servicio_inventario = servicio_inventario
        self.items = {}  # Estructura: {id_producto: {"nombre", "precio_unitario", "cantidad", "tarifa_iva"}}

    def agregar_producto(self, id_producto: str, nombre: str, precio_unitario: int, cantidad: int, tarifa_iva: float = 0.0):
        """
        Agrega o acumula un producto en el carrito aplicando las reglas de negocio de HU-01:
        - Valida que la cantidad esté entre 1 y 50.
        - Consulta el stock externo disponible usando el servicio de inventario.
        - Suma la cantidad si el producto ya existía previamente.
        """
        # HU-01 CA2: Validar rango permitido (entre 1 y 50 unidades)
        if cantidad <= 0 or cantidad > 50:
            raise ValueError("La cantidad a agregar debe ser entre 1 y 50 unidades.")

        # HU-01 CA1/CA3: Consultar disponibilidad en el inventario externo
        stock_disponible = self.servicio_inventario.consultar_stock(id_producto)
        
        if stock_disponible < cantidad:
            raise ValueError("Stock insuficiente para el producto solicitado.")

        # HU-01 CA4: Si ya existe en el carrito, se acumulan las cantidades
        if id_producto in self.items:
            self.items[id_producto]["cantidad"] += cantidad
        else:
            self.items[id_producto] = {
                "id_producto": id_producto,
                "nombre": nombre,
                "precio_unitario": precio_unitario,
                "cantidad": cantidad,
                "tarifa_iva": tarifa_iva
            }

    def obtener_items(self) -> dict:
        """
        Devuelve todos los productos registrados en el carrito.
        """
        return self.items

    def calcular_subtotal(self) -> int:
        """
        Calcula la suma básica de (precio_unitario * cantidad) redondeado al peso más cercano.
        """
        subtotal = sum(item["precio_unitario"] * item["cantidad"] for item in self.items.values())
        return round(subtotal)
