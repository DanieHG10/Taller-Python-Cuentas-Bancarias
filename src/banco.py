"""Servicio de aplicacion para administrar cuentas bancarias."""

from __future__ import annotations

from typing import Dict, List

from .excepciones import CuentaDuplicadaError, CuentaNoEncontradaError
from .modelos import CuentaBancaria


class Banco:
    """Coordina operaciones entre cuentas.

    Esta clase aplica el principio de responsabilidad unica: administra cuentas y
    operaciones bancarias, pero no se encarga de guardar archivos.
    """

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self._cuentas: Dict[str, CuentaBancaria] = {}

    def agregar_cuenta(self, cuenta: CuentaBancaria) -> None:
        if cuenta.numero in self._cuentas:
            raise CuentaDuplicadaError(f"La cuenta {cuenta.numero} ya existe.")
        self._cuentas[cuenta.numero] = cuenta

    def obtener_cuenta(self, numero: str) -> CuentaBancaria:
        try:
            return self._cuentas[numero]
        except KeyError as exc:
            raise CuentaNoEncontradaError(f"La cuenta {numero} no existe.") from exc

    def listar_cuentas(self) -> List[CuentaBancaria]:
        return list(self._cuentas.values())

    def depositar(self, numero: str, monto: float) -> None:
        self.obtener_cuenta(numero).depositar(monto)

    def retirar(self, numero: str, monto: float) -> None:
        self.obtener_cuenta(numero).retirar(monto)

    def transferir(self, origen: str, destino: str, monto: float) -> None:
        cuenta_origen = self.obtener_cuenta(origen)
        cuenta_destino = self.obtener_cuenta(destino)
        cuenta_origen.retirar(monto)
        cuenta_destino.depositar(monto)

    def aplicar_corte_mensual(self) -> List[str]:
        """Demuestra polimorfismo.

        Todas las cuentas son tratadas como CuentaBancaria, pero cada objeto
        ejecuta su propia version de aplicar_corte_mensual().
        """
        reportes: List[str] = []
        for cuenta in self._cuentas.values():
            reportes.append(cuenta.aplicar_corte_mensual())
        return reportes
