# Explicación del Lenguaje L (ECO-GRID)

El **Lenguaje L** es un Lenguaje de Dominio Específico (DSL) diseñado específicamente para el control, la gestión y la automatización de **ECO-GRID**, una microred eléctrica.

Su objetivo es permitir a los ingenieros de red o técnicos escribir reglas de control de hardware de manera sencilla, declarativa y segura, abstrayendo la complejidad de comunicarse con el hardware de bajo nivel (sensores, baterías, relés).

## Componentes Principales

El lenguaje tiene una sintaxis muy estructurada, parecida a un pseudocódigo en español.

### Palabras Clave (Keywords)
* **`init_grid`**: Registra los componentes (sensores, interruptores) que se van a usar en el programa.
* **`leer_temperatura`**: Lee la temperatura de un componente.
* **`estado_carga`**: Lee el estado de carga (batería, SoC) de un componente.
* **`conmutar_linea`**: Cambia el estado de una línea de carga a `ON` o `OFF`.
* **`si` / `entonces` / `fin_si`**: Permite tomar decisiones (condicionales).
* **`mientras` / `ejecutar` / `fin_mientras`**: Permite crear bucles infinitos para monitoreo en tiempo real.

## Ejemplos Prácticos

### Prevención de Fugas Térmicas
Si una batería se calienta demasiado, hay riesgo de incendio o avería grave. El siguiente código asegura que si la temperatura sube de 55°C, el sistema desconecte la línea de carga automáticamente:

```
init_grid(bateria_b1, linea_carga)

mientras 1 == 1 ejecutar
    temp_actual = leer_temperatura(bateria_b1)
    
    si temp_actual > 55 entonces
        conmutar_linea(linea_carga, OFF)
    fin_si
fin_mientras
```

### Balance de Cargas (Deslastre)
Si la batería principal se está agotando (baja del 20%), apagamos cargas secundarias para ahorrar energía. Solo las volvemos a encender cuando la batería se recupera firmemente (más del 40%):

```
init_grid(bat_principal, cargas_secundarias)

mientras 1 == 1 ejecutar
    carga_sistema = estado_carga(bat_principal)
    
    si carga_sistema < 20 entonces
        conmutar_linea(cargas_secundarias, OFF)
    fin_si
    
    si carga_sistema > 40 entonces
        conmutar_linea(cargas_secundarias, ON)
    fin_si
fin_mientras
```

## Arquitectura (Cómo funciona por debajo)

1. **Analizador Léxico**: Lee el texto y lo separa en "palabras" que el sistema entiende (Tokens).
2. **Analizador Sintáctico**: Lee los tokens y comprueba que las frases formadas tienen sentido estructural, creando un Árbol Sintáctico (AST).
3. **Capa HAL (Hardware Abstraction Layer)**: Traduce los comandos lógicos del lenguaje L (como "apagar línea de carga") a comandos eléctricos físicos que los sensores o relés reales puedan entender.
