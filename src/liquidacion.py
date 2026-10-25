"""
Módulo: src/liquidacion.py
Descripción: Implementación de la clase LiquidadorCompra para responder a HU-02 a HU-06.
"""


class LiquidadorCompra:
    def obtener_porcentaje_descuento_volumen(self, subtotal: int) -> float:
        """
        HU-03: Determina el porcentaje de descuento por volumen según el subtotal:
        - Subtotal < $200.000 -> 0%
        - $200.000 <= Subtotal < $500.000 -> 5%
        - Subtotal >= $500.000 -> 10%
        """
        if subtotal >= 500000:
            return 0.10
        elif subtotal >= 200000:
            return 0.05
        return 0.00

    def validar_y_obtener_descuento_cupon(self, cupon: str, subtotal: int) -> float:
        """
        HU-04: Valida cupones de descuento.
        Lanza ValueError si el cupón no existe o no cumple condiciones.
        """
        if not cupon:
            return 0.0

        cupon_clean = cupon.strip().upper()

        if cupon_clean == "SABANERO10":
            if subtotal < 50000:
                raise ValueError("El cupón SABANERO10 requiere un subtotal mínimo de $50.000.")
            return 0.10
        elif cupon_clean == "ENVIOGRATIS":
            return 0.0  # El descuento de envío se gestiona en la tarifa de envío
        else:
            raise ValueError("Cupón inválido o vencido.")

    def calcular_envio(self, municipio: str, suma_productos_con_iva: int, cupon: str = None) -> int:
        """
        HU-05: Calcula el costo de envío:
        - Gratis si se usa cupón ENVIOGRATIS.
        - Gratis si los productos con IVA (tarifa > 0%) suman $150.000 o más.
        - Sincelejo: $8.000.
        - Otros municipios de Sucre: $15.000.
        """
        if cupon and cupon.strip().upper() == "ENVIOGRATIS":
            return 0

        if suma_productos_con_iva >= 150000:
            return 0

        municipio_clean = municipio.strip().title()
        if municipio_clean == "Sincelejo":
            return 8000
        else:
            return 15000

    def calcular_puntos(self, total_sin_envio: int, tipo_cliente: str = "ESTANDAR") -> int:
        """
        HU-06: Acumulación de puntos:
        - 1 punto por cada $1.000 completos pagados (sin envío).
        - Clientes ORO reciben el doble.
        """
        puntos_base = total_sin_envio // 1000
        if tipo_cliente.strip().upper() == "ORO":
            return puntos_base * 2
        return puntos_base

    def liquidar(self, items: list, municipio: str, cupon: str = None, tipo_cliente: str = "ESTANDAR") -> dict:
        """
        Liquida la compra aplicando la secuencia completa de reglas de negocio:
        1. Subtotal
        2. Regla de no acumulación de descuentos (Volumen vs Cupón)
        3. Recálculo de IVA sobre valor con descuento aplicado por producto
        4. Envío regional / envío gratis
        5. Total final y Puntos acumulados
        """
        if not items:
            raise ValueError("El carrito no contiene productos para liquidar.")

        # 1. Subtotal bruto y suma de productos con IVA
        subtotal = 0
        suma_productos_con_iva = 0

        for item in items:
            subtotal_item = item["precio_unitario"] * item["cantidad"]
            subtotal += subtotal_item
            if item.get("tarifa_iva", 0.0) > 0.0:
                suma_productos_con_iva += subtotal_item

        subtotal = round(subtotal)

        # 2. Descuento: Regla de no acumulación (HU-04 CA4) -> Elegir el mayor entre Volumen y Cupón
        porc_volumen = self.obtener_porcentaje_descuento_volumen(subtotal)
        porc_cupon = self.validar_y_obtener_descuento_cupon(cupon, subtotal)

        if porc_cupon > porc_volumen:
            porcentaje_descuento_final = porc_cupon
            tipo_descuento_aplicado = "CUPON"
        else:
            porcentaje_descuento_final = porc_volumen
            tipo_descuento_aplicado = "VOLUMEN" if porc_volumen > 0 else "NINGUNO"

        monto_descuento_total = round(subtotal * porcentaje_descuento_final)

        # 3. HU-02 CA2: Calcular IVA ítem por ítem aplicando el descuento proporcional
        factor_descuento = 1.0 - porcentaje_descuento_final
        iva_total = 0.0

        for item in items:
            base_item = (item["precio_unitario"] * item["cantidad"]) * factor_descuento
            iva_item = base_item * item.get("tarifa_iva", 0.0)
            iva_total += iva_item

        iva_total = round(iva_total)

        # 4. HU-05: Calcular Envío
        costo_envio = self.calcular_envio(municipio, suma_productos_con_iva, cupon)

        # 5. HU-05 CA3: Total a Pagar = Subtotal - Descuento + IVA + Envío
        total_pagar = subtotal - monto_descuento_total + iva_total + costo_envio

        # 6. HU-06: Puntos sobre valor total sin envío
        total_sin_envio = subtotal - monto_descuento_total + iva_total
        puntos = self.calcular_puntos(total_sin_envio, tipo_cliente)

        return {
            "subtotal": subtotal,
            "descuento_monto": monto_descuento_total,
            "descuento_aplicado_tipo": tipo_descuento_aplicado,
            "iva_total": iva_total,
            "envio": costo_envio,
            "total_pagar": total_pagar,
            "puntos": puntos
        }
