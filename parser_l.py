# parser_l.py
# Nodos del Árbol Sintáctico (AST)

class ASTNode:
    pass

class Programa(ASTNode):
    def __init__(self, ids, bloque):
        self.ids = ids
        self.bloque = bloque

class Asignacion(ASTNode):
    def __init__(self, id_var, expresion):
        self.id_var = id_var
        self.expresion = expresion

class ComandoConmutar(ASTNode):
    def __init__(self, id_linea, estado):
        self.id_linea = id_linea
        self.estado = estado

class Condicional(ASTNode):
    def __init__(self, condicion, bloque):
        self.condicion = condicion
        self.bloque = bloque

class Bucle(ASTNode):
    def __init__(self, condicion, bloque):
        self.condicion = condicion
        self.bloque = bloque

class Condicion(ASTNode):
    def __init__(self, izq, op, der):
        self.izq = izq
        self.op = op
        self.der = der

class ExpresionNum(ASTNode):
    def __init__(self, valor):
        self.valor = valor

class ExpresionID(ASTNode):
    def __init__(self, id_var):
        self.id_var = id_var

class LlamadaFuncion(ASTNode):
    def __init__(self, funcion, argumento):
        self.funcion = funcion
        self.argumento = argumento

# Implementación del Analizador Sintáctico de Descenso Recursivo
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, token_type):
        if self.current_token() and self.current_token().type == token_type:
            token = self.current_token()
            self.pos += 1
            return token
        else:
            esperado = token_type
            encontrado = self.current_token().type if self.current_token() else "EOF"
            linea = self.current_token().line if self.current_token() else "Desconocida"
            raise SyntaxError(f"Error de sintaxis en línea {linea}: se esperaba {esperado}, pero se encontró {encontrado} ('{self.current_token().value if self.current_token() else ''}')")

    def eat_keyword(self, keyword_value):
        if self.current_token() and self.current_token().type == 'KEYWORD' and self.current_token().value == keyword_value:
            token = self.current_token()
            self.pos += 1
            return token
        else:
            linea = self.current_token().line if self.current_token() else "Desconocida"
            raise SyntaxError(f"Error de sintaxis en línea {linea}: se esperaba palabra clave '{keyword_value}'")

    def parse_programa(self):
        # <programa> ::= "init_grid" "(" <lista_ids> ")" <bloque_instrucciones>
        self.eat_keyword('init_grid')
        self.eat('LPAREN')
        ids = self.parse_lista_ids()
        self.eat('RPAREN')
        bloque = self.parse_bloque_instrucciones()
        return Programa(ids, bloque)

    def parse_lista_ids(self):
        # <lista_ids> ::= ID | ID "," <lista_ids>
        ids = []
        token_id = self.eat('ID')
        ids.append(token_id.value)
        while self.current_token() and self.current_token().type == 'COMMA':
            self.eat('COMMA')
            token_id = self.eat('ID')
            ids.append(token_id.value)
        return ids

    def parse_bloque_instrucciones(self):
        # <bloque_instrucciones> ::= <instruccion> | <instruccion> <bloque_instrucciones>
        instrucciones = []
        while self.current_token() and self.current_token().type != 'EOF':
            # Detener el bloque si encontramos un cierre de estructura de control
            if self.current_token().type == 'KEYWORD' and self.current_token().value in ('fin_si', 'fin_mientras'):
                break
            instrucciones.append(self.parse_instruccion())
        return instrucciones

    def parse_instruccion(self):
        # <instruccion> ::= <asignacion> | <comando_conmutar> | <condicional> | <bucle>
        token = self.current_token()
        if token.type == 'ID':
            return self.parse_asignacion()
        elif token.type == 'KEYWORD':
            if token.value == 'conmutar_linea':
                return self.parse_comando_conmutar()
            elif token.value == 'si':
                return self.parse_condicional()
            elif token.value == 'mientras':
                return self.parse_bucle()
        raise SyntaxError(f"Instrucción no válida en la línea {token.line}: '{token.value}'")

    def parse_asignacion(self):
        # <asignacion> ::= ID "=" <expresion>
        id_token = self.eat('ID')
        self.eat('OP_ASIG')
        expr = self.parse_expresion()
        return Asignacion(id_token.value, expr)

    def parse_expresion(self):
        # <expresion> ::= NUM | ID | "leer_temperatura" "(" ID ")" | "estado_carga" "(" ID ")"
        token = self.current_token()
        if token.type == 'NUM':
            self.eat('NUM')
            return ExpresionNum(token.value)
        elif token.type == 'ID':
            self.eat('ID')
            return ExpresionID(token.value)
        elif token.type == 'KEYWORD' and token.value in ('leer_temperatura', 'estado_carga'):
            func_name = self.eat('KEYWORD').value
            self.eat('LPAREN')
            id_token = self.eat('ID')
            self.eat('RPAREN')
            return LlamadaFuncion(func_name, id_token.value)
        else:
            raise SyntaxError(f"Expresión no válida en la línea {token.line}")

    def parse_comando_conmutar(self):
        # <comando_conmutar> ::= "conmutar_linea" "(" ID "," <estado> ")"
        self.eat_keyword('conmutar_linea')
        self.eat('LPAREN')
        id_token = self.eat('ID')
        self.eat('COMMA')
        estado_token = self.eat('ESTADO')
        self.eat('RPAREN')
        return ComandoConmutar(id_token.value, estado_token.value)

    def parse_condicional(self):
        # <condicional> ::= "si" <condicion> "entonces" <bloque_instrucciones> "fin_si"
        self.eat_keyword('si')
        cond = self.parse_condicion()
        self.eat_keyword('entonces')
        bloque = self.parse_bloque_instrucciones()
        self.eat_keyword('fin_si')
        return Condicional(cond, bloque)

    def parse_bucle(self):
        # <bucle> ::= "mientras" <condicion> "ejecutar" <bloque_instrucciones> "fin_mientras"
        self.eat_keyword('mientras')
        cond = self.parse_condicion()
        self.eat_keyword('ejecutar')
        bloque = self.parse_bloque_instrucciones()
        self.eat_keyword('fin_mientras')
        return Bucle(cond, bloque)

    def parse_condicion(self):
        # <condicion> ::= <expresion> OP_COMP <expresion>
        izq = self.parse_expresion()
        op_token = self.eat('OP_COMP')
        der = self.parse_expresion()
        return Condicion(izq, op_token.value, der)
