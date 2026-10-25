"""Interfaz de consola para el carrito y la liquidacion de compras."""

from src.carrito import CarritoCompras
from src.liquidacion import LiquidadorCompra


class InventarioDemostracion:
    """Inventario local de demostracion: ofrece 50 unidades por producto."""

    def __init__(self):
        self.unidades_vendidas = {}

    def consultar_stock(self, id_producto: str) -> int:
        return 50 - self.unidades_vendidas.get(id_producto, 0)

    def registrar_agregado(self, id_producto: str, cantidad: int) -> None:
        self.unidades_vendidas[id_producto] = (
            self.unidades_vendidas.get(id_producto, 0) + cantidad
        )


def leer_entero(mensaje: str, minimo: int = 0) -> int:
    while True:
        try:
            valor = int(input(mensaje).strip())
        except ValueError:
            print("Ingresa un numero entero.")
            continue

        if valor < minimo:
            print(f"El valor debe ser mayor o igual a {minimo}.")
            continue
        return valor


def leer_iva() -> float:
    while True:
        try:
            porcentaje = float(input("Tarifa de IVA (porcentaje, por ejemplo 19): ").strip().replace(",", "."))
        except ValueError:
            print("Ingresa un porcentaje numerico entre 0 y 100.")
            continue

        if not 0 <= porcentaje <= 100:
            print("La tarifa de IVA debe estar entre 0 y 100.")
            continue
        return porcentaje / 100


def leer_si_no(mensaje: str) -> bool:
    while True:
        respuesta = input(mensaje).strip().lower()
        if respuesta in ("s", "si", "sí"):
            return True
        if respuesta in ("n", "no"):
            return False
        print("Responde si o no.")


def formato_pesos(valor: int) -> str:
    return f"${valor:,.0f}".replace(",", ".")


def main() -> None:
    inventario = InventarioDemostracion()
    carrito = CarritoCompras(inventario)
    liquidador = LiquidadorCompra()

    print("=== Mercado Sabanero: liquidacion de compra ===")
    print("Nota: el inventario es de demostracion, con 50 unidades por producto.")

    while True:
        print("\nIngresa los datos del producto:")
        id_producto = input("ID del producto: ").strip()
        nombre = input("Nombre: ").strip()
        if not id_producto or not nombre:
            print("El ID y el nombre no pueden estar vacios.")
            continue

        precio = leer_entero("Precio unitario en pesos: ", minimo=1)
        cantidad = leer_entero("Cantidad (de 1 a 50): ", minimo=1)
        tarifa_iva = leer_iva()

        try:
            carrito.agregar_producto(
                id_producto=id_producto,
                nombre=nombre,
                precio_unitario=precio,
                cantidad=cantidad,
                tarifa_iva=tarifa_iva,
            )
        except ValueError as error:
            print(f"No se pudo agregar el producto: {error}")
            continue

        inventario.registrar_agregado(id_producto, cantidad)
        print(f"Agregado: {cantidad} x {nombre}.")
        if not leer_si_no("Deseas agregar otro producto? (si/no): "):
            break

    if not carrito.obtener_items():
        print("No se agregaron productos; no hay una compra para liquidar.")
        return

    municipio = ""
    while not municipio:
        municipio = input("\nMunicipio de entrega: ").strip()
        if not municipio:
            print("El municipio no puede estar vacio.")

    tipo_cliente = ""
    while tipo_cliente not in ("ESTANDAR", "ORO"):
        tipo_cliente = input("Tipo de cliente (ESTANDAR/ORO): ").strip().upper()
        if tipo_cliente not in ("ESTANDAR", "ORO"):
            print("Ingresa ESTANDAR u ORO.")

    while True:
        cupon = input("Cupon (Enter si no tienes): ").strip() or None
        try:
            resultado = liquidador.liquidar(
                items=list(carrito.obtener_items().values()),
                municipio=municipio,
                cupon=cupon,
                tipo_cliente=tipo_cliente,
            )
        except ValueError as error:
            print(f"No se pudo liquidar la compra: {error}")
            continue
        break

    print("\n=== Resumen de compra ===")
    print(f"Subtotal:                 {formato_pesos(resultado['subtotal'])}")
    print(f"Descuento:                {formato_pesos(resultado['descuento_monto'])}")
    print(f"Tipo de descuento:        {resultado['descuento_aplicado_tipo']}")
    print(f"IVA:                      {formato_pesos(resultado['iva_total'])}")
    print(f"Envio:                    {formato_pesos(resultado['envio'])}")
    print(f"Total a pagar:            {formato_pesos(resultado['total_pagar'])}")
    print(f"Puntos acumulados:        {resultado['puntos']}")


if __name__ == "__main__":
    main()
