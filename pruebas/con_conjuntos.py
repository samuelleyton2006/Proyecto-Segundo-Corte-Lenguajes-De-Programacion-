import sys


class ParserLL1Completo:
    def __init__(self):
        self.gramatica = self._definir_gramatica()
        
        # Conjuntos calculados
        self.first = {}
        self.follow = {}
        self.tabla_parsing = {}
        
        # Símbolos especiales
        self.epsilon = 'ε'
        self.endmarker = 'ENDMARKER'
        
        self.tokens = []
        self.pos = 0
        self.token_actual = None
        self.errores = []
        
    def _definir_gramatica(self):
        return {
            # Simbolo inicial
            'programa': [
                ['NEWLINE', 'programa'],
                ['sentencias', 'programa_tail']
            ],
            'programa_tail': [
                ['ENDMARKER'],
                ['NEWLINE']
            
            ],
            # Sentencias
            'sentencias': [
                ['sentencia', 'sentencias'],
                ['ε']
            ],
            
            'sentencia': [
                ['sentencia_simple', 'NEWLINE_opt'],
                ['sentencia_compuesta']
            ],
            
            'NEWLINE_opt': [
                ['NEWLINE'],
                ['ε']
            ],
            
            'sentencia_simple': [

                ['id', 'sentencia_id'],
                ['self', 'sentencia_self'],
                ['return_stmt'],
                ['break'],
                ['continue'],
                ['pass'],
                ['del_stmt'],
                ['import_stmt'],
                ['print_stmt']
                
            ],
            
            # Sentencias con id y self
            'sentencia_id': [
                ['op_asignacion', 'expresion'],
                ['tk_corchete_izq', 'expresion', 'tk_corchete_der', 'tk_asig', 'expresion'],
                ['tk_par_izq', 'args_opt', 'tk_par_der'],
                ['tk_punto', 'id', 'sentencia_id_dot']

            ],
            #Ejemplos:
            #x = 2
            #lista[0] = 1
            #f(3)
            #obj.atributo = 2

         
            'sentencia_self': [
                ['tk_punto', 'id', 'sentencia_id_dot'],
                ['tk_par_izq', 'args_opt', 'tk_par_der']
            ],
            
            'sentencia_id_dot': [
                ['op_asignacion', 'expresion'],
                ['tk_corchete_izq', 'expresion', 'tk_corchete_der', 'tk_asig', 'expresion'],
                ['tk_par_izq', 'args_opt', 'tk_par_der'],
                ['tk_punto', 'id', 'sentencia_id_dot'],
                ['ε']
            ],
            
            # Operadores de asignación
            'op_asignacion': [
                ['tk_asig'],
                ['tk_mas_asig'],
                ['tk_menos_asig'],
                ['tk_mult_asig'],
                ['tk_div_asig'],
                ['tk_mod_asig']
            ],
            
            # Otras sentencias simples
            'return_stmt': [
                ['return', 'expresion_opt']
            ],
            
            'expresion_opt': [
                ['expresion'],
                ['ε']
            ],
            
            'del_stmt': [
                ['del', 'id']
            ],
            
            'import_stmt': [
                ['import', 'id', 'import_as'],
                ['from', 'id', 'import', 'id', 'import_as']
            ],
            
            'import_as': [
                ['as', 'id'],
                ['ε']
            ],
            
            'print_stmt': [
                ['print', 'tk_par_izq', 'args_opt', 'tk_par_der']
            ],
            
            # Sentencias compuestas
            'sentencia_compuesta': [
                ['if_stmt'],
                ['while_stmt'],
                ['for_stmt'],
                ['def_stmt'],
                ['class_stmt'],
                ['try_stmt']
            ],
            
            # IF-ELIF-ELSE
            'if_stmt': [
                ['if', 'expresion', 'tk_dos_puntos', 'bloque', 'elif_chain', 'else_opt']
            ],
            
            'elif_chain': [
                ['elif', 'expresion', 'tk_dos_puntos', 'bloque', 'elif_chain'],
                ['ε']
            ],
            
            'else_opt': [
                ['else', 'tk_dos_puntos', 'bloque'],
                ['ε']
            ],
            
            # WHILE
            'while_stmt': [
                ['while', 'expresion', 'tk_dos_puntos', 'bloque']
            ],
            
            # FOR
            'for_stmt': [
                ['for', 'id', 'in', 'expresion', 'tk_dos_puntos', 'bloque']
            ],
            
            # DEF
            'def_stmt': [
                ['def', 'id', 'tk_par_izq', 'parametros', 'tk_par_der', 'tk_dos_puntos', 'bloque']
            ],
            
            'parametros': [
                ['parametro', 'lista_parametros'],
                ['ε']
            ],
            
            'lista_parametros': [
                ['tk_coma', 'parametro', 'lista_parametros'],
                ['ε']
            ],
            
            'parametro': [
                ['id', 'param_anotacion'], #param_default
                ['self', 'param_default']
            ],
            'param_anotacion': [
                ['tk_dos_puntos', 'tipo_anotacion', 'param_default'],
                ['param_default']
            ],
            
            'tipo_anotacion': [
                ['id', 'tipo_suffix']
            ],

            'tipo_suffix': [
                ['tk_punto', 'id', 'tipo_suffix'],
                ['tk_corchete_izq', 'tipo_anotacion', 'tk_corchete_der', 'tipo_suffix'],
                ['ε']
            ],
            'param_default': [
                ['tk_asig', 'expresion'],
                ['ε']
            ],
            
            # CLASS
            'class_stmt': [
                ['class', 'id', 'herencia_opt', 'tk_dos_puntos', 'bloque']
            ],
            
            'herencia_opt': [
                ['tk_par_izq', 'id', 'tk_par_der'],
                ['ε']
            ],
            
            # TRY-EXCEPT-FINALLY
            'try_stmt': [
                ['try', 'tk_dos_puntos', 'bloque', 'except_clauses', 'finally_opt']
            ],
            
            'except_clauses': [
                ['except', 'except_tipo', 'tk_dos_puntos', 'bloque', 'except_clauses'],
                ['ε']
            ],
            
            'except_tipo': [
                ['id'],
                ['ε']
            ],
            
            'finally_opt': [
                ['finally', 'tk_dos_puntos', 'bloque'],
                ['ε']
            ],
            
            # BLOQUE
            'bloque': [
                ['NEWLINE', 'TAB', 'sentencias', 'TABend']
            ],
            
            # EXPRESIONES
            'expresion': [
                ['expr_or']
            ],
            
            # OR lógico
            'expr_or': [
                ['expr_and', 'expr_or_prime']
            ],
            
            'expr_or_prime': [
                ['or', 'expr_and', 'expr_or_prime'],
                ['ε']
            ],
            
            # AND lógico
            'expr_and': [
                ['expr_not', 'expr_and_prime']
            ],
            
            'expr_and_prime': [
                ['and', 'expr_not', 'expr_and_prime'],
                ['ε']
            ],
            
            # NOT lógico
            'expr_not': [
                ['not', 'expr_not'],
                ['expr_comparacion']
            ],
            
            # Comparaciones
            'expr_comparacion': [
                ['expr_aritmetica', 'expr_comp_prime']
            ],
            
            'expr_comp_prime': [
                ['op_comparacion', 'expr_aritmetica', 'expr_comp_prime'],
                ['ε']
            ],
            
            'op_comparacion': [
                ['tk_igual'],
                ['tk_distinto'],
                ['tk_menor'],
                ['tk_menor_igual'],
                ['tk_mayor'],
                ['tk_mayor_igual'],
                ['in'],
                ['is', 'is_not_opt']
            ],
            
            'is_not_opt': [
                ['not'],
                ['ε']
            ],
            
            # Aritmética: suma y resta
            'expr_aritmetica': [
                ['termino', 'expr_arit_prime']
            ],
            
            'expr_arit_prime': [
                ['tk_suma', 'termino', 'expr_arit_prime'],
                ['tk_resta', 'termino', 'expr_arit_prime'],
                ['ε']
            ],
            
            # Aritmética: multiplicación, división, módulo
            'termino': [
                ['factor', 'termino_prime']
            ],
            
            'termino_prime': [
                ['tk_mult', 'factor', 'termino_prime'],
                ['tk_div', 'factor', 'termino_prime'],
                ['tk_modulo', 'factor', 'termino_prime'],
                ['ε']
            ],
            
            # Factor: unarios
            'factor': [
                ['tk_suma', 'factor'],
                ['tk_resta', 'factor'],
                ['potencia']
            ],
            
            # Potencia
            'potencia': [
                ['atom', 'potencia_prime']
            ],
            
            'potencia_prime': [
                ['tk_potencia', 'factor'],
                ['ε']
            ],
            
            # Atómicos
            'atom': [
                ['id', 'atom_suffix'],
                ['self', 'atom_suffix'],
                ['numero'],
                ['tk_cadena'],
                ['True'],
                ['False'],
                ['None'],
                ['tk_par_izq', 'expresion_o_tupla'],
                ['lista'],
                ['diccionario_o_conjunto']
            ],
            
            'expresion_o_tupla': [
                ['expresion', 'tupla_o_expr'],
                ['tk_par_der']  # tupla vacía
            ],
            
            'tupla_o_expr': [
                ['tk_coma', 'elementos_tupla_tail', 'tk_par_der'],  # tupla
                ['tk_par_der']  # expresión entre paréntesis
            ],
            
            'atom_suffix': [
                ['tk_par_izq', 'args_opt', 'tk_par_der', 'atom_suffix'],
                ['tk_corchete_izq', 'expresion', 'tk_corchete_der', 'atom_suffix'],
                ['tk_punto', 'id', 'atom_suffix'],
                ['ε']
            ],
            
            'numero': [
                ['tk_entero', 'numero_decimal']
            ],
            
            'numero_decimal': [
                ['tk_punto', 'tk_entero'],
                ['ε']
            ],
            
            # Argumentos
            'args_opt': [
                ['args'],
                ['ε']
            ],
            
            'args': [
                ['expresion', 'args_tail']
            ],
            
            'args_tail': [
                ['tk_coma', 'expresion', 'args_tail'],
                ['ε']
            ],
            
            # Listas
            'lista': [
                ['tk_corchete_izq', 'elementos_lista', 'tk_corchete_der']
            ],
            
            'elementos_lista': [
                ['expresion', 'elementos_lista_tail'],
                ['ε']
            ],
            
            'elementos_lista_tail': [
                ['tk_coma', 'expresion', 'elementos_lista_tail'],
                ['ε']
            ],
            
            # Tuplas
            'elementos_tupla_tail': [
                ['expresion', 'elementos_tupla_tail_cont'],
                ['ε']
            ],
            
            'elementos_tupla_tail_cont': [
                ['tk_coma', 'expresion', 'elementos_tupla_tail_cont'],
                ['ε']
            ],
            
            # Diccionarios y Conjuntos
            'diccionario_o_conjunto': [
                ['tk_llave_izq', 'dict_o_set_contenido']
            ],
            
            'dict_o_set_contenido': [
                ['expresion', 'dict_o_set_decision'],
                ['tk_llave_der']  # dict/set vacío
            ],
            
            'dict_o_set_decision': [
                ['tk_dos_puntos', 'expresion', 'elementos_dict_tail', 'tk_llave_der'],  # diccionario
                ['elementos_conjunto_tail', 'tk_llave_der']  # conjunto
            ],
            
            'elementos_dict_tail': [
                ['tk_coma', 'par_dict', 'elementos_dict_tail'],
                ['ε']
            ],
            
            'par_dict': [
                ['expresion', 'tk_dos_puntos', 'expresion']
            ],
            
            'elementos_conjunto_tail': [
                ['tk_coma', 'expresion', 'elementos_conjunto_tail'],
                ['ε']
            ]
        }
    
    # CÁLCULO DE FIRST
    
    def calcular_first(self, verbose=False):
        """Calcula el conjunto FIRST para cada símbolo de la gramática"""
        if verbose:
            print("=" * 60)
            print("CALCULANDO CONJUNTOS FIRST")
            print("=" * 60)
        
        # Inicializar FIRST para todos los no terminales
        for no_terminal in self.gramatica.keys():
            self.first[no_terminal] = set()
        
        # Para terminales, FIRST(terminal) = {terminal}
        terminales = self._obtener_terminales()
        for terminal in terminales:
            self.first[terminal] = {terminal}
        
        # FIRST(ε) = {ε}
        self.first[self.epsilon] = {self.epsilon}
        
        # Iterar hasta que no haya cambios
        cambios = True
        iteracion = 0
        while cambios:
            cambios = False
            iteracion += 1
            if verbose:
                print(f"\nIteración {iteracion}:")
            
            for no_terminal, producciones in self.gramatica.items():
                first_anterior = len(self.first[no_terminal])
                
                for produccion in producciones:
                    self._agregar_first_produccion(no_terminal, produccion)
                
                if len(self.first[no_terminal]) > first_anterior:
                    cambios = True
                    if verbose:
                        print(f"  PRIMEROS({no_terminal}) = {self.first[no_terminal]}")
        
        if verbose:
            print("\n" + "=" * 60)
            print("CONJUNTOS PRIMEROS:")
            print("=" * 60)
            for simbolo in sorted(self.first.keys()):
                if simbolo in self.gramatica:
                    print(f"PRIMEROS({simbolo:20s}) = {self.first[simbolo]}")
        
        return self.first
    
    def _agregar_first_produccion(self, no_terminal, produccion):
        """Agrega elementos a FIRST de un no terminal basado en una producción"""
        if produccion[0] == self.epsilon:
            self.first[no_terminal].add(self.epsilon)
            return
        
        for i, simbolo in enumerate(produccion):
            if simbolo in self.first:
                self.first[no_terminal].update(self.first[simbolo] - {self.epsilon})
                
                if self.epsilon not in self.first[simbolo]:
                    break
                
                if i == len(produccion) - 1:
                    self.first[no_terminal].add(self.epsilon)
            else:
                self.first[no_terminal].add(simbolo)
                break
    
    # ===================================================================
    # CÁLCULO DE FOLLOW
    # ===================================================================
    
    def calcular_follow(self, verbose=False):
        """Calcula el conjunto FOLLOW para cada no terminal"""
        if verbose:
            print("\n" + "=" * 60)
            print("CALCULANDO CONJUNTOS SIGUIENTES")
            print("=" * 60)
        
        for no_terminal in self.gramatica.keys():
            self.follow[no_terminal] = set()
        
        simbolo_inicial = 'programa'
        self.follow[simbolo_inicial].add(self.endmarker)
        
        cambios = True
        iteracion = 0
        while cambios:
            cambios = False
            iteracion += 1
            if verbose:
                print(f"\nIteración {iteracion}:")
            
            for no_terminal, producciones in self.gramatica.items():
                for produccion in producciones:
                    if produccion[0] == self.epsilon:
                        continue
                    
                    for i, simbolo in enumerate(produccion):
                        if simbolo not in self.gramatica:
                            continue
                        
                        follow_anterior = len(self.follow[simbolo])
                        
                        if i < len(produccion) - 1:
                            siguiente = produccion[i + 1]
                            
                            if siguiente in self.first:
                                self.follow[simbolo].update(
                                    self.first[siguiente] - {self.epsilon}
                                )
                            
                            if siguiente in self.first and self.epsilon in self.first[siguiente]:
                                self.follow[simbolo].update(self.follow[no_terminal])
                        else:
                            self.follow[simbolo].update(self.follow[no_terminal])
                        
                        if len(self.follow[simbolo]) > follow_anterior:
                            cambios = True
                            if verbose:
                                print(f"  SIGUIENTES({simbolo}) = {self.follow[simbolo]}")
        
        if verbose:
            print("\n" + "=" * 60)
            print("CONJUNTOS SIGUIENTES INALES:")
            print("=" * 60)
            for simbolo in sorted(self.follow.keys()):
                print(f"SIGUIENTES({simbolo:20s}) = {self.follow[simbolo]}")
        
        return self.follow
    
    # CONSTRUCCION DE TABLA DE PARSING
    
    def construir_tabla_parsing(self, verbose=False):
        """Construye la tabla de análisis sintáctico LL(1)"""
        if verbose:
            print("\n" + "=" * 60)
            print("CONSTRUYENDO TABLA DE PARSING LL(1)")
            print("=" * 60)
        
        conflictos = []
        
        for no_terminal, producciones in self.gramatica.items():
            for idx, produccion in enumerate(producciones):
                first_prod = self._calcular_first_produccion(produccion)
                
                for terminal in first_prod:
                    if terminal == self.epsilon:
                        continue
                    
                    if (no_terminal, terminal) in self.tabla_parsing:
                        conflictos.append({
                            'no_terminal': no_terminal,
                            'terminal': terminal,
                            'produccion1': self.tabla_parsing[(no_terminal, terminal)],
                            'produccion2': produccion
                        })
                    else:
                        self.tabla_parsing[(no_terminal, terminal)] = produccion
                
                if self.epsilon in first_prod:
                    for terminal in self.follow[no_terminal]:
                        if (no_terminal, terminal) in self.tabla_parsing:
                            conflictos.append({
                                'no_terminal': no_terminal,
                                'terminal': terminal,
                                'produccion1': self.tabla_parsing[(no_terminal, terminal)],
                                'produccion2': produccion
                            })
                        else:
                            self.tabla_parsing[(no_terminal, terminal)] = produccion

        print("\n" + "=" * 60)
        print(f"TABLA DE PARSING: {len(self.tabla_parsing)} entradas")
        print("=" * 60)
        print(self.tabla_parsing)
        
        return self.tabla_parsing, conflictos
    
    def _calcular_first_produccion(self, produccion):
        """Calcula FIRST de una producción completa"""
        resultado = set()
        
        if produccion[0] == self.epsilon:
            return {self.epsilon}
        
        for simbolo in produccion:
            if simbolo in self.first:
                resultado.update(self.first[simbolo] - {self.epsilon})
                if self.epsilon not in self.first[simbolo]:
                    break
            else:
                resultado.add(simbolo)
                break
        else:
            resultado.add(self.epsilon)
        
        return resultado
    
    def _obtener_terminales(self):
        """Extrae todos los terminales mencionados en la gramática"""
        terminales = set()
        for producciones in self.gramatica.values():
            for produccion in producciones:
                for simbolo in produccion:
                    if simbolo not in self.gramatica and simbolo != self.epsilon:
                        terminales.add(simbolo)
        return terminales
    
    # ANÁLISIS SINTÁCTICO
    
    def parsear(self, tokens):
        """Analiza sintácticamente una lista de tokens"""
        self.tokens = tokens
        self.pos = 0
        self.token_actual = tokens[0] if tokens else None
        self.errores = []
        
        try:
            self._parsear_no_terminal('programa')
            print("✓ Análisis sintáctico completado exitosamente")
            return True
        except SyntaxError as e:
            print(f"✗ {e}")
            return False
    
    def _parsear_no_terminal(self, no_terminal):
        """Parsea un no terminal usando la tabla de parsing"""
        if no_terminal == self.epsilon:
            return
        
        terminal_actual = self.token_actual.tipo
        
        # Buscar en la tabla de parsing
        if (no_terminal, terminal_actual) in self.tabla_parsing:
            produccion = self.tabla_parsing[(no_terminal, terminal_actual)]
            
            # Aplicar la producción
            for simbolo in produccion:
                if simbolo == self.epsilon:
                    continue
                elif simbolo in self.gramatica:
                    # Es un no terminal
                    self._parsear_no_terminal(simbolo)
                else:
                    # Es un terminal
                    self._match(simbolo)
        else:
            self._error(f"Sintaxis invalida({no_terminal}, {terminal_actual})")
    
    def _match(self, tipo_esperado):
        """Verifica y consume un token del tipo esperado"""
        if self.token_actual.tipo == tipo_esperado:
            self._avanzar()
        else:
            self._error(f"Se esperaba '{tipo_esperado}' pero se encontró '{self.token_actual.tipo}'")
    
    def _avanzar(self):
        """Avanza al siguiente token"""
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.token_actual = self.tokens[self.pos]
    
    def _error(self, mensaje):
        """Registra un error sintáctico"""
        error_msg = f"Error sintáctico en línea {self.token_actual.fila}, columna {self.token_actual.columna}: {mensaje}"
        self.errores.append(error_msg)
        raise SyntaxError(error_msg)


# ===================================================================
# FUNCIÓN PRINCIPAL
# ===================================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python parser_ll1.py <opcion> [archivo.py]")
        print("\nOpciones:")
        print("  --analizar <archivo>  : Analiza sintácticamente un archivo")
        print("  --tablas              : Muestra FIRST, FOLLOW y tabla de parsing")
        print("  --todo <archivo>      : Muestra tablas y analiza el archivo")
        sys.exit(1)
    
    opcion = sys.argv[1]
    
    parser = ParserLL1Completo()
    
    if opcion == "--tablas":
        # Solo mostrar las tablas
        parser.calcular_first(verbose=True)
        parser.calcular_follow(verbose=True)
        parser.construir_tabla_parsing(verbose=True)
        
    elif opcion == "--analizar" and len(sys.argv) == 3:
        # Solo analizar archivo
        archivo = sys.argv[2]
        
        try:
            from analizador_lex import analizador_lexico
            
            with open(archivo, 'r', encoding='utf-8') as f:
                codigo = f.read()
            
            print(f"Analizando archivo: {archivo}")
            print("=" * 60)
            
            print("\n[1] Análisis Léxico...")
            tokens = analizador_lexico(codigo)
            print(f"✓ Se generaron {len(tokens)} tokens")
            
            print("\n[2] Preparando parser LL(1)...")
            parser.calcular_first(verbose=False)
            parser.calcular_follow(verbose=False)
            parser.construir_tabla_parsing(verbose=False)
            print("✓ Tablas FIRST, FOLLOW y Parsing construidas")
            
            print("\n[3] Análisis Sintáctico...")
            resultado = parser.parsear(tokens)
            
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
    
    elif opcion == "--todo" and len(sys.argv) == 3:
        # Mostrar tablas y analizar
        archivo = sys.argv[2]
        
        try:
            from analizador_lex import analizador_lexico
            
            # Mostrar tablas
            parser.calcular_first(verbose=True)
            parser.calcular_follow(verbose=True)
            parser.construir_tabla_parsing(verbose=True)
            
            # Analizar archivo
            with open(archivo, 'r', encoding='utf-8') as f:
                codigo = f.read()
            
            print("\n" + "=" * 60)
            print(f"ANALIZANDO ARCHIVO: {archivo}")
            print("=" * 60)
            
            print("\n[1] Análisis Léxico...")
            tokens = analizador_lexico(codigo)
            print(f"✓ Se generaron {len(tokens)} tokens")
            
            print("\n[2] Análisis Sintáctico...")
            resultado = parser.parsear(tokens)
            
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
    
    else:
        print("✗ Opción no válida")
        print("\nUso correcto:")
        print("  python parser_ll1.py --tablas")
        print("  python parser_ll1.py --analizar archivo.py")
        print("  python parser_ll1.py --todo archivo.py")
        sys.exit(1)