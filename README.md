# Sistema de cuentas bancarias en Python

Trabajo sobre el sistema de cuentas bancarias para evidenciar programacion orientada a objetos, principios SOLID, herencia, reutilizacion de codigo, polimorfismo, modularidad, manejo de archivos y pruebas unitarias.

## Tema

Sistema de cuentas bancarias con dos tipos de cuentas:

- `CuentaAhorros`: no permite sobregiro y gana interes mensual.
- `CuentaCorriente`: permite sobregiro hasta un cupo y cobra comision mensual.

Los objetos se guardan en el archivo de texto `datos/cuentas.txt` usando una linea JSON por cuenta.

## Estructura del proyecto

``` text
sistema_cuentas_bancarias/
|-- cuentas/
|   |-- __init__.py
|   |-- banco.py
|   |-- excepciones.py
|   |-- modelos.py
|   `-- persistencia.py
|-- datos/
|   `-- cuentas.txt
|-- tests/
|   `-- test_cuentas.py
|-- main.py
`-- README.md
```

## Diagrama UML

``` mermaid

classDiagram
    class CuentaBancaria {
        <<abstract>>
        +str numero
        +str titular
        +float saldo
        +tipo* str
        +saldo_minimo_permitido() float
        +depositar(monto)
        +retirar(monto)
        +aplicar_corte_mensual()* str
        +to_dict() dict
    }

    class CuentaAhorros {
        +float tasa_interes
        +aplicar_corte_mensual() str
    }

    class CuentaCorriente {
        +float cupo_sobregiro
        +float comision_mensual
        +saldo_minimo_permitido() float
        +aplicar_corte_mensual() str
    }

    class Banco {
        +str nombre
        -_cuentas dict
        +agregar_cuenta(cuenta)
        +obtener_cuenta(numero)
        +listar_cuentas() list
        +depositar(numero, monto)
        +retirar(numero, monto)
        +transferir(origen, destino, monto)
        +aplicar_corte_mensual() list
    }

    class RepositorioCuentasTxt {
        +Path ruta_archivo
        +guardar(cuentas)
        +cargar() list
    }

    CuentaBancaria <|-- CuentaAhorros : Herencia
    CuentaBancaria <|-- CuentaCorriente : Herencia
    Banco "1" o-- "*" CuentaBancaria : Agregación
    RepositorioCuentasTxt ..> CuentaBancaria : Persistencia
```

## Conceptos aplicados

| Concepto | Aplicacion en el proyecto |
|------------------------------------|------------------------------------|
| Herencia | `CuentaAhorros` y `CuentaCorriente` heredan de `CuentaBancaria`. |
| Reutilizacion | `depositar`, `retirar`, validaciones y `to_dict` se implementan una vez en la clase base. |
| Polimorfismo | `aplicar_corte_mensual()` se llama igual para todas las cuentas, pero cada subclase responde diferente. |
| Modularidad | El codigo se divide en modulos: modelos, banco, persistencia, excepciones y pruebas. |
| Manejo de archivos | `RepositorioCuentasTxt` guarda y carga objetos desde `datos/cuentas.txt`. |
| Pruebas unitarias | `tests/test_cuentas.py` valida reglas de negocio, polimorfismo y persistencia. |
| SOLID | Responsabilidad unica, abierto/cerrado, sustitucion de Liskov e inversion hacia abstracciones de dominio. |

## Archivo de texto generado

Despues de ejecutar el programa, se crea o actualiza:

``` text
datos/cuentas.txt
```

Ejemplo de una linea guardada:

``` json
{"tipo": "AHORROS", "numero": "AH-001", "titular": "Daniel Moreno", "saldo": 525000.0, "tasa_interes": 0.015}
```

\`\`\`
