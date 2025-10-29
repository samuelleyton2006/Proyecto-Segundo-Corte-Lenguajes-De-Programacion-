import sys
from collections import defaultdict
from analizador_lex import analizador_lexico

# ============================================================
#  1️⃣ Cargar gramática
# ============================================================
def leer_gramatica(nombre_archivo):
    gramatica = defaultdict(list)
    simbolo_inicial = None
    with open(nombre_archivo, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            if ":" in linea and not linea.startswith("|"):
                izquierda = linea.replace(":", "").strip()
                if simbolo_inicial is None:
                    simbolo_inicial = izquierda
                actual = izquierda
            elif linea.startswith("|"):
                derecha = linea[1:].strip()
                if derecha == "ε":
                    gramatica[actual].append(["ε"])
                else:
                    gramatica[actual].append(derecha.split())
    return gramatica, simbolo_inicial


# ============================================================
#  2️⃣ Calcular PRIMEROS
# ============================================================
def calcular_primeros(gramatica):
    primeros = defaultdict(set)
    for nt in gramatica:
        for prod in gramatica[nt]:
            for simbolo in prod:
                if simbolo not in gramatica and simbolo != "ε":
                    primeros[simbolo].add(simbolo)
    cambiado = True
    while cambiado:
        cambiado = False
        for nt in gramatica:
            for prod in gramatica[nt]:
                puede_vacio = True
                for simbolo in prod:
                    if simbolo not in gramatica:
                        antes = len(primeros[nt])
                        primeros[nt].add(simbolo)
                        if len(primeros[nt]) > antes:
                            cambiado = True
                        puede_vacio = False
                        break
                    else:
                        antes = len(primeros[nt])
                        primeros[nt] |= (primeros[simbolo] - {"ε"})
                        if len(primeros[nt]) > antes:
                            cambiado = True
                        if "ε" not in primeros[simbolo]:
                            puede_vacio = False
                            break
                if puede_vacio and "ε" not in primeros[nt]:
                    primeros[nt].add("ε")
                    cambiado = True
    return primeros


# ============================================================
#  3️⃣ Calcular SIGUIENTES
# ============================================================
def calcular_siguientes(gramatica, inicial, primeros):
    siguientes = defaultdict(set)
    siguientes[inicial].add("$")
    cambiado = True
    while cambiado:
        cambiado = False
        for nt in gramatica:
            for prod in gramatica[nt]:
                for i, simbolo in enumerate(prod):
                    if simbolo in gramatica:
                        beta = prod[i + 1:]
                        if beta:
                            primeros_beta = set()
                            vacio = True
                            for b in beta:
                                primeros_beta |= (primeros[b] if b in primeros else {b})
                                if "ε" not in primeros[b]:
                                    vacio = False
                                    break
                            antes = len(siguientes[simbolo])
                            siguientes[simbolo] |= (primeros_beta - {"ε"})
                            if len(siguientes[simbolo]) > antes:
                                cambiado = True
                            if vacio:
                                antes = len(siguientes[simbolo])
                                siguientes[simbolo] |= siguientes[nt]
                                if len(siguientes[simbolo]) > antes:
                                    cambiado = True
                        else:
                            antes = len(siguientes[simbolo])
                            siguientes[simbolo] |= siguientes[nt]
                            if len(siguientes[simbolo]) > antes:
                                cambiado = True
    return siguientes


# ============================================================
#  4️⃣ Crear tabla predictiva LL(1)
# ============================================================
def construir_tabla_LL1(gramatica, primeros, siguientes):
    tabla = {}
    for nt in gramatica:
        for prod in gramatica[nt]:
            primeros_prod = set()
            vacio = True
            for s in prod:
                if s in primeros:
                    primeros_prod |= (primeros[s] - {"ε"})
                    if "ε" not in primeros[s]:
                        vacio = False
                        break
                else:
                    primeros_prod.add(s)
                    vacio = False
                    break
            if vacio:
                primeros_prod |= siguientes[nt]
            for t in primeros_prod:
                tabla[(nt, t)] = prod
    return tabla


# ============================================================
#  5️⃣ PARSER LL(1)
# ============================================================
class Token:
    def __init__(self, tipo, valor, fila, columna):
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.columna = columna

    def __repr__(self):
        return f"<{self.tipo}, {self.valor}, {self.fila}, {self.columna}>"


class ParserLL1:
    def __init__(self, tokens, tabla, simbolo_inicial):
        self.tokens = tokens + [Token("ENDMARKER", "$", 0, 0)]
        self.tabla = tabla
        self.pila = ["$", simbolo_inicial]
        self.i = 0

    def token_actual(self):
        return self.tokens[self.i].tipo

    def avanzar(self):
        if self.i < len(self.tokens) - 1:
            self.i += 1

    def parsear(self):
        print("\n🚀 Iniciando análisis sintáctico...\n")
        while self.pila:
            cima = self.pila.pop()
            actual = self.token_actual()

            if cima == "ε":
                continue

            if cima == "$":
                if actual == "ENDMARKER":
                    print("✅ Análisis completado correctamente.")
                    return True
                else:
                    print(f"❌ Se esperaba fin de entrada, pero se encontró {actual}")
                    return False

            if cima not in {nt for nt in gramatica.keys()}:
                if cima == actual:
                    print(f"✔️ Coincidencia: {cima}")
                    self.avanzar()
                else:
                    print(f"❌ Error sintáctico: se esperaba {cima}, se encontró {actual}")
                    return False
            else:
                clave = (cima, actual)
                if clave in self.tabla:
                    prod = self.tabla[clave]
                    print(f"➡️ {cima} → {' '.join(prod)}")
                    for s in reversed(prod):
                        self.pila.append(s)
                else:
                    print(f"❌ No hay regla para ({cima}, {actual})")
                    return False
        return True


# ============================================================
#  6️⃣ MAIN: Cargar gramática, calcular conjuntos y analizar
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Uso correcto: python parserr.py archivo.py")
        sys.exit(1)

    archivo_py = sys.argv[1]
    archivo_gramatica = "gramarr.txt"

    # Cargar gramática
    gramatica, inicial = leer_gramatica(archivo_gramatica)
    print(f"📘 Gramática cargada desde {archivo_gramatica}. Símbolo inicial: {inicial}")

    # Construir conjuntos y tabla LL(1)
    primeros = calcular_primeros(gramatica)
    siguientes = calcular_siguientes(gramatica, inicial, primeros)
    tabla = construir_tabla_LL1(gramatica, primeros, siguientes)
    print("\n✅ Tabla LL(1) generada automáticamente.\n")

    # Leer archivo .py pasado como argumento
    try:
        with open(archivo_py, "r", encoding="utf-8") as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo: {archivo_py}")
        sys.exit(1)

    print(f"\n🚀 Analizando archivo: {archivo_py}\n")

    # Analizar con el lexer
    tokens = analizador_lexico(codigo)
    print(tokens)
    print(f"🔹 Total de tokens generados: {len(tokens)}\n")

    # Iniciar parser LL(1)
    parser = ParserLL1(tokens, tabla, inicial)
    parser.parsear()