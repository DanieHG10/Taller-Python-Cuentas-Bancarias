"""Persistencia de objetos en archivo de texto usando JSON Lines."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

from .modelos import CuentaBancaria, crear_cuenta_desde_dict


class RepositorioCuentasTxt:
    """Guarda y carga cuentas en un archivo .txt.

    Cada linea del archivo es un objeto en formato JSON. Sigue siendo un archivo
    de texto y se puede abrir con cualquier editor.
    """

    def __init__(self, ruta_archivo: str | Path) -> None:
        self.ruta_archivo = Path(ruta_archivo)

    def guardar(self, cuentas: Iterable[CuentaBancaria]) -> None:
        self.ruta_archivo.parent.mkdir(parents=True, exist_ok=True)
        with self.ruta_archivo.open("w", encoding="utf-8") as archivo:
            for cuenta in cuentas:
                linea = json.dumps(cuenta.to_dict(), ensure_ascii=False)
                archivo.write(linea + "\n")

    def cargar(self) -> List[CuentaBancaria]:
        if not self.ruta_archivo.exists():
            return []

        cuentas: List[CuentaBancaria] = []
        with self.ruta_archivo.open("r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue
                data = json.loads(linea)
                cuentas.append(crear_cuenta_desde_dict(data))
        return cuentas
