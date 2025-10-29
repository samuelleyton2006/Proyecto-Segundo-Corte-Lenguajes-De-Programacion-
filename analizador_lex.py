class Token:
    def __init__(self, tipo, valor=None, fila=0, columna=0):
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.columna = columna

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor}, {self.fila}, {self.columna})"


# -----------------------------
# Palabras reservadas y tipos
# -----------------------------
palabras_reservadas = {
    'False', 'None', 'True', 'and', 'as', 'break', 'class', 'continue',
    'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from',
    'if', 'import', 'in', 'is', 'not', 'or', 'pass', 'return', 'try',
    'while', 'print', 'self', '__init__'
}

tipos_datos = {'int', 'float', 'str', 'bool', 'list', 'tuple', 'dict', 'set'}


# -----------------------------
# Lexer principal
# -----------------------------
def analizador_lexico(codigo):
    tokens = []
    lineas = codigo.split("\n")
    indent_stack = [0]
    fila = 0

    # Mapeo directo de símbolos simples a gramática
    simbolos = {
        '(': 'tk_par_izq', ')': 'tk_par_der', '[': 'tk_corchete_izq', ']': 'tk_corchete_der',
        '{': 'tk_llave_izq', '}': 'tk_llave_der', ':': 'tk_dos_puntos', ',': 'tk_coma',
        '=': 'tk_asig', '+=': 'tk_mas_asig', '-=': 'tk_menos_asig', '*=': 'tk_mult_asig',
        '/=': 'tk_div_asig', '%=': 'tk_mod_asig', '>=': 'tk_mayor_igual', '<=': 'tk_menor_igual',
        '==': 'tk_igual', '!=': 'tk_distinto', '>': 'tk_mayor', '<': 'tk_menor',
        '+': 'tk_suma', '-': 'tk_resta', '*': 'tk_mult', '/': 'tk_div', '%': 'tk_modulo',
        '**': 'tk_potencia'
    }

    for linea in lineas:
        fila += 1
        columna = 0
        if fila > 1:
            tokens.append(Token("NEWLINE", None, fila, 0))

        if not linea.strip():
            continue

        # Calcular indentación
        indent = len(linea) - len(linea.lstrip(' '))
        columna = indent

        if indent > indent_stack[-1]:
            indent_stack.append(indent)
            tokens.append(Token("TAB", None, fila, 0))
        elif indent < indent_stack[-1]:
            while indent < indent_stack[-1]:
                indent_stack.pop()
                tokens.append(Token("TABend", None, fila, 0))
        elif indent != indent_stack[-1]:
            raise Exception(f"Error de indentación en línea {fila}")

        # Procesar contenido
        while columna < len(linea):
            char = linea[columna]

            if char.isspace():
                columna += 1
                continue

            # Comentarios
            if char == '#':
                break

            # Identificador o palabra reservada
            if char.isalpha() or char == '_':
                start_col = columna
                palabra = ""
                while columna < len(linea) and (linea[columna].isalnum() or linea[columna] == '_'):
                    palabra += linea[columna]
                    columna += 1
                if palabra in palabras_reservadas:
                    if palabra == 'self':
                        tokens.append(Token("self", palabra, fila, start_col))
                    else:
                        tokens.append(Token(palabra, palabra, fila, start_col))
                else:
                    tokens.append(Token("id", palabra, fila, start_col))
                continue

            # Número (entero o float)
            if char.isdigit():
                start_col = columna
                numero = ""
                while columna < len(linea) and (linea[columna].isdigit() or linea[columna] == '.'):
                    numero += linea[columna]
                    columna += 1
                # Separar float en tk_entero + tk_punto + tk_entero
                if '.' in numero:
                    partes = numero.split('.')
                    tokens.append(Token("tk_entero", partes[0], fila, start_col))
                    tokens.append(Token("tk_punto", '.', fila, start_col + len(partes[0])))
                    tokens.append(Token("tk_entero", partes[1], fila, start_col + len(numero) - len(partes[1])))
                else:
                    tokens.append(Token("tk_entero", numero, fila, start_col))
                continue

            # Strings
            if char == '"' or char == "'":
                quote = char
                start_col = columna
                columna += 1
                valor = ""
                while columna < len(linea) and linea[columna] != quote:
                    valor += linea[columna]
                    columna += 1
                if columna == len(linea):
                    raise Exception(f"Error léxico: cadena sin cerrar en línea {fila}")
                columna += 1
                tokens.append(Token("tk_cadena", valor, fila, start_col))
                continue

            # Operadores y símbolos
            matched = False
            for sym, tipo in sorted(simbolos.items(), key=lambda x: -len(x[0])):  # priorizar multi-char
                if linea[columna:columna + len(sym)] == sym:
                    tokens.append(Token(tipo, sym, fila, columna))
                    columna += len(sym)
                    matched = True
                    break
            if matched:
                continue

            raise Exception(f"Error léxico: carácter inesperado '{char}' en línea {fila}, columna {columna}")

    # Procesar dedents al final
    while len(indent_stack) > 1:
        indent_stack.pop()
        tokens.append(Token("TABend", None, fila, 0))

    tokens.append(Token("ENDMARKER", "$", fila + 1, 0))
    return tokens
