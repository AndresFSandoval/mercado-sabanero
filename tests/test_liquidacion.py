"""
Módulo: tests/test_liquidacion.py
Descripción: Pruebas unitarias automatizadas para HU-02 a HU-06.
Cumple con:
- Patrón AAA (# Arrange, # Act, # Assert) en el 100% de las pruebas.
- Pruebas parametrizadas (@pytest.mark.parametrize) para tramos de descuento y límites.
- Verificación de excepciones (pytest.raises).
- Inclusión exacta del Caso de Ejemplo Obligatorio de la Guía.
"""

import pytest
from src.liquidacion import LiquidadorCompra


# --- HU-03: PRUEBAS PARAMETRIZADAS DE DESCUENTO POR VOLUMEN ---

@pytest.mark.parametrize(
    "subtotal, descuento_esperado_porcentaje",
    [
        (199999, 0.0),   # Límite superior sin descuento
        (200000, 0.05),  # Límite inferior descuento 5%
        (499999, 0.05),  # Límite superior descuento 5%
        (500000, 0.10),  # Límite inferior descuento 10%
        (800000, 0.10),  # Valor superior descuento 10%
    ]
)
def test_calcular_porcentaje_descuento_volumen(subtotal, descuento_esperado_porcentaje):
    # Arrange
    liquidador = LiquidadorCompra()

    # Act
    porcentaje = liquidador.obtener_porcentaje_descuento_volumen(subtotal)

    # Assert
    assert porcentaje == descuento_esperado_porcentaje


# --- HU-04: PRUEBAS DE CUPONES Y REGLA DE NO ACUMULACIÓN ---

def test_cupon_sabanero10_subtotal_insuficiente_lanza_excepcion():
    # Arrange
    liquidador = LiquidadorCompra()

    # Act & Assert
    with pytest.raises(ValueError, match="El cupón SABANERO10 requiere un subtotal mínimo de \$50\.000\."):
        liquidador.validar_y_obtener_descuento_cupon("SABANERO10", subtotal=49999)


def test_cupon_sabanero10_subtotal_exacto_50000_aplica_10_porciento():
    # Arrange
    liquidador = LiquidadorCompra()

    # Act
    descuento_porcentaje = liquidador.validar_y_obtener_descuento_cupon("SABANERO10", subtotal=50000)

    # Assert
    assert descuento_porcentaje == 0.10


def test_cupon_inexistente_o_vencido_lanza_excepcion():
    # Arrange
    liquidador = LiquidadorCompra()

    # Act & Assert
    with pytest.raises(ValueError, match="Cupón inválido o vencido."):
        liquidador.validar_y_obtener_descuento_cupon("CUPON_FALSO", subtotal=100000)


def test_no_acumulacion_aplica_solo_descuento_mayor_volumen_vs_cupon():
    # Arrange: Subtotal de $200.000 otorga 5% por volumen ($10.000). Cupón SABANERO10 da 10% ($20.000).
    liquidador = LiquidadorCompra()
    items = [{"precio_unitario": 200000, "cantidad": 1, "tarifa_iva": 0.0}]

    # Act
    resultado = liquidador.liquidar(
        items=items,
        municipio="Sincelejo",
        cupon="SABANERO10",
        tipo_cliente="ESTANDAR"
    )

    # Assert: Se debe aplicar solo el 10% del cupón ($20.000), no la suma (15%).
    assert resultado["descuento_monto"] == 20000
    assert resultado["descuento_aplicado_tipo"] == "CUPON"


# --- HU-05: PRUEBAS DE TARIFAS DE ENVÍO ---

@pytest.mark.parametrize(
    "municipio, suma_prod_iva, cupon, costo_envio_esperado",
    [
        ("Sincelejo", 100000, None, 8000),        # Sincelejo estándar
        ("Corozal", 100000, None, 15000),         # Municipio Sucre estándar
        ("Sincelejo", 149999, None, 8000),        # Límite inferior no alcanza envío gratis
        ("Sincelejo", 150000, None, 0),           # Límite exacto suma IVA >= $150.000 (Gratis)
        ("Corozal", 50000, "ENVIOGRATIS", 0),      # Envío gratis por cupón
    ]
)
def test_calcular_costo_envio(municipio, suma_prod_iva, cupon, costo_envio_esperado):
    # Arrange
    liquidador = LiquidadorCompra()

    # Act
    costo = liquidador.calcular_envio(
        municipio=municipio,
        suma_productos_con_iva=suma_prod_iva,
        cupon=cupon
    )

    # Assert
    assert costo == costo_envio_esperado


# --- HU-06: PRUEBAS DE ACUMULACIÓN DE PUNTOS ---

def test_acumulacion_puntos_cliente_estandar():
    # Arrange
    liquidador = LiquidadorCompra()

    # Act: Total pagado sin envío = $250.515
    puntos = liquidador.calcular_puntos(total_sin_envio=250515, tipo_cliente="ESTANDAR")

    # Assert: 1 punto por cada $1.000 completos -> 250 puntos
    assert puntos == 250


def test_acumulacion_puntos_cliente_oro_recibe_doble():
    # Arrange
    liquidador = LiquidadorCompra()

    # Act: Total pagado sin envío = $250.515, cliente ORO
    puntos = liquidador.calcular_puntos(total_sin_envio=250515, tipo_cliente="ORO")

    # Assert: Doble de puntos -> 500 puntos
    assert puntos == 500


# --- PRUEBA OBLIGATORIA DEL CASO DE EJEMPLO DE LA GUÍA ---

def test_caso_ejemplo_guia_mercado_sabanero():
    """
    Verifica exactamente el caso provisto en el enunciado de la actividad:
    - Cliente ESTÁNDAR en Sincelejo, sin cupón.
    - Compras:
      * 1 Licuadora de $180.000 (IVA 19%)
      * 2 Cafés de $15.000 (IVA 5%) -> $30.000
      * 4 Arroces de $4.500 (IVA 0%) -> $18.000
    - Resultados esperados:
      * Subtotal: $228.000
      * Descuento 5%: $11.400
      * IVA Total: $33.915
      * Envío: $0
      * Total a Pagar: $250.515
      * Puntos: 250
    """
    # Arrange
    liquidador = LiquidadorCompra()
    items = [
        {"nombre": "Licuadora", "precio_unitario": 180000, "cantidad": 1, "tarifa_iva": 0.19},
        {"nombre": "Café", "precio_unitario": 15000, "cantidad": 2, "tarifa_iva": 0.05},
        {"nombre": "Arroz", "precio_unitario": 4500, "cantidad": 4, "tarifa_iva": 0.00},
    ]

    # Act
    liquidacion = liquidador.liquidar(
        items=items,
        municipio="Sincelejo",
        cupon=None,
        tipo_cliente="ESTANDAR"
    )

    # Assert
    assert liquidacion["subtotal"] == 228000
    assert liquidacion["descuento_monto"] == 11400
    assert liquidacion["iva_total"] == 33915
    assert liquidacion["envio"] == 0
    assert liquidacion["total_pagar"] == 250515
    assert liquidacion["puntos"] == 250
