# Mercado Sabanero - Módulo de Liquidación de Compras

Sistema de liquidación de pedidos y gestión de carrito de compras para la tienda en línea **Mercado Sabanero** (Sincelejo, Sucre). Proyecto desarrollado para la asignatura de Agilidad Continua (CECAR) utilizando Desarrollo Guiado por Pruebas (TDD).

## Estructura del Proyecto

```text
mercado-sabanero/
├── src/
│   ├── __init__.py
│   ├── inventario.py     # Servicio externo de inventario (Mockeado en pruebas)
│   ├── carrito.py        # HU-01: Lógica de carrito de compras
│   └── liquidacion.py    # HU-02 a HU-06: Lógica de IVA, descuentos, cupones, envío y puntos
├── tests/
│   ├── __init__.py
│   ├── test_carrito.py    # Pruebas unitarias de carrito
│   └── test_liquidacion.py# Pruebas unitarias de liquidación
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Instrucciones de ejecución
```

## Requisitos Previos

- Python 3.10 o superior
- Git

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone <URL_DEL_REPOSITO>
   cd mercado-sabanero
   ```

2. Crear y activar un entorno virtual (recomendado):
   ```bash
   # En Windows:
   python -m venv venv
   .\venv\Scripts\activate

   # En Linux/macOS:
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instalar las dependencias del proyecto:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución de Pruebas Unitarias

Para ejecutar todas las pruebas unitarias automatizadas con `pytest`:

```bash
pytest
```

Para ver la salida detallada de cada prueba:

```bash
pytest -v
```

## Reporte de Cobertura de Código

Para ejecutar las pruebas y generar el reporte de cobertura en consola (verificando el requisito de mínimo 80%):

```bash
pytest --cov=src --cov-report=term-missing
```

Para generar un reporte interactivo en HTML:

```bash
pytest --cov=src --cov-report=html
```
El reporte se generará en la carpeta `htmlcov/index.html`.
