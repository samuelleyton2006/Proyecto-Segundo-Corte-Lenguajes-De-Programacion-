

class ParserLL1Completo:
    def __init__(self):
        # Gramática en formato: 'no_terminal' -> [['produccion1'], ['produccion2'], ...]
        self.gramatica = self._definir_gramatica()
        
        # Conjuntos calculados
        self.first = {}
        self.follow = {}
        self.tabla_parsing = {}
        
        # Símbolos especiales
        self.epsilon = 'ε'
        self.endmarker = 'ENDMARKER'
        
    def _definir_gramatica(self):
        """Define la gramática LL(1) en formato diccionario"""
        return {
            # Símbolo inicial
            'programa': [
                ['NEWLINE', 'programa'],
                ['sentencias', 'ENDMARKER']
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
                ['id', 'param_default'],
                ['self', 'param_default']
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
    
    def calcular_first(self):
        """
        Calcula el conjunto FIRST para cada símbolo de la gramática
        FIRST(X) = conjunto de terminales que pueden aparecer al inicio de X
        """
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
            print(f"\nIteración {iteracion}:")
            
            for no_terminal, producciones in self.gramatica.items():
                first_anterior = len(self.first[no_terminal])
                
                for produccion in producciones:
                    # Para cada producción A → X1 X2 ... Xn
                    self._agregar_first_produccion(no_terminal, produccion)
                
                if len(self.first[no_terminal]) > first_anterior:
                    cambios = True
                    print(f"  FIRST({no_terminal}) = {self.first[no_terminal]}")
        
        print("\n" + "=" * 60)
        print("CONJUNTOS FIRST FINALES:")
        print("=" * 60)
        for simbolo in sorted(self.first.keys()):
            if simbolo in self.gramatica:  # Solo no terminales
                print(f"FIRST({simbolo:20s}) = {self.first[simbolo]}")
        
        return self.first
    
    def _agregar_first_produccion(self, no_terminal, produccion):
        """Agrega elementos a FIRST de un no terminal basado en una producción"""
        if produccion[0] == self.epsilon:
            self.first[no_terminal].add(self.epsilon)
            return
        
        # Para A → X1 X2 ... Xn
        for i, simbolo in enumerate(produccion):
            if simbolo in self.first:
                # Agregar FIRST(Xi) - {ε} a FIRST(A)
                self.first[no_terminal].update(self.first[simbolo] - {self.epsilon})
                
                # Si ε no está en FIRST(Xi), terminar
                if self.epsilon not in self.first[simbolo]:
                    break
                
                # Si llegamos al final y todos tenían ε, agregar ε
                if i == len(produccion) - 1:
                    self.first[no_terminal].add(self.epsilon)
            else:
                # Símbolo no reconocido, asumir terminal
                self.first[no_terminal].add(simbolo)
                break
    
    def calcular_follow(self):
        """
        Calcula el conjunto FOLLOW para cada no terminal
        FOLLOW(A) = conjunto de terminales que pueden aparecer después de A
        """
        print("\n" + "=" * 60)
        print("CALCULANDO CONJUNTOS FOLLOW")
        print("=" * 60)
        
        # Inicializar FOLLOW
        for no_terminal in self.gramatica.keys():
            self.follow[no_terminal] = set()
        
        # FOLLOW del símbolo inicial contiene $
        simbolo_inicial = 'programa'
        self.follow[simbolo_inicial].add(self.endmarker)
        
        # Iterar hasta que no haya cambios
        cambios = True
        iteracion = 0
        while cambios:
            cambios = False
            iteracion += 1
            print(f"\nIteración {iteracion}:")
            
            for no_terminal, producciones in self.gramatica.items():
                for produccion in producciones:
                    if produccion[0] == self.epsilon:
                        continue
                    
                    # Para cada símbolo en la producción
                    for i, simbolo in enumerate(produccion):
                        if simbolo not in self.gramatica:
                            continue  # Es terminal
                        
                        follow_anterior = len(self.follow[simbolo])
                        
                        # Si hay símbolos después
                        if i < len(produccion) - 1:
                            siguiente = produccion[i + 1]
                            
                            # Agregar FIRST(siguiente) - {ε} a FOLLOW(simbolo)
                            if siguiente in self.first:
                                self.follow[simbolo].update(
                                    self.first[siguiente] - {self.epsilon}
                                )
                            
                            # Si ε está en FIRST(siguiente), agregar FOLLOW(no_terminal)
                            if siguiente in self.first and self.epsilon in self.first[siguiente]:
                                self.follow[simbolo].update(self.follow[no_terminal])
                        else:
                            # Es el último símbolo, agregar FOLLOW(no_terminal)
                            self.follow[simbolo].update(self.follow[no_terminal])
                        
                        if len(self.follow[simbolo]) > follow_anterior:
                            cambios = True
                            print(f"  FOLLOW({simbolo}) = {self.follow[simbolo]}")
        
        print("\n" + "=" * 60)
        print("CONJUNTOS FOLLOW FINALES:")
        print("=" * 60)
        for simbolo in sorted(self.follow.keys()):
            print(f"FOLLOW({simbolo:20s}) = {self.follow[simbolo]}")
        
        return self.follow
    
    def construir_tabla_parsing(self):
        """
        Construye la tabla de análisis sintáctico LL(1)
        Tabla[A, a] indica qué producción usar cuando:
        - A es el no terminal en el tope de la pila
        - a es el terminal actual en la entrada
        """
        print("\n" + "=" * 60)
        print("CONSTRUYENDO TABLA DE PARSING LL(1)")
        print("=" * 60)
        
        conflictos = []
        
        for no_terminal, producciones in self.gramatica.items():
            for idx, produccion in enumerate(producciones):
                # Para cada terminal en FIRST(produccion)
                first_prod = self._calcular_first_produccion(produccion)
                
                for terminal in first_prod:
                    if terminal == self.epsilon:
                        continue
                    
                    # Tabla[A, terminal] = producción
                    if (no_terminal, terminal) in self.tabla_parsing:
                        # ¡CONFLICTO LL(1)!
                        conflictos.append({
                            'no_terminal': no_terminal,
                            'terminal': terminal,
                            'produccion1': self.tabla_parsing[(no_terminal, terminal)],
                            'produccion2': produccion
                        })
                    else:
                        self.tabla_parsing[(no_terminal, terminal)] = produccion
                
                # Si ε está en FIRST(produccion)
                if self.epsilon in first_prod:
                    # Para cada terminal en FOLLOW(A)
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
        
        if conflictos:
            print("\n⚠️  CONFLICTOS LL(1) DETECTADOS:")
            for i, conflicto in enumerate(conflictos, 1):
                print(f"\n  Conflicto {i}:")
                print(f"    No terminal: {conflicto['no_terminal']}")
                print(f"    Terminal: {conflicto['terminal']}")
                print(f"    Producción 1: {conflicto['produccion1']}")
                print(f"    Producción 2: {conflicto['produccion2']}")
            print("\n  ❌ LA GRAMÁTICA NO ES LL(1)")
        else:
            print("\n✓ No se detectaron conflictos - La gramática es LL(1)")
        
        # Mostrar tabla (primeras entradas)
        print("\n" + "=" * 60)
        print("TABLA DE PARSING (muestra):")
        print("=" * 60)
        count = 0
        for (nt, term), prod in sorted(self.tabla_parsing.items()):
            if count < 20:  # Mostrar solo primeras 20 entradas
                print(f"  Tabla[{nt:15s}, {term:15s}] = {prod}")
                count += 1
        print(f"  ... ({len(self.tabla_parsing)} entradas totales)")
        
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
    
    def verificar_ll1(self):
        """Verifica si la gramática es LL(1)"""
        print("\n" + "=" * 60)
        print("VERIFICACIÓN LL(1)")
        print("=" * 60)
        
        es_ll1 = True
        
        # Verificar que no haya recursión izquierda
        print("\n1. Verificando recursión izquierda...")
        tiene_rec_izq = False
        for no_terminal, producciones in self.gramatica.items():
            for produccion in producciones:
                if produccion[0] == no_terminal:
                    print(f"   ❌ {no_terminal} → {' '.join(produccion)} (recursión izquierda)")
                    tiene_rec_izq = True
                    es_ll1 = False
        
        if not tiene_rec_izq:
            print("   ✓ No hay recursión izquierda")
        
        # Verificar ambigüedad con FIRST/FOLLOW
        print("\n2. Verificando condición LL(1) con FIRST/FOLLOW...")
        for no_terminal, producciones in self.gramatica.items():
            for i, prod1 in enumerate(producciones):
                for prod2 in producciones[i+1:]:
                    first1 = self._calcular_first_produccion(prod1)
                    first2 = self._calcular_first_produccion(prod2)
                    
                    interseccion = first1 & first2
                    if interseccion:
                        print(f"   ❌ {no_terminal}: FIRST({prod1}) ∩ FIRST({prod2}) = {interseccion}")
                        es_ll1 = False
        
        print("\n" + "=" * 60)
        if es_ll1:
            print("RESULTADO: ✓ La gramática ES LL(1)")
        else:
            print("RESULTADO: ❌ La gramática NO es LL(1)")
        print("=" * 60)
        
        return es_ll1


# ===================================================================
# FUNCIÓN PRINCIPAL
# ===================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("ANALIZADOR LL(1) COMPLETO")
    print("Parser con cálculo de FIRST, FOLLOW y Tabla de Parsing")
    print("=" * 60)
    
    parser = ParserLL1Completo()
    
    # Paso 1: Calcular FIRST
    parser.calcular_first()
    
    # Paso 2: Calcular FOLLOW
    parser.calcular_follow()
    
    # Paso 3: Construir tabla de parsing
    tabla, conflictos = parser.construir_tabla_parsing()
    
    # Paso 4: Verificar si es LL(1)
    es_ll1 = parser.verificar_ll1()
    
    print("\n" + "=" * 60)
    print("ANÁLISIS COMPLETADO")
    print("=" * 60)
    print(f"No terminales: {len(parser.gramatica)}")
    print(f"Terminales únicos: {len(parser._obtener_terminales())}")
    print(f"Entradas en tabla: {len(tabla)}")
    print(f"Conflictos detectados: {len(conflictos)}")