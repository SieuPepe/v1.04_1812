"""
Módulo de formato de números para garantizar precisión de 2 decimales.

Este módulo proporciona funciones para formatear números con exactamente
2 decimales en todo el software, asegurando consistencia en la presentación
de importes monetarios, cantidades, precios unitarios, certificaciones, etc.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Union, Optional


def format_decimal(value: Union[int, float, Decimal, str, None], decimals: int = 2) -> str:
    """
    Formatea un número con el número especificado de decimales.

    Args:
        value: Valor numérico a formatear (int, float, Decimal, str o None)
        decimals: Número de decimales (por defecto 2)

    Returns:
        str: Valor formateado con los decimales especificados

    Ejemplos:
        >>> format_decimal(1234.5678)
        '1234.57'
        >>> format_decimal(1234.5)
        '1234.50'
        >>> format_decimal(None)
        '0.00'
        >>> format_decimal('1234.567')
        '1234.57'
    """
    if value is None or value == '':
        return f"0.{'{:0{width}d}'.format(0, width=decimals)}"

    try:
        # Convertir a Decimal para mayor precisión
        if isinstance(value, str):
            decimal_value = Decimal(value.replace(',', '.'))
        else:
            decimal_value = Decimal(str(value))

        # Redondear al número de decimales especificado
        quantize_string = '0.' + '0' * decimals
        rounded_value = decimal_value.quantize(Decimal(quantize_string), rounding=ROUND_HALF_UP)

        # Formatear con el número de decimales especificado
        return f"{rounded_value:.{decimals}f}"

    except (ValueError, TypeError, ArithmeticError):
        # En caso de error, devolver 0 con los decimales especificados
        return f"0.{'{:0{width}d}'.format(0, width=decimals)}"


def format_currency(value: Union[int, float, Decimal, str, None], decimals: int = 2, currency: str = '€') -> str:
    """
    Formatea un número como moneda con el número especificado de decimales.

    Args:
        value: Valor numérico a formatear
        decimals: Número de decimales (por defecto 2)
        currency: Símbolo de moneda (por defecto '€')

    Returns:
        str: Valor formateado como moneda

    Ejemplos:
        >>> format_currency(1234.5678)
        '1234.57 €'
        >>> format_currency(1234.5, currency='$')
        '1234.50 $'
    """
    formatted_value = format_decimal(value, decimals)
    return f"{formatted_value} {currency}"


def format_percentage(value: Union[int, float, Decimal, str, None], decimals: int = 2) -> str:
    """
    Formatea un número como porcentaje con el número especificado de decimales.

    Args:
        value: Valor numérico a formatear (ya en formato porcentaje, no fracción)
        decimals: Número de decimales (por defecto 2)

    Returns:
        str: Valor formateado como porcentaje

    Ejemplos:
        >>> format_percentage(15.5)
        '15.50%'
        >>> format_percentage(0.5)
        '0.50%'
    """
    formatted_value = format_decimal(value, decimals)
    return f"{formatted_value}%"


def to_decimal(value: Union[int, float, Decimal, str, None], decimals: int = 2) -> Decimal:
    """
    Convierte un valor a Decimal con el número especificado de decimales.

    Args:
        value: Valor a convertir
        decimals: Número de decimales (por defecto 2)

    Returns:
        Decimal: Valor como Decimal redondeado

    Ejemplos:
        >>> to_decimal(1234.567)
        Decimal('1234.57')
        >>> to_decimal('1234.5')
        Decimal('1234.50')
    """
    if value is None or value == '':
        return Decimal('0.00')

    try:
        if isinstance(value, str):
            decimal_value = Decimal(value.replace(',', '.'))
        else:
            decimal_value = Decimal(str(value))

        quantize_string = '0.' + '0' * decimals
        return decimal_value.quantize(Decimal(quantize_string), rounding=ROUND_HALF_UP)

    except (ValueError, TypeError, ArithmeticError):
        return Decimal('0.00')


def safe_float(value: Union[int, float, Decimal, str, None], default: float = 0.0) -> float:
    """
    Convierte de forma segura un valor a float, devolviendo un valor por defecto si falla.

    Args:
        value: Valor a convertir
        default: Valor por defecto si la conversión falla (por defecto 0.0)

    Returns:
        float: Valor como float o valor por defecto

    Ejemplos:
        >>> safe_float('1234.56')
        1234.56
        >>> safe_float(None)
        0.0
        >>> safe_float('invalid', 99.0)
        99.0
    """
    if value is None or value == '':
        return default

    try:
        if isinstance(value, str):
            return float(value.replace(',', '.'))
        return float(value)
    except (ValueError, TypeError):
        return default


def round_to_decimals(value: Union[int, float, Decimal, str, None], decimals: int = 2) -> float:
    """
    Redondea un valor al número especificado de decimales.

    Args:
        value: Valor a redondear
        decimals: Número de decimales (por defecto 2)

    Returns:
        float: Valor redondeado

    Ejemplos:
        >>> round_to_decimals(1234.567)
        1234.57
        >>> round_to_decimals('1234.5')
        1234.50
    """
    return float(to_decimal(value, decimals))


# Alias para facilitar la migración de código existente
fmt = format_decimal
fmt_curr = format_currency
fmt_pct = format_percentage


if __name__ == "__main__":
    # Pruebas
    print("Pruebas del módulo number_formatter:")
    print("-" * 60)

    test_values = [1234.567, 1234.5, None, '1234.567', 0, 0.1, 0.01]

    for value in test_values:
        print(f"\nValor: {value}")
        print(f"  format_decimal:      {format_decimal(value)}")
        print(f"  format_currency:     {format_currency(value)}")
        print(f"  format_percentage:   {format_percentage(value)}")
        print(f"  to_decimal:          {to_decimal(value)}")
        print(f"  round_to_decimals:   {round_to_decimals(value)}")
