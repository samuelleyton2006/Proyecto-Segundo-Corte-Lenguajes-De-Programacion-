import re
from collections import defaultdict

# --- PARTE 1: Leer gramática desde archivo ---
def parse_grammar(path):
    grammar = defaultdict(list)
    current_nonterminal = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):  # ignorar comentarios y líneas vacías
                continue

            # detectar nueva regla
            if ":" in line:
                current_nonterminal = line.split(":")[0].strip()
                rest = line.split(":", 1)[1].strip()
                if rest:
                    production = rest.replace("|", "").strip()
                    grammar[current_nonterminal].append(production.split())
            elif line.startswith("|"):
                if current_nonterminal is None:
                    continue
                production = line.replace("|", "").strip()
                if production == "ε":
                    grammar[current_nonterminal].append(["ε"])
                elif production:
                    grammar[current_nonterminal].append(production.split())
                else:
                    grammar[current_nonterminal].append(["ε"])
    return grammar

# --- PARTE 2: Calcular FIRST ---
def compute_first(symbol, grammar, FIRST, non_terminals):
    if symbol not in non_terminals:
        return {symbol}
    for production in grammar[symbol]:
        for sym in production:
            first_set = compute_first(sym, grammar, FIRST, non_terminals)
            FIRST[symbol].update(first_set - {"ε"})
            if "ε" not in first_set:
                break
        else:
            FIRST[symbol].add("ε")
    return FIRST[symbol]

# --- PARTE 3: Calcular FOLLOW ---
def compute_follow(grammar, FIRST, non_terminals, start_symbol):
    FOLLOW = defaultdict(set)
    FOLLOW[start_symbol].add("$")
    changed = True
    while changed:
        changed = False
        for A in grammar:
            for production in grammar[A]:
                for i, B in enumerate(production):
                    if B in non_terminals:
                        beta = production[i + 1:]
                        if beta:
                            first_beta = set()
                            for sym in beta:
                                first_beta |= (FIRST[sym] - {"ε"})
                                if "ε" not in FIRST[sym]:
                                    break
                            else:
                                first_beta.add("ε")
                            old = len(FOLLOW[B])
                            FOLLOW[B].update(first_beta - {"ε"})
                            if "ε" in first_beta:
                                FOLLOW[B].update(FOLLOW[A])
                            if len(FOLLOW[B]) != old:
                                changed = True
                        else:
                            old = len(FOLLOW[B])
                            FOLLOW[B].update(FOLLOW[A])
                            if len(FOLLOW[B]) != old:
                                changed = True
    return FOLLOW

# --- PARTE 4: Verificar conflictos LL(1) ---
def check_ll1(grammar, FIRST, FOLLOW):
    print("\n=== VERIFICACIÓN LL(1) ===")
    for A, prods in grammar.items():
        seen = []
        for i, alpha in enumerate(prods):
            first_alpha = set()
            for sym in alpha:
                first_alpha |= (FIRST[sym] - {"ε"})
                if "ε" not in FIRST[sym]:
                    break
            else:
                first_alpha.add("ε")
            for prev in seen:
                if not first_alpha.isdisjoint(prev):
                    print(f"[⚠️ Solapamiento] {A} → {' '.join(alpha)} tiene intersección con otra producción FIRST.")
            seen.append(first_alpha)
            if "ε" in first_alpha:
                if not FIRST[A].isdisjoint(FOLLOW[A]):
                    print(f"[⚠️ Epsilon conflicto] {A}: FIRST y FOLLOW se solapan.")
    print("Verificación completa.\n")

# --- PARTE 5: Ejecutar todo ---
def main():
    path = "GRAMATICA_SELECCIONADA.txt"  # cambia por el nombre de tu archivo
    grammar = parse_grammar(path)
    non_terminals = list(grammar.keys())

    FIRST = defaultdict(set)
    for nt in non_terminals:
        compute_first(nt, grammar, FIRST, non_terminals)

    FOLLOW = compute_follow(grammar, FIRST, non_terminals, start_symbol=non_terminals[0])

    print("\n=== CONJUNTOS FIRST ===")
    for nt in non_terminals:
        print(f"FIRST({nt}) = {FIRST[nt]}")

    print("\n=== CONJUNTOS FOLLOW ===")
    for nt in non_terminals:
        print(f"FOLLOW({nt}) = {FOLLOW[nt]}")

    check_ll1(grammar, FIRST, FOLLOW)

if __name__ == "__main__":
    main()