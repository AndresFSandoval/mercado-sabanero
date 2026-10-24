"""
Módulo: tests/test_carrito.py
Descripción: Pruebas unitarias para la Historia de Usuario HU-01 (Carrito de Compras).
Cumple strictly con:
- Patrón AAA (# Arrange, # Act, # Assert).
- Uso de unittest.mock (MagicMock) para simular ServicioInventario.
- Verificación de excepciones esperadas con pytest.raises.
- Nombres de prueba descriptivos en español.
"""

import pytest
from unittest.mock import MagicMock
from src.carrito import CarritoCompras
from src.inventario import ServicioInventario


# --- PRUEBAS CON MOCKS DE INVENTARIO (HU-01: CA1 y CA3) ---

def test_agregar_producto_con_stock_disponible_agrega_exitosamente():
    # Arrange (Preparar)
    mock_inventario = MagicMock(spec=ServicioInventario)
    mock_inventario.consultar_stock.return_value = 20  # Simula que hay 20 unidades en stock
    carrito = CarritoCompras(servicio_inventario=mock_inventario)

    # Act (Ejecutar)
    carrito.agregar_producto(
        id_producto="P01",
        nombre="Licuadora",
        precio_unitario=180000,
        cantidad=1,
        tarifa_iva=0.19
    )

    # Assert (Verificar)
    items = carrito.obtener_items()
    assert "P01" in items
    assert items["P01"]["cantidad"] == 1
    mock_inventario.consultar_stock.assert_called_once_with("P01")


def test_agregar_producto_con_stock_insuficiente_lanza_excepcion():
    # Arrange (Preparar)
    mock_inventario = MagicMock(spec=ServicioInventario)
    mock_inventario.consultar_stock.return_value = 3  # Solo hay 3 en stock
    carrito = CarritoCompras(servicio_inventario=mock_inventario)

    # Act & Assert (Ejecutar y Verificar)
    with pytest.raises(ValueError, match="Stock insuficiente para el producto solicitado."):
        carrito.agregar_producto("P03", "Aceite", 12000, 5, 0.0)

    mock_inventario.consultar_stock.assert_called_once_with("P03")


# --- PRUEBAS DE EXCEPCIÓN / LÍMITES DE CANTIDAD (HU-01: CA2) ---

def test_agregar_producto_cantidad_cero_lanza_excepcion():
    # Arrange (Preparar)
    mock_inventario = MagicMock(spec=ServicioInventario)
    carrito = CarritoCompras(servicio_inventario=mock_inventario)

    # Act & Assert (Ejecutar y Verificar)
    with pytest.raises(ValueError, match="La cantidad a agregar debe ser entre 1 y 50 unidades."):
        carrito.agregar_producto("P01", "Arroz", 4500, 0, 0.0)


def test_agregar_producto_cantidad_negativa_lanza_excepcion():
    # Arrange (Preparar)
    mock_inventario = MagicMock(spec=ServicioInventario)
    carrito = CarritoCompras(servicio_inventario=mock_inventario)

    # Act & Assert (Ejecutar y Verificar)
    with pytest.raises(ValueError, match="La cantidad a agregar debe ser entre 1 y 50 unidades."):
        carrito.agregar_producto("P01", "Arroz", 4500, -5, 0.0)


def test_agregar_producto_cantidad_mayor_a_50_lanza_excepcion():
    # Arrange (Preparar)
    mock_inventario = MagicMock(spec=ServicioInventario)
    carrito = CarritoCompras(servicio_inventario=mock_inventario)

    # Act & Assert (Ejecutar y Verificar)
    with pytest.raises(ValueError, match="La cantidad a agregar debe ser entre 1 y 50 unidades."):
        carrito.agregar_producto("P01", "Arroz", 4500, 51, 0.0)


# --- PRUEBAS DE LÍMITE Y ACUMULACIÓN DE PRODUCTOS (HU-01: CA1 y CA4) ---

def test_agregar_producto_limite_maximo_50_unidades_exitoso():
    # Arrange (Preparar)
    mock_inventario = MagicMock(spec=ServicioInventario)
    mock_inventario.consultar_stock.return_value = 100
    carrito = CarritoCompras(servicio_inventario=mock_inventario)

    # Act (Ejecutar)
    carrito.agregar_producto("P02", "Café", 15000, 50, 0.05)

    # Assert (Verificar)
    items = carrito.obtener_items()
    assert items["P02"]["cantidad"] == 50


def test_agregar_producto_existente_suma_cantidades_correctamente():
    # Arrange (Preparar)
    mock_inventario = MagicMock(spec=ServicioInventario)
    mock_inventario.consultar_stock.return_value = 10
    carrito = CarritoCompras(servicio_inventario=mock_inventario)

    # Act (Ejecutar)
    carrito.agregar_producto("P01", "Café", 15000, 2, 0.05)
    carrito.agregar_producto("P01", "Café", 15000, 3, 0.05)

    # Assert (Verificar)
    items = carrito.obtener_items()
    assert items["P01"]["cantidad"] == 5
    assert mock_inventario.consultar_stock.call_count == 2
