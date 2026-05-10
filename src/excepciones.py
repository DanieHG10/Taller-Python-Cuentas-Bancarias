"""Excepciones propias del sistema bancario."""


class CuentaError(Exception):
    """Error base del sistema de cuentas."""


class ValorInvalidoError(CuentaError):
    """Se lanza cuando un dato o monto no cumple las reglas de negocio."""


class FondosInsuficientesError(CuentaError):
    """Se lanza cuando una cuenta no puede cubrir un retiro."""


class CuentaNoEncontradaError(CuentaError):
    """Se lanza cuando se busca una cuenta que no existe."""


class CuentaDuplicadaError(CuentaError):
    """Se lanza cuando se intenta registrar una cuenta ya existente."""
