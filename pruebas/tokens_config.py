SIMBOLOS = {
    '(': 'tk_par_izq', ')': 'tk_par_der', 
    '[': 'tk_corchete_izq', ']': 'tk_corchete_der',
    '{': 'tk_llave_izq', '}': 'tk_llave_der', 
    ':': 'tk_dos_puntos', ',': 'tk_coma',
    '=': 'tk_asig', '+=': 'tk_mas_asig', 
    '-=': 'tk_menos_asig', '*=': 'tk_mult_asig',
    '/=': 'tk_div_asig', '%=': 'tk_mod_asig', 
    '>=': 'tk_mayor_igual', '<=': 'tk_menor_igual',
    '==': 'tk_igual', '!=': 'tk_distinto', 
    '>': 'tk_mayor', '<': 'tk_menor',
    '+': 'tk_suma', '-': 'tk_resta', 
    '*': 'tk_mult', '/': 'tk_div', 
    '%': 'tk_modulo', '**': 'tk_potencia', 
    '.': 'tk_punto', ';' : 'tk_punto_y_coma'
}

PALABRAS_RESERVADAS = {
    'False', 'None', 'True', 'and', 'as', 'break', 'class', 'continue',
    'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from',
    'if', 'import', 'in', 'is', 'not', 'or', 'pass', 'return', 'try',
    'while', 'print', 'self'
}

SIMBOLOS_INVERTIDOS = {v: k for k, v in SIMBOLOS.items()}