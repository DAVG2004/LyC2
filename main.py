import sys
from lexer import tokenize
from parser_l import Parser
from hal_simulator import HALSimulator
from interpreter import Interpreter

def main():
    """
    Punto de entrada principal para el intérprete del Lenguaje L.
    """
    if len(sys.argv) < 2:
        print("Uso: python main.py <archivo.l>")
        return

    archivo = sys.argv[1]
    print(f"\n--- Iniciando ECO-GRID Runtime ---")
    print(f"Cargando código fuente: {archivo}")
    
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo}' no fue encontrado.")
        return

    try:
        # 1. Análisis Léxico
        tokens = tokenize(codigo)
        
        # 2. Análisis Sintáctico (AST)
        parser = Parser(tokens)
        ast = parser.parse_programa()

        # 3. Interpretación y Simulación HAL
        hal = HALSimulator()
        interprete = Interpreter(hal)
        
        # Configuramos el limite de ciclos para la demo (5 es suficiente para ver los cambios)
        interprete.max_cycles = 5

        interprete.evaluar(ast)
        
    except Exception as e:
        print(f"\n[ERROR FATAL DEL SISTEMA]")
        print(str(e))
        
    print("--- Ejecución Finalizada ---\n")

if __name__ == '__main__':
    main()
