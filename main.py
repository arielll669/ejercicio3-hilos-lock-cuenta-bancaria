"""
Ejercicio 3: Hilos y condiciones de carrera (con y sin Lock)
Ejemplo de la vida real: dos personas retiran dinero de la MISMA cuenta
bancaria al mismo tiempo, desde dos cajeros automaticos distintos.

Cada cajero es un hilo (threading.Thread). Ambos comparten la variable `saldo`.

  1) SIN Lock -> condicion de carrera: los dos hilos leen el mismo saldo, cada
                 uno resta por su lado y uno pisa el resultado del otro.
                 El banco entrega mas dinero del que descuenta.
  2) CON Lock -> solo un hilo a la vez puede ejecutar la seccion critica
                 (leer saldo + restar + guardar). El saldo queda correcto.
"""

import sys
import threading
import time

INICIO = time.perf_counter()

SALDO_INICIAL = 1000
MONTO_RETIRO = 100
RETIROS_POR_CAJERO = 5
NUM_CAJEROS = 2
# Dinero que se retira en total: 2 cajeros x 5 retiros x $100 = $1000
TOTAL_ENTREGADO_ESPERADO = NUM_CAJEROS * RETIROS_POR_CAJERO * MONTO_RETIRO


def log(mensaje: str) -> None:
    """Imprime un mensaje con el segundo exacto y el nombre del hilo."""
    transcurrido = time.perf_counter() - INICIO
    hilo = threading.current_thread().name
    # Una sola escritura (con el salto de linea incluido) para que las lineas
    # de distintos hilos no se mezclen en pantalla.
    sys.stdout.write(f"[{transcurrido:5.2f}s] [{hilo}] {mensaje}\n")


class CuentaBancaria:
    def __init__(self, saldo: int) -> None:
        self.saldo = saldo
        self.dinero_entregado = 0  # efectivo que realmente salio de los cajeros
        self.lock = threading.Lock()

    # ------------------------------------------------------------------
    # VERSION INSEGURA: sin Lock
    # ------------------------------------------------------------------
    def retirar_sin_lock(self, monto: int) -> None:
        saldo_leido = self.saldo                      # 1. lee el saldo
        log(f"Lee saldo: ${saldo_leido}. Quiere retirar ${monto}")
        if saldo_leido >= monto:
            time.sleep(0.05)                          # 2. el cajero procesa (aqui
            #                                              el otro hilo se cuela)
            self.saldo = saldo_leido - monto          # 3. guarda el nuevo saldo
            self.dinero_entregado += monto
            log(f"Entrega ${monto}. Saldo guardado: ${self.saldo}")
        else:
            log("Fondos insuficientes.")

    # ------------------------------------------------------------------
    # VERSION SEGURA: con Lock
    # ------------------------------------------------------------------
    def retirar_con_lock(self, monto: int) -> None:
        with self.lock:                               # solo UN hilo entra a la vez
            saldo_leido = self.saldo
            log(f"Lee saldo: ${saldo_leido}. Quiere retirar ${monto}")
            if saldo_leido >= monto:
                time.sleep(0.05)
                self.saldo = saldo_leido - monto
                self.dinero_entregado += monto
                log(f"Entrega ${monto}. Saldo guardado: ${self.saldo}")
            else:
                log("Fondos insuficientes.")


def cajero(cuenta: CuentaBancaria, usar_lock: bool) -> None:
    """Un cajero automatico que hace varios retiros seguidos."""
    for _ in range(RETIROS_POR_CAJERO):
        if usar_lock:
            cuenta.retirar_con_lock(MONTO_RETIRO)
        else:
            cuenta.retirar_sin_lock(MONTO_RETIRO)


def simular(usar_lock: bool) -> CuentaBancaria:
    cuenta = CuentaBancaria(SALDO_INICIAL)
    hilos = [
        threading.Thread(target=cajero, args=(cuenta, usar_lock), name=f"Cajero-{i + 1}")
        for i in range(NUM_CAJEROS)
    ]

    for h in hilos:
        h.start()   # los dos cajeros empiezan a la vez
    for h in hilos:
        h.join()    # esperamos a que ambos terminen

    return cuenta


def mostrar_resultado(cuenta: CuentaBancaria) -> None:
    saldo_esperado = SALDO_INICIAL - TOTAL_ENTREGADO_ESPERADO
    print("-" * 66)
    print(f"Saldo inicial:               ${SALDO_INICIAL}")
    print(f"Dinero entregado por cajeros: ${cuenta.dinero_entregado}")
    print(f"Saldo esperado:              ${saldo_esperado}")
    print(f"Saldo final real:            ${cuenta.saldo}")
    if cuenta.saldo == saldo_esperado:
        print("RESULTADO: CORRECTO. El saldo coincide con el dinero entregado.")
    else:
        descontado = SALDO_INICIAL - cuenta.saldo
        regalado = cuenta.dinero_entregado - descontado
        print(f"RESULTADO: INCORRECTO (condicion de carrera). El banco entrego "
              f"${cuenta.dinero_entregado} pero solo desconto ${descontado}: "
              f"${regalado} regalados.")
    print("-" * 66)


def main() -> None:
    print("=" * 66)
    print("PARTE 1: SIN LOCK (condicion de carrera)")
    print("Dos cajeros retiran de la misma cuenta al mismo tiempo.")
    print("=" * 66)
    cuenta_sin_lock = simular(usar_lock=False)
    mostrar_resultado(cuenta_sin_lock)

    print()
    print("=" * 66)
    print("PARTE 2: CON LOCK (seccion critica protegida)")
    print("Mismo escenario, pero solo un cajero a la vez accede al saldo.")
    print("=" * 66)
    cuenta_con_lock = simular(usar_lock=True)
    mostrar_resultado(cuenta_con_lock)


if __name__ == "__main__":
    main()
