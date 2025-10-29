class ParserLL1:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.token_actual = tokens[0] if tokens else None
        self.errores = []

    def avanzar(self):
        """Avanza al siguiente token"""
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.token_actual = self.tokens[self.pos]

    def match(self, tipo_esperado):
        """Verifica y consume un token del tipo esperado"""
        if self.token_actual.tipo == tipo_esperado:
            self.avanzar()
            return True
        else:
            self.error(f"Se esperaba '{tipo_esperado}' pero se encontró '{self.token_actual.tipo}'")
            return False

    def error(self, mensaje):
        """Registra un error sintáctico"""
        error_msg = f"Error sintáctico en línea {self.token_actual.fila}, columna {self.token_actual.columna}: {mensaje}"
        self.errores.append(error_msg)
        raise SyntaxError(error_msg)

    # ===================================================================
    # SÍMBOLO INICIAL
    # ===================================================================

    def programa(self):
        """programa → NEWLINE programa | sentencias ENDMARKER"""
        while self.token_actual.tipo == "NEWLINE":
            self.match("NEWLINE")
        self.sentencias()
        self.match("ENDMARKER")

    # ===================================================================
    # SENTENCIAS
    # ===================================================================

    def sentencias(self):
        """sentencias → sentencia sentencias | ε"""
        while self.token_actual.tipo not in ["ENDMARKER", "TABend"]:
            if self.token_actual.tipo == "NEWLINE":
                self.match("NEWLINE")
            else:
                self.sentencia()

    def sentencia(self):
        """sentencia → sentencia_simple NEWLINE | sentencia_compuesta"""
        if self.token_actual.tipo in ["if", "while", "for", "def", "class", "try"]:
            self.sentencia_compuesta()
        else:
            self.sentencia_simple()
            if self.token_actual.tipo == "NEWLINE":
                self.match("NEWLINE")

    def sentencia_simple(self):
        """sentencia_simple → id sentencia_id | self sentencia_self | expresion | return_stmt | break | continue | pass | del_stmt | import_stmt | print_stmt"""
        if self.token_actual.tipo == "id":
            self.match("id")
            self.sentencia_id()
        elif self.token_actual.tipo == "self":
            self.match("self")
            self.sentencia_self()
        elif self.token_actual.tipo == "return":
            self.return_stmt()
        elif self.token_actual.tipo == "break":
            self.match("break")
        elif self.token_actual.tipo == "continue":
            self.match("continue")
        elif self.token_actual.tipo == "pass":
            self.match("pass")
        elif self.token_actual.tipo == "del":
            self.del_stmt()
        elif self.token_actual.tipo in ["import", "from"]:
            self.import_stmt()
        elif self.token_actual.tipo == "print":
            self.print_stmt()
        elif self.token_actual.tipo in ["tk_entero", "tk_cadena", "True", "False", "None", 
                                         "tk_par_izq", "tk_corchete_izq", "tk_llave_izq",
                                         "tk_suma", "tk_resta", "not"]:
            self.expresion()
        else:
            self.error(f"Token inesperado '{self.token_actual.tipo}' al inicio de sentencia")
    
    def sentencia_self(self):
        """sentencia_self → tk_punto id sentencia_id_dot | tk_par_izq args_opt tk_par_der"""
        if self.token_actual.tipo == "tk_punto":
            self.match("tk_punto")
            self.match("id")
            self.sentencia_id_dot()
        elif self.token_actual.tipo == "tk_par_izq":
            self.match("tk_par_izq")
            self.args_opt()
            self.match("tk_par_der")

    def sentencia_id(self):
        """sentencia_id → op_asignacion expresion | tk_corchete_izq expresion tk_corchete_der tk_asig expresion | tk_par_izq args_opt tk_par_der | tk_punto id sentencia_id_dot"""
        if self.token_actual.tipo in ["tk_asig", "tk_mas_asig", "tk_menos_asig", "tk_mult_asig", "tk_div_asig", "tk_mod_asig"]:
            self.op_asignacion()
            self.expresion()
        elif self.token_actual.tipo == "tk_corchete_izq":
            self.match("tk_corchete_izq")
            self.expresion()
            self.match("tk_corchete_der")
            self.match("tk_asig")
            self.expresion()
        elif self.token_actual.tipo == "tk_par_izq":
            self.match("tk_par_izq")
            self.args_opt()
            self.match("tk_par_der")
        elif self.token_actual.tipo == "tk_punto":
            self.match("tk_punto")
            self.match("id")
            self.sentencia_id_dot()
    
    def sentencia_id_dot(self):
        """sentencia_id_dot → op_asignacion expresion | tk_corchete_izq expresion tk_corchete_der tk_asig expresion | tk_par_izq args_opt tk_par_der | tk_punto id sentencia_id_dot | ε"""
        if self.token_actual.tipo in ["tk_asig", "tk_mas_asig", "tk_menos_asig", "tk_mult_asig", "tk_div_asig", "tk_mod_asig"]:
            self.op_asignacion()
            self.expresion()
        elif self.token_actual.tipo == "tk_corchete_izq":
            self.match("tk_corchete_izq")
            self.expresion()
            self.match("tk_corchete_der")
            self.match("tk_asig")
            self.expresion()
        elif self.token_actual.tipo == "tk_par_izq":
            self.match("tk_par_izq")
            self.args_opt()
            self.match("tk_par_der")
        elif self.token_actual.tipo == "tk_punto":
            self.match("tk_punto")
            self.match("id")
            self.sentencia_id_dot()

    def op_asignacion(self):
        """op_asignacion → tk_asig | tk_mas_asig | tk_menos_asig | tk_mult_asig | tk_div_asig | tk_mod_asig"""
        if self.token_actual.tipo == "tk_asig":
            self.match("tk_asig")
        elif self.token_actual.tipo == "tk_mas_asig":
            self.match("tk_mas_asig")
        elif self.token_actual.tipo == "tk_menos_asig":
            self.match("tk_menos_asig")
        elif self.token_actual.tipo == "tk_mult_asig":
            self.match("tk_mult_asig")
        elif self.token_actual.tipo == "tk_div_asig":
            self.match("tk_div_asig")
        elif self.token_actual.tipo == "tk_mod_asig":
            self.match("tk_mod_asig")

    # ===================================================================
    # OTRAS SENTENCIAS SIMPLES
    # ===================================================================

    def return_stmt(self):
        """return_stmt → return expresion_opt"""
        self.match("return")
        self.expresion_opt()

    def expresion_opt(self):
        """expresion_opt → expresion | ε"""
        if self.token_actual.tipo not in ["NEWLINE", "ENDMARKER"]:
            self.expresion()

    def del_stmt(self):
        """del_stmt → del id"""
        self.match("del")
        self.match("id")

    def import_stmt(self):
        """import_stmt → import id import_as | from id import id import_as"""
        if self.token_actual.tipo == "import":
            self.match("import")
            self.match("id")
            self.import_as()
        elif self.token_actual.tipo == "from":
            self.match("from")
            self.match("id")
            self.match("import")
            self.match("id")
            self.import_as()

    def import_as(self):
        """import_as → as id | ε"""
        if self.token_actual.tipo == "as":
            self.match("as")
            self.match("id")

    def print_stmt(self):
        """print_stmt → print tk_par_izq args_opt tk_par_der"""
        self.match("print")
        self.match("tk_par_izq")
        self.args_opt()
        self.match("tk_par_der")

    # ===================================================================
    # SENTENCIAS COMPUESTAS
    # ===================================================================

    def sentencia_compuesta(self):
        """sentencia_compuesta → if_stmt | while_stmt | for_stmt | def_stmt | class_stmt | try_stmt"""
        if self.token_actual.tipo == "if":
            self.if_stmt()
        elif self.token_actual.tipo == "while":
            self.while_stmt()
        elif self.token_actual.tipo == "for":
            self.for_stmt()
        elif self.token_actual.tipo == "def":
            self.def_stmt()
        elif self.token_actual.tipo == "class":
            self.class_stmt()
        elif self.token_actual.tipo == "try":
            self.try_stmt()

    def if_stmt(self):
        """if_stmt → if expresion tk_dos_puntos bloque elif_chain else_opt"""
        self.match("if")
        self.expresion()
        self.match("tk_dos_puntos")
        self.bloque()
        self.elif_chain()
        self.else_opt()

    def elif_chain(self):
        """elif_chain → elif expresion tk_dos_puntos bloque elif_chain | ε"""
        if self.token_actual.tipo == "elif":
            self.match("elif")
            self.expresion()
            self.match("tk_dos_puntos")
            self.bloque()
            self.elif_chain()

    def else_opt(self):
        """else_opt → else tk_dos_puntos bloque | ε"""
        if self.token_actual.tipo == "else":
            self.match("else")
            self.match("tk_dos_puntos")
            self.bloque()

    def while_stmt(self):
        """while_stmt → while expresion tk_dos_puntos bloque"""
        self.match("while")
        self.expresion()
        self.match("tk_dos_puntos")
        self.bloque()

    def for_stmt(self):
        """for_stmt → for id in expresion tk_dos_puntos bloque"""
        self.match("for")
        self.match("id")
        self.match("in")
        self.expresion()
        self.match("tk_dos_puntos")
        self.bloque()

    def def_stmt(self):
        """def_stmt → def id tk_par_izq parametros tk_par_der tk_dos_puntos bloque"""
        self.match("def")
        self.match("id")
        self.match("tk_par_izq")
        self.parametros()
        self.match("tk_par_der")
        self.match("tk_dos_puntos")
        self.bloque()

    def parametros(self):
        """parametros → parametro lista_parametros | ε"""
        if self.token_actual.tipo == "id" or self.token_actual.tipo == "self":
            self.parametro()
            self.lista_parametros()

    def lista_parametros(self):
        """lista_parametros → tk_coma parametro lista_parametros | ε"""
        if self.token_actual.tipo == "tk_coma":
            self.match("tk_coma")
            self.parametro()
            self.lista_parametros()

    def parametro(self):
        """parametro → id param_default | self param_default"""
        if self.token_actual.tipo == "id":
            self.match("id")
            self.param_default()
        elif self.token_actual.tipo == "self":
            self.match("self")
            self.param_default()

    def param_default(self):
        """param_default → tk_asig expresion | ε"""
        if self.token_actual.tipo == "tk_asig":
            self.match("tk_asig")
            self.expresion()

    def class_stmt(self):
        """class_stmt → class id herencia_opt tk_dos_puntos bloque"""
        self.match("class")
        self.match("id")
        self.herencia_opt()
        self.match("tk_dos_puntos")
        self.bloque()

    def herencia_opt(self):
        """herencia_opt → tk_par_izq id tk_par_der | ε"""
        if self.token_actual.tipo == "tk_par_izq":
            self.match("tk_par_izq")
            self.match("id")
            self.match("tk_par_der")

    def try_stmt(self):
        """try_stmt → try tk_dos_puntos bloque except_clauses finally_opt"""
        self.match("try")
        self.match("tk_dos_puntos")
        self.bloque()
        self.except_clauses()
        self.finally_opt()

    def except_clauses(self):
        """except_clauses → except except_tipo tk_dos_puntos bloque except_clauses | ε"""
        if self.token_actual.tipo == "except":
            self.match("except")
            self.except_tipo()
            self.match("tk_dos_puntos")
            self.bloque()
            self.except_clauses()

    def except_tipo(self):
        """except_tipo → id | ε"""
        if self.token_actual.tipo == "id":
            self.match("id")

    def finally_opt(self):
        """finally_opt → finally tk_dos_puntos bloque | ε"""
        if self.token_actual.tipo == "finally":
            self.match("finally")
            self.match("tk_dos_puntos")
            self.bloque()

    def bloque(self):
        """bloque → NEWLINE TAB sentencias TABend"""
        self.match("NEWLINE")
        self.match("TAB")
        self.sentencias()
        self.match("TABend")

    # ===================================================================
    # EXPRESIONES
    # ===================================================================

    def expresion(self):
        """expresion → expr_or"""
        self.expr_or()

    def expr_or(self):
        """expr_or → expr_and expr_or_prime"""
        self.expr_and()
        self.expr_or_prime()

    def expr_or_prime(self):
        """expr_or_prime → or expr_and expr_or_prime | ε"""
        if self.token_actual.tipo == "or":
            self.match("or")
            # Verificar que después del operador haya algo válido
            if self.token_actual.tipo in ["tk_dos_puntos", "NEWLINE", "ENDMARKER", "tk_par_der", "tk_corchete_der", "tk_coma"]:
                self.error(f"Expresión incompleta después de 'or'")
            self.expr_and()
            self.expr_or_prime()

    def expr_and(self):
        """expr_and → expr_not expr_and_prime"""
        self.expr_not()
        self.expr_and_prime()

    def expr_and_prime(self):
        """expr_and_prime → and expr_not expr_and_prime | ε"""
        if self.token_actual.tipo == "and":
            self.match("and")
            # Verificar que después del operador haya algo válido
            if self.token_actual.tipo in ["tk_dos_puntos", "NEWLINE", "ENDMARKER", "tk_par_der", "tk_corchete_der", "tk_coma"]:
                self.error(f"Expresión incompleta después de 'and'")
            self.expr_not()
            self.expr_and_prime()

    def expr_not(self):
        """expr_not → not expr_not | expr_comparacion"""
        if self.token_actual.tipo == "not":
            self.match("not")
            # Verificar que después de 'not' haya algo válido
            if self.token_actual.tipo in ["tk_dos_puntos", "NEWLINE", "ENDMARKER", "tk_par_der", "tk_corchete_der", "tk_coma"]:
                self.error(f"Expresión incompleta después de 'not'")
            self.expr_not()
        else:
            self.expr_comparacion()

    def expr_comparacion(self):
        """expr_comparacion → expr_aritmetica expr_comp_prime"""
        self.expr_aritmetica()
        self.expr_comp_prime()

    def expr_comp_prime(self):
        """expr_comp_prime → op_comparacion expr_aritmetica expr_comp_prime | ε"""
        if self.token_actual.tipo in ["tk_igual", "tk_distinto", "tk_menor", "tk_menor_igual", "tk_mayor", "tk_mayor_igual", "in", "is"]:
            self.op_comparacion()
            self.expr_aritmetica()
            self.expr_comp_prime()

    def op_comparacion(self):
        """op_comparacion → tk_igual | tk_distinto | tk_menor | tk_menor_igual | tk_mayor | tk_mayor_igual | in | is not | is"""
        if self.token_actual.tipo == "is":
            self.match("is")
            if self.token_actual.tipo == "not":
                self.match("not")
        elif self.token_actual.tipo in ["tk_igual", "tk_distinto", "tk_menor", "tk_menor_igual", "tk_mayor", "tk_mayor_igual", "in"]:
            tipo = self.token_actual.tipo
            self.match(self.token_actual.tipo)
            # Verificar que después del operador haya algo válido
            if self.token_actual.tipo in ["tk_dos_puntos", "NEWLINE", "ENDMARKER", "tk_par_der", "tk_corchete_der"]:
                self.error(f"Expresión incompleta después del operador de comparación")
        else:
            self.error(f"Se esperaba operador de comparación pero se encontró '{self.token_actual.tipo}'")

    def expr_aritmetica(self):
        """expr_aritmetica → termino expr_arit_prime"""
        self.termino()
        self.expr_arit_prime()

    def expr_arit_prime(self):
        """expr_arit_prime → tk_suma termino expr_arit_prime | tk_resta termino expr_arit_prime | ε"""
        if self.token_actual.tipo in ["tk_suma", "tk_resta"]:
            self.match(self.token_actual.tipo)
            # Verificar que después del operador haya algo válido para un término
            if self.token_actual.tipo in ["tk_dos_puntos", "NEWLINE", "ENDMARKER", "tk_par_der", "tk_corchete_der", "tk_coma"]:
                self.error(f"Expresión incompleta después del operador aritmético")
            self.termino()
            self.expr_arit_prime()

    def termino(self):
        """termino → factor termino_prime"""
        self.factor()
        self.termino_prime()

    def termino_prime(self):
        """termino_prime → tk_mult factor termino_prime | tk_div factor termino_prime | tk_modulo factor termino_prime | ε"""
        if self.token_actual.tipo in ["tk_mult", "tk_div", "tk_modulo"]:
            self.match(self.token_actual.tipo)
            # Verificar que después del operador haya algo válido
            if self.token_actual.tipo in ["tk_dos_puntos", "NEWLINE", "ENDMARKER", "tk_par_der", "tk_corchete_der", "tk_coma"]:
                self.error(f"Expresión incompleta después del operador de multiplicación/división")
            self.factor()
            self.termino_prime()

    def factor(self):
        """factor → tk_suma factor | tk_resta factor | potencia"""
        if self.token_actual.tipo == "tk_suma":
            self.match("tk_suma")
            self.factor()
        elif self.token_actual.tipo == "tk_resta":
            self.match("tk_resta")
            self.factor()
        else:
            self.potencia()

    def potencia(self):
        """potencia → atom potencia_prime"""
        self.atom()
        self.potencia_prime()

    def potencia_prime(self):
        """potencia_prime → tk_potencia factor | ε"""
        if self.token_actual.tipo == "tk_potencia":
            self.match("tk_potencia")
            # Verificar que después del operador haya algo válido
            if self.token_actual.tipo in ["tk_dos_puntos", "NEWLINE", "ENDMARKER", "tk_par_der", "tk_corchete_der", "tk_coma"]:
                self.error(f"Expresión incompleta después del operador de potencia")
            self.factor()

    def atom(self):
        """atom → id atom_suffix | self atom_suffix | numero | tk_cadena | True | False | None | tk_par_izq expresion tk_par_der | lista | tupla | diccionario | conjunto"""
        if self.token_actual.tipo == "id":
            self.match("id")
            self.atom_suffix()
        elif self.token_actual.tipo == "self":
            self.match("self")
            self.atom_suffix()
        elif self.token_actual.tipo == "tk_entero":
            self.numero()
        elif self.token_actual.tipo == "tk_cadena":
            self.match("tk_cadena")
        elif self.token_actual.tipo == "True":
            self.match("True")
        elif self.token_actual.tipo == "False":
            self.match("False")
        elif self.token_actual.tipo == "None":
            self.match("None")
        elif self.token_actual.tipo == "tk_par_izq":
            self.match("tk_par_izq")
            if self.token_actual.tipo == "tk_par_der":
                # Tupla vacía
                self.match("tk_par_der")
            else:
                self.expresion()
                if self.token_actual.tipo == "tk_coma":
                    # Es una tupla
                    self.match("tk_coma")
                    self.elementos_tupla_tail()
                    self.match("tk_par_der")
                else:
                    # Es una expresión entre paréntesis
                    self.match("tk_par_der")
        elif self.token_actual.tipo == "tk_corchete_izq":
            self.lista()
        elif self.token_actual.tipo == "tk_llave_izq":
            # Puede ser diccionario o conjunto
            self.match("tk_llave_izq")
            if self.token_actual.tipo == "tk_llave_der":
                # Diccionario vacío
                self.match("tk_llave_der")
            else:
                self.expresion()
                if self.token_actual.tipo == "tk_dos_puntos":
                    # Es un diccionario
                    self.match("tk_dos_puntos")
                    self.expresion()
                    self.elementos_dict_tail()
                    self.match("tk_llave_der")
                else:
                    # Es un conjunto
                    self.elementos_conjunto_tail()
                    self.match("tk_llave_der")

    def atom_suffix(self):
        """atom_suffix → tk_par_izq args_opt tk_par_der atom_suffix | tk_corchete_izq expresion tk_corchete_der atom_suffix | tk_punto id atom_suffix | ε"""
        if self.token_actual.tipo == "tk_par_izq":
            self.match("tk_par_izq")
            self.args_opt()
            self.match("tk_par_der")
            self.atom_suffix()
        elif self.token_actual.tipo == "tk_corchete_izq":
            self.match("tk_corchete_izq")
            self.expresion()
            self.match("tk_corchete_der")
            self.atom_suffix()
        elif self.token_actual.tipo == "tk_punto":
            self.match("tk_punto")
            self.match("id")
            self.atom_suffix()

    def numero(self):
        """numero → tk_entero numero_decimal"""
        self.match("tk_entero")
        self.numero_decimal()

    def numero_decimal(self):
        """numero_decimal → tk_punto tk_entero | ε"""
        if self.token_actual.tipo == "tk_punto":
            self.match("tk_punto")
            self.match("tk_entero")

    # ===================================================================
    # ARGUMENTOS
    # ===================================================================

    def args_opt(self):
        """args_opt → args | ε"""
        if self.token_actual.tipo not in ["tk_par_der"]:
            self.args()

    def args(self):
        """args → expresion args_tail"""
        self.expresion()
        self.args_tail()

    def args_tail(self):
        """args_tail → tk_coma expresion args_tail | ε"""
        if self.token_actual.tipo == "tk_coma":
            self.match("tk_coma")
            self.expresion()
            self.args_tail()

    # ===================================================================
    # ESTRUCTURAS DE DATOS
    # ===================================================================

    def lista(self):
        """lista → tk_corchete_izq elementos_lista tk_corchete_der"""
        self.match("tk_corchete_izq")
        self.elementos_lista()
        self.match("tk_corchete_der")

    def elementos_lista(self):
        """elementos_lista → expresion elementos_lista_tail | ε"""
        if self.token_actual.tipo != "tk_corchete_der":
            self.expresion()
            self.elementos_lista_tail()

    def elementos_lista_tail(self):
        """elementos_lista_tail → tk_coma expresion elementos_lista_tail | ε"""
        if self.token_actual.tipo == "tk_coma":
            self.match("tk_coma")
            self.expresion()
            self.elementos_lista_tail()

    def elementos_tupla_tail(self):
        """elementos_tupla_tail → expresion elementos_tupla_tail_cont | ε"""
        if self.token_actual.tipo != "tk_par_der":
            self.expresion()
            self.elementos_tupla_tail_cont()

    def elementos_tupla_tail_cont(self):
        """elementos_tupla_tail_cont → tk_coma expresion elementos_tupla_tail_cont | ε"""
        if self.token_actual.tipo == "tk_coma":
            self.match("tk_coma")
            self.expresion()
            self.elementos_tupla_tail_cont()

    def elementos_dict_tail(self):
        """elementos_dict_tail → tk_coma par_dict elementos_dict_tail | ε"""
        if self.token_actual.tipo == "tk_coma":
            self.match("tk_coma")
            self.par_dict()
            self.elementos_dict_tail()

    def par_dict(self):
        """par_dict → expresion tk_dos_puntos expresion"""
        self.expresion()
        self.match("tk_dos_puntos")
        self.expresion()

    def elementos_conjunto_tail(self):
        """elementos_conjunto_tail → tk_coma expresion elementos_conjunto_tail | ε"""
        if self.token_actual.tipo == "tk_coma":
            self.match("tk_coma")
            self.expresion()
            self.elementos_conjunto_tail()


# ===================================================================
# FUNCIÓN PRINCIPAL PARA USAR EL PARSER
# ===================================================================

def parsear(tokens):
    """
    Función principal para analizar una lista de tokens
    Retorna True si no hay errores, False en caso contrario
    """
    try:
        parser = ParserLL1(tokens)
        parser.programa()
        print("✓ Análisis sintáctico completado exitosamente")
        return True
    except SyntaxError as e:
        print(f"✗ {e}")
        return False


# ===================================================================
# EJECUCIÓN DESDE LÍNEA DE COMANDOS
# ===================================================================

if __name__ == "__main__":
    import sys
    from analizador_lex import analizador_lexico  # Asume que el lexer está en lexer.py
    
    # Verificar que se proporcione un argumento
    if len(sys.argv) < 2:
        print("Uso: python parser.py <archivo.py>")
        print("Ejemplo: python parser.py programa.py")
        sys.exit(1)
    
    archivo = sys.argv[1]
    
    try:
        # Leer el archivo
        with open(archivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        print(f"Analizando archivo: {archivo}")
        print("=" * 60)
        
        # Análisis léxico
        print("\n[1] Análisis Léxico...")
        tokens = analizador_lexico(codigo)
        print(f"✓ Se generaron {len(tokens)} tokens")
        
        # Análisis sintáctico
        print("\n[2] Análisis Sintáctico...")
        resultado = parsear(tokens)
        
        print("\n" + "=" * 60)
        if resultado:
            print("RESULTADO: ✓ El archivo es sintácticamente correcto")
            sys.exit(0)
        else:
            print("RESULTADO: ✗ Se encontraron errores sintácticos")
            sys.exit(1)
            
    except FileNotFoundError:
        print(f"✗ Error: No se encontró el archivo '{archivo}'")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error durante el análisis: {e}")
        sys.exit(1)