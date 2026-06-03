import re

class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, '{self.value}')"

def tokenize(code):
    """Convierte el código fuente en una lista de Tokens válidos según las Regex"""
    token_specification = [
        ('KEYWORD',  r'\b(init_grid|leer_temperatura|estado_carga|conmutar_linea|si|entonces|fin_si|mientras|ejecutar|fin_mientras)\b'),
        ('ESTADO',   r'\b(ON|OFF)\b'),
        ('ID',       r'[a-zA-Z][a-zA-Z0-9_]*'),
        ('NUM',      r'\d+(\.\d+)?'),
        ('OP_COMP',  r'==|!=|<|>'),
        ('OP_ASIG',  r'='),
        ('LPAREN',   r'\('),
        ('RPAREN',   r'\)'),
        ('COMMA',    r','),
        ('NEWLINE',  r'\n'),           # Saltos de línea
        ('SKIP',     r'[ \t\r]+'),     # Espacios y tabulaciones
        ('MISMATCH', r'.'),            # Cualquier otro carácter
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    tokens = []
    
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == 'NEWLINE':
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            if value.strip() == '': 
                continue
            raise RuntimeError(f'Error léxico en la línea {line_num}: Carácter inesperado {value}')
        
        # Convertir los tipos numéricos para uso directo
        if kind == 'NUM':
            value = float(value) if '.' in value else int(value)
            
        tokens.append(Token(kind, value, line_num))
    
    tokens.append(Token('EOF', '', line_num))
    return tokens
