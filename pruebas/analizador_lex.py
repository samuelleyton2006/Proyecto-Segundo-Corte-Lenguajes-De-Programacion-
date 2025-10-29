class Token:
    def __init__(self, tipo, valor=None, fila=0, columna=0):
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.columna = columna

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor}, {self.fila}, {self.columna})"
from tokens_config import SIMBOLOS, PALABRAS_RESERVADAS


tipos_datos = {'int', 'float', 'str', 'bool', 'list', 'tuple', 'dict', 'set'}

    
def analizador_lexico(codigo):
    tokens = []
    lineas = codigo.split("\n")
    indent_stack = [0]
    fila = 0

    # Mapeo directo de símbolos simples a gramática
  

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
                if palabra in PALABRAS_RESERVADAS:
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
                # Verificar si el punto anterior es de un número flotante
                es_decimal = False
                if tokens and tokens[-1].tipo == "tk_punto":
                    # Es parte de un decimal, no separar
                    es_decimal = True
                
                while columna < len(linea) and (linea[columna].isdigit() or linea[columna] == '.'):
                    numero += linea[columna]
                    columna += 1
                
                # Separar float en tk_entero + tk_punto + tk_entero solo si NO es atributo
                if '.' in numero and not es_decimal:
                    partes = numero.split('.')
                    tokens.append(Token("tk_entero", partes[0], fila, start_col))
                    tokens.append(Token("tk_punto", '.', fila, start_col + len(partes[0])))
                    if len(partes) > 1 and partes[1]:
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
            for sym, tipo in sorted(SIMBOLOS.items(), key=lambda x: -len(x[0])):  # priorizar multi-char
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