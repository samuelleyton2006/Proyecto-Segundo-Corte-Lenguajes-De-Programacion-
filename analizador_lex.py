import sys

class Token:
    def __init__(self, tipo, valor=None, fila=0, columna=0):
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.columna = columna

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor}, {self.fila}, {self.columna})"


# -----------------------------
# Tokens de símbolos y operadores
# -----------------------------
char_tokens = {
    'tk_ejecuta': '->',
    'tk_potencia': '**',
    'tk_mayor_igual': '>=',
    'tk_menor_igual': '<=',
    'tk_igual': '==',
    'tk_distinto': '!=',
    'tk_mas_asig': '+=',
    'tk_menos_asig': '-=',
    'tk_mult_asig': '*=',
    'tk_div_asig': '/=',
    'tk_div_entera': '//',
    'tk_mod_asig': '%=',
    'tk_amper_asig': '&=',
    'tk_bar_asig': '|=',
    'tk_hat_asig': '^=',
    'tk_left_shift_asig': '<<=',
    'tk_right_shift_asig': '>>=',
    'tk_pot_asig': '**=',
    'tk_div_entera_asig': '//=',
    'tk_punto_y_coma': ';',
    'tk_coma': ',',
    'tk_par_izq': '(',
    'tk_par_der': ')',
    'tk_corchete_izq': '[',
    'tk_corchete_der': ']',
    'tk_llave_izq': '{',
    'tk_llave_der': '}',
    'tk_dos_puntos': ':',
    'tk_punto': '.',
    'tk_asig': '=',
    'tk_div': '/',
    'tk_suma': '+',
    'tk_resta': '-',
    'tk_mult': '*',
    'tk_modulo': '%',
    'tk_mayor': '>',
    'tk_menor': '<',
    'tk_arroba': '@',
    'tk_or': '|',
    'tk_and': '&',
    'tk_tilde': '~',
    'tk_xor': '^',
    'tk_left_shift': '<<',
    'tk_right_shift': '>>',
    'tk_colon_asig': ':=',
    'tk_ellipsis': '...',
}

# -----------------------------
# Palabras reservadas
# -----------------------------
palabras_reservadas = {
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break',
    'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for',
    'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or',
    'pass', 'raise', 'return', 'try', 'while', 'with', 'yield', 'print', 'self',
    '__init__'
}

tipos_datos = {'int', 'float', 'str', 'bool', 'list', 'tuple', 'dict', 'set'}


# -----------------------------
# Funciones auxiliares
# -----------------------------
def es_digito(char):
    return char.isdigit()

def es_identificador(char):
    return char.isalpha() or char == '_'

def es_cadena(char):
    return char in {'"', "'"}


# -----------------------------
# Lexer principal compatible con LL(1)
# -----------------------------
def analizador_lexico(codigo):
    tokens = []
    # Usaremos iter() para tener contexto de la última línea
    lineas = codigo.split('\n')
    indent_stack = [0]
    fila = 0

    lista_tokens = sorted(char_tokens.items(), key=lambda x: len(x[1]), reverse=True)
    
    # ----------------------------------------------------
    # Nueva lista que combina el código con el NEWLINE final 
    # (para asegurar el último NEWLINE es procesado correctamente)
    # ----------------------------------------------------
    lineas_procesar = [linea for linea in lineas]
    
    for linea in lineas_procesar:
        fila += 1
        columna = 0
        
        # 1. Procesar NEWLINE (si no es la primera línea)
        if fila > 1:
            tokens.append(Token("NEWLINE", None, fila, 0))
            
        # Omitir líneas vacías (ya manejado, pero limpio)
        if not linea.strip():
            continue

        # 2. Calcular la indentación y emitir INDENT/DEDENT
        #    Buscar la posición del primer carácter no-espacio
        indent = len(linea) - len(linea.lstrip(' '))
        
        # Eliminar el espacio en blanco de indentación antes de tokenizar
        columna = indent
        
        if indent > indent_stack[-1]:
            indent_stack.append(indent)
            tokens.append(Token("INDENT", None, fila, 1))
        elif indent < indent_stack[-1]:
            while indent < indent_stack[-1]:
                indent_stack.pop()
                tokens.append(Token("DEDENT", None, fila, 1))
        
        if indent != indent_stack[-1]:
            raise Exception(f"Error de indentación en la línea {fila}")

        # 3. Tokenizar el contenido (iniciando después de la indentación)
        while columna < len(linea):
            char = linea[columna]
            
            # ------------------------------------------------------------------
            # *IMPORTANTE*: Eliminar el manejo de espacios aquí, 
            # ya que la indentación ya fue procesada, y solo buscamos tokens.
            # Los espacios INTERNOS entre tokens se ignoran
            # ------------------------------------------------------------------
            if char.isspace():
                columna += 1
                continue
            
            # ... (Resto de la lógica de tokenización, sin cambios) ...
            
            # Comentarios
            if char == '#':
                break  # Ignorar comentarios
            
            # Identificadores o palabras reservadas
            if es_identificador(char):
                # ... (Lógica de NAME) ...
                start_col = columna
                palabra = ""
                while columna < len(linea) and (linea[columna].isalnum() or linea[columna] == '_'):
                    palabra += linea[columna]
                    columna += 1
                if palabra in palabras_reservadas:
                    tokens.append(Token(f"'{palabra}'", palabra, fila, start_col))
                else:
                    tokens.append(Token("NAME", palabra, fila, start_col))
                continue

            # Números
            if es_digito(char):
                # ... (Lógica de NUMBER) ...
                start_col = columna
                numero = ""
                has_dot = False
                while columna < len(linea) and (linea[columna].isdigit() or linea[columna] == '.'):
                    if linea[columna] == '.':
                        if has_dot:
                             # Manejar doble punto como error o como parte de un token (como elipsis)
                             # Para simplificar, asumiremos que solo se permite un punto decimal
                             break
                        has_dot = True
                    numero += linea[columna]
                    columna += 1
                tokens.append(Token("NUMBER", numero, fila, start_col))
                continue
            
            if es_cadena(char):
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
                tokens.append(Token("STRING", valor, fila, start_col))
                continue

            matched = False
            for nombre, simbolo in lista_tokens:
                if linea[columna:].startswith(simbolo):
                    tokens.append(Token(nombre, simbolo, fila, columna))
                    columna += len(simbolo)
                    matched = True
                    break
            if matched:
                continue

            raise Exception(f"Error léxico: carácter inesperado '{char}' en línea {fila}, columna {columna}")

    while len(indent_stack) > 1:
        indent_stack.pop()
        tokens.append(Token("DEDENT", None, fila, 1))

    tokens.append(Token("ENDMARKER", None, fila + 1, 0))
    return tokens