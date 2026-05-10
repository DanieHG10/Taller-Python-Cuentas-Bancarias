from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Type

from .excepciones import FondosInsuficientesError, ValorInvalidoError


@dataclass
class CuentaBancaria(ABC):
    """Clase abstracta que define el comportamiento comun de una cuenta.
    """

    numero: str
    titular: str
    saldo: float = 0.0

    def __post_init__(self) -> None:
        self.numero = self.numero.strip()
        self.titular = self.titular.strip()
        self.saldo = float(self.saldo)
        if not self.numero:
            raise ValorInvalidoError("El numero de cuenta es obligatorio.")
        if not self.titular:
            raise ValorInvalidoError("El titular de la cuenta es obligatorio.")
        if self.saldo < self.saldo_minimo_permitido():
            raise ValorInvalidoError(
                f"El saldo inicial no puede ser menor a {self.saldo_minimo_permitido():.2f}."
            )

    @property
    @abstractmethod
    def tipo(self) -> str:
        """Tipo de cuenta usado para persistencia y reportes."""

    def saldo_minimo_permitido(self) -> float:
        """Regla reutilizable. Por defecto una cuenta no acepta saldo negativo."""
        return 0.0

    def depositar(self, monto: float) -> None:
        """Aumenta el saldo si el monto es valido."""
        monto = self._validar_monto(monto)
        self.saldo += monto

    def retirar(self, monto: float) -> None:
        """Disminuye el saldo respetando el saldo minimo permitido."""
        monto = self._validar_monto(monto)
        saldo_resultante = self.saldo - monto
        if saldo_resultante < self.saldo_minimo_permitido():
            raise FondosInsuficientesError(
                f"La cuenta {self.numero} no tiene fondos suficientes."
            )
        self.saldo = saldo_resultante

    @abstractmethod
    def aplicar_corte_mensual(self) -> str:
        """Operacion polimorfica: cada cuenta aplica reglas diferentes."""

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el objeto a diccionario para guardarlo en archivo de texto."""
        return {
            "tipo": self.tipo,
            "numero": self.numero,
            "titular": self.titular,
            "saldo": round(self.saldo, 2),
        }

    @staticmethod
    def _validar_monto(monto: float) -> float:
        try:
            monto = float(monto)
        except (TypeError, ValueError) as exc:
            raise ValorInvalidoError("El monto debe ser numerico.") from exc
        if monto <= 0:
            raise ValorInvalidoError("El monto debe ser mayor que cero.")
        return monto


@dataclass
class CuentaAhorros(CuentaBancaria):
    """Cuenta de ahorros: gana intereses y no permite sobregiro."""

    tasa_interes: float = 0.01

    @property
    def tipo(self) -> str:
        return "AHORROS"

    def __post_init__(self) -> None:
        self.tasa_interes = float(self.tasa_interes)
        if self.tasa_interes < 0:
            raise ValorInvalidoError("La tasa de interes no puede ser negativa.")
        super().__post_init__()

    def aplicar_corte_mensual(self) -> str:
        interes = self.saldo * self.tasa_interes
        self.saldo += interes
        return (
            f"Cuenta {self.numero} AHORROS: se adiciono interes de "
            f"{interes:.2f}. Saldo final: {self.saldo:.2f}."
        )

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["tasa_interes"] = self.tasa_interes
        return data


@dataclass
class CuentaCorriente(CuentaBancaria):
    """Cuenta corriente: permite sobregiro y cobra comision mensual."""

    cupo_sobregiro: float = 100_000.0
    comision_mensual: float = 3_000.0

    @property
    def tipo(self) -> str:
        return "CORRIENTE"

    def __post_init__(self) -> None:
        self.cupo_sobregiro = float(self.cupo_sobregiro)
        self.comision_mensual = float(self.comision_mensual)
        if self.cupo_sobregiro < 0:
            raise ValorInvalidoError("El cupo de sobregiro no puede ser negativo.")
        if self.comision_mensual < 0:
            raise ValorInvalidoError("La comision mensual no puede ser negativa.")
        super().__post_init__()

    def saldo_minimo_permitido(self) -> float:
        return -self.cupo_sobregiro

    def aplicar_corte_mensual(self) -> str:
        # Reutiliza retirar para aplicar las mismas reglas de saldo minimo.
        self.retirar(self.comision_mensual)
        return (
            f"Cuenta {self.numero} CORRIENTE: se desconto comision de "
            f"{self.comision_mensual:.2f}. Saldo final: {self.saldo:.2f}."
        )

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["cupo_sobregiro"] = self.cupo_sobregiro
        data["comision_mensual"] = self.comision_mensual
        return data


TIPOS_CUENTA: Dict[str, Type[CuentaBancaria]] = {
    "AHORROS": CuentaAhorros,
    "CORRIENTE": CuentaCorriente,
}


def crear_cuenta_desde_dict(data: Dict[str, Any]) -> CuentaBancaria:
    """Reconstruye una cuenta desde un diccionario leido del archivo."""
    tipo = str(data.get("tipo", "")).upper()
    if tipo not in TIPOS_CUENTA:
        raise ValorInvalidoError(f"Tipo de cuenta no soportado: {tipo}")

    clase = TIPOS_CUENTA[tipo]
    valores = dict(data)
    valores.pop("tipo", None)
    return clase(**valores)
