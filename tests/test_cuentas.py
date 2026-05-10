import tempfile
import unittest
from pathlib import Path

from src import Banco, CuentaAhorros, CuentaCorriente, RepositorioCuentasTxt
from src.excepciones import CuentaDuplicadaError, FondosInsuficientesError, ValorInvalidoError


class TestSistemaCuentasBancarias(unittest.TestCase):
    def test_depositar_y_retirar_en_cuenta_ahorros(self):
        cuenta = CuentaAhorros(numero="AH-100", titular="Ana", saldo=1000)
        cuenta.depositar(500)
        cuenta.retirar(300)
        self.assertEqual(cuenta.saldo, 1200)

    def test_cuenta_ahorros_no_permite_sobregiro(self):
        cuenta = CuentaAhorros(numero="AH-101", titular="Luis", saldo=1000)
        with self.assertRaises(FondosInsuficientesError):
            cuenta.retirar(1500)

    def test_cuenta_corriente_permite_sobregiro_controlado(self):
        cuenta = CuentaCorriente(
            numero="CC-200",
            titular="Maria",
            saldo=1000,
            cupo_sobregiro=500,
            comision_mensual=100,
        )
        cuenta.retirar(1200)
        self.assertEqual(cuenta.saldo, -200)

        with self.assertRaises(FondosInsuficientesError):
            cuenta.retirar(400)

    def test_polimorfismo_en_corte_mensual(self):
        cuentas = [
            CuentaAhorros(numero="AH-300", titular="Pedro", saldo=1000, tasa_interes=0.10),
            CuentaCorriente(
                numero="CC-300",
                titular="Sofia",
                saldo=1000,
                cupo_sobregiro=500,
                comision_mensual=100,
            ),
        ]

        reportes = [cuenta.aplicar_corte_mensual() for cuenta in cuentas]

        self.assertAlmostEqual(cuentas[0].saldo, 1100)
        self.assertAlmostEqual(cuentas[1].saldo, 900)
        self.assertIn("AHORROS", reportes[0])
        self.assertIn("CORRIENTE", reportes[1])

    def test_banco_transfiere_entre_cuentas(self):
        banco = Banco("Banco Test")
        banco.agregar_cuenta(CuentaAhorros(numero="AH-400", titular="Camila", saldo=5000))
        banco.agregar_cuenta(
            CuentaCorriente(numero="CC-400", titular="David", saldo=1000, cupo_sobregiro=1000)
        )

        banco.transferir("AH-400", "CC-400", 1500)

        self.assertEqual(banco.obtener_cuenta("AH-400").saldo, 3500)
        self.assertEqual(banco.obtener_cuenta("CC-400").saldo, 2500)

    def test_banco_no_acepta_cuentas_duplicadas(self):
        banco = Banco("Banco Test")
        banco.agregar_cuenta(CuentaAhorros(numero="AH-500", titular="Elena", saldo=1000))
        with self.assertRaises(CuentaDuplicadaError):
            banco.agregar_cuenta(CuentaAhorros(numero="AH-500", titular="Otro", saldo=2000))

    def test_persistencia_guarda_y_carga_archivo_txt(self):
        cuentas = [
            CuentaAhorros(numero="AH-600", titular="Nora", saldo=8000, tasa_interes=0.02),
            CuentaCorriente(
                numero="CC-600",
                titular="Oscar",
                saldo=3000,
                cupo_sobregiro=2000,
                comision_mensual=200,
            ),
        ]

        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "cuentas.txt"
            repositorio = RepositorioCuentasTxt(ruta)
            repositorio.guardar(cuentas)
            cuentas_cargadas = repositorio.cargar()

        self.assertEqual(len(cuentas_cargadas), 2)
        self.assertIsInstance(cuentas_cargadas[0], CuentaAhorros)
        self.assertIsInstance(cuentas_cargadas[1], CuentaCorriente)
        self.assertEqual(cuentas_cargadas[0].numero, "AH-600")
        self.assertEqual(cuentas_cargadas[1].numero, "CC-600")

    def test_valida_montos_invalidos(self):
        cuenta = CuentaAhorros(numero="AH-700", titular="Valentina", saldo=1000)
        with self.assertRaises(ValorInvalidoError):
            cuenta.depositar(0)
        with self.assertRaises(ValorInvalidoError):
            cuenta.retirar(-100)


if __name__ == "__main__":
    unittest.main(verbosity=2)
