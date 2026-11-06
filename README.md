# Ejercicio 3: Hilos con Lock (condiciones de carrera) - Cuenta bancaria compartida

Script en Python que muestra una **ejecución con hilos** y una **condición de carrera**, y cómo se soluciona con un **Lock**. El ejemplo de la vida real: dos personas retiran dinero de la misma cuenta bancaria al mismo tiempo desde dos cajeros automáticos.

## Conceptos

- **Hilo (thread):** flujo de ejecución independiente dentro de un programa. Aquí, cada cajero automático es un hilo (`threading.Thread`).
- **Condición de carrera (race condition):** ocurre cuando varios hilos leen y modifican un mismo dato compartido al mismo tiempo y el resultado depende del orden en que se ejecuten.
- **Lock:** un "candado". Solo un hilo a la vez puede entrar a la **sección crítica** (el código que toca el dato compartido). Los demás esperan su turno.

## El ejemplo

Una cuenta tiene **$1000**. Dos cajeros (hilos) hacen **5 retiros de $100 cada uno**. En total se retiran $1000, así que el saldo final correcto es **$0**.

Cada retiro hace tres pasos:

1. **Leer** el saldo.
2. Procesar el retiro (el cajero tarda un instante).
3. **Guardar** `saldo_leido - monto`.

### Parte 1: SIN Lock (incorrecto)

Los dos cajeros leen el mismo saldo ($1000) antes de que el otro guarde su resultado. Ambos guardan $900, y el segundo pisa al primero: **se entregan $200 en efectivo pero el saldo solo baja $100**. Al final el banco entregó $1000 y solo descontó $500.

### Parte 2: CON Lock (correcto)

El retiro completo (leer + procesar + guardar) está protegido con `with self.lock:`. Un cajero termina su retiro antes de que el otro pueda leer el saldo. El saldo final es **$0**, coherente con el dinero entregado.

> Nota: en la Parte 2 se ve que un cajero hace varios retiros seguidos antes de que el otro entre. Es normal: el Lock garantiza **exclusión mutua**, no un orden alternado. Lo importante es que el resultado es siempre correcto.

## Requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y en ejecución (incluye Docker Compose).

## Cómo ejecutarlo con Docker

1. Clonar el repositorio y entrar a la carpeta:

   ```bash
   git clone https://github.com/arielll669/ejercicio3-hilos-lock-cuenta-bancaria.git
   cd ejercicio3-hilos-lock-cuenta-bancaria
   ```

2. Construir la imagen y ejecutar el script:

   ```bash
   docker compose up --build
   ```

3. Al terminar, limpiar el contenedor:

   ```bash
   docker compose down
   ```

## Salida esperada

El orden exacto de las líneas de los dos cajeros puede variar entre ejecuciones (así son los hilos), pero el resultado final de cada parte es siempre el mismo.

```
==================================================================
PARTE 1: SIN LOCK (condicion de carrera)
Dos cajeros retiran de la misma cuenta al mismo tiempo.
==================================================================
[ 0.00s] [Cajero-1] Lee saldo: $1000. Quiere retirar $100
[ 0.00s] [Cajero-2] Lee saldo: $1000. Quiere retirar $100
[ 0.05s] [Cajero-1] Entrega $100. Saldo guardado: $900
[ 0.05s] [Cajero-2] Entrega $100. Saldo guardado: $900
...
------------------------------------------------------------------
Saldo inicial:               $1000
Dinero entregado por cajeros: $1000
Saldo esperado:              $0
Saldo final real:            $500
RESULTADO: INCORRECTO (condicion de carrera). El banco entrego $1000 pero solo desconto $500: $500 regalados.
------------------------------------------------------------------

==================================================================
PARTE 2: CON LOCK (seccion critica protegida)
Mismo escenario, pero solo un cajero a la vez accede al saldo.
==================================================================
[ 0.25s] [Cajero-1] Lee saldo: $1000. Quiere retirar $100
[ 0.30s] [Cajero-1] Entrega $100. Saldo guardado: $900
...
------------------------------------------------------------------
Saldo inicial:               $1000
Dinero entregado por cajeros: $1000
Saldo esperado:              $0
Saldo final real:            $0
RESULTADO: CORRECTO. El saldo coincide con el dinero entregado.
------------------------------------------------------------------
```

## Estructura del proyecto

```
.
├── main.py              # Cuenta bancaria, cajeros (hilos) y comparación sin/con Lock
├── Dockerfile           # Imagen de Python 3.12
├── docker-compose.yml   # Definición del servicio
└── README.md
```

## Ejecución sin Docker (opcional)

```bash
python main.py
```
