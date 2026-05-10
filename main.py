"""Programa principal del sistema de cuentas bancarias."""

from pathlib import Path

from src import Banco, CuentaAhorros, CuentaCorriente, RepositorioCuentasTxt


def construir_banco_demo() -> Banco:
    banco = Banco("Banco POO Python")
    banco.agregar_cuenta(
        CuentaAhorros(numero="AH-001", titular="Daniel Moreno", saldo=500_000, tasa_interes=0.015)
    )
    banco.agregar_cuenta(
        CuentaCorriente(
            numero="CC-001",
            titular="Laura Garcia",
            saldo=200_000,
            cupo_sobregiro=150_000,
            comision_mensual=5_000,
        )
    )
    return banco


def mostrar_cuentas(banco: Banco) -> None:
    print(f"\nCuentas registradas en {banco.nombre}")
    print("-" * 62)
    for cuenta in banco.listar_cuentas():
        print(
            f"{cuenta.tipo:10} | {cuenta.numero:6} | "
            f"{cuenta.titular:20} | saldo: {cuenta.saldo:,.2f}"
        )


def main() -> None:
    ruta = Path(__file__).parent / "datos" / "cuentas.txt"
    repositorio = RepositorioCuentasTxt(ruta)

    cuentas_guardadas = repositorio.cargar()
    if cuentas_guardadas:
        banco = Banco("Banco POO Python")
        for cuenta in cuentas_guardadas:
            banco.agregar_cuenta(cuenta)
        print("Se cargaron las cuentas desde el archivo de texto.")
    else:
        banco = construir_banco_demo()
        print("No habia archivo previo. Se crearon cuentas de ejemplo.")

    mostrar_cuentas(banco)

    print("\nOperaciones realizadas")
    print("-" * 62)
    banco.depositar("AH-001", 100_000)
    print("Deposito de 100000 en AH-001")

    banco.retirar("CC-001", 50_000)
    print("Retiro de 50000 en CC-001")

    banco.transferir("AH-001", "CC-001", 75_000)
    print("Transferencia de 75000 desde AH-001 hacia CC-001")

    print("\nCorte mensual polimorfico")
    print("-" * 62)
    for reporte in banco.aplicar_corte_mensual():
        print(reporte)

    mostrar_cuentas(banco)
    repositorio.guardar(banco.listar_cuentas())
    print(f"\nObjetos guardados en archivo de texto: {ruta}")


if __name__ == "__main__":
    main()
