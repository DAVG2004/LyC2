from parser_l import (Programa, Asignacion, ComandoConmutar, Condicional, Bucle,
                      Condicion, ExpresionNum, ExpresionID, LlamadaFuncion)

class Interpreter:
    """
    Intérprete para el Lenguaje L que evalúa el AST (Árbol de Sintaxis Abstracta)
    y se comunica con la Capa de Abstracción de Hardware (HAL).
    """
    def __init__(self, hal):
        self.hal = hal
        self.variables = {}
        # Habilitamos un límite de ciclos para que los "mientras 1 == 1" infinitos 
        # no bloqueen el proceso en pruebas demostrativas
        self.max_cycles = 10 
        self.cycle_count = 0

    def evaluar(self, nodo):
        # Determina qué método visitar_X llamar dependiendo del tipo de nodo
        method_name = f'visitar_{type(nodo).__name__}'
        visitante = getattr(self, method_name, self.error_generico)
        return visitante(nodo)

    def error_generico(self, nodo):
        raise Exception(f'Error de interpretación: No se encontró el método para evaluar el nodo de tipo {type(nodo).__name__}')

    def visitar_Programa(self, nodo):
        self.hal.registrar_componentes(nodo.ids)
        self.visitar_Bloque(nodo.bloque)

    def visitar_Bloque(self, instrucciones):
        for instruccion in instrucciones:
            self.evaluar(instruccion)
            # Salvaguarda de bucle infinito para pruebas
            if self.cycle_count > self.max_cycles:
                return

    def visitar_Asignacion(self, nodo):
        valor = self.evaluar(nodo.expresion)
        self.variables[nodo.id_var] = valor

    def visitar_ComandoConmutar(self, nodo):
        self.hal.conmutar_linea(nodo.id_linea, nodo.estado)

    def visitar_Condicional(self, nodo):
        if self.evaluar(nodo.condicion):
            self.visitar_Bloque(nodo.bloque)

    def visitar_Bucle(self, nodo):
        while self.evaluar(nodo.condicion):
            self.cycle_count += 1
            if self.cycle_count > self.max_cycles:
                print("\n[INTERPRETE] Detención de seguridad: Máximo de ciclos de demostración alcanzado para evitar un bucle infinito en la prueba.")
                break
            self.visitar_Bloque(nodo.bloque)

    def visitar_Condicion(self, nodo):
        izq = self.evaluar(nodo.izq)
        der = self.evaluar(nodo.der)
        
        if nodo.op == '==': return izq == der
        elif nodo.op == '!=': return izq != der
        elif nodo.op == '<': return izq < der
        elif nodo.op == '>': return izq > der
        return False

    def visitar_ExpresionNum(self, nodo):
        return nodo.valor

    def visitar_ExpresionID(self, nodo):
        if nodo.id_var in self.variables:
            return self.variables[nodo.id_var]
        raise Exception(f"Error de Ejecución: Variable '{nodo.id_var}' no definida antes de su uso.")

    def visitar_LlamadaFuncion(self, nodo):
        if nodo.funcion == 'leer_temperatura':
            return self.hal.leer_temperatura(nodo.argumento)
        elif nodo.funcion == 'estado_carga':
            return self.hal.estado_carga(nodo.argumento)
        raise Exception(f"Error de Ejecución: Función interna '{nodo.funcion}' no definida.")
