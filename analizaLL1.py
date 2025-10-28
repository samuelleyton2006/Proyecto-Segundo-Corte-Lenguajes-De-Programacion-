# -----------------------------------------------
# ANALIZADOR LL(1) - Cálculo de FIRST, FOLLOW y Tabla de Predicción
# -----------------------------------------------

from collections import defaultdict

# -----------------------------------------------
# Funciones principales
# -----------------------------------------------

def parse_grammar(file_path):
    grammar = defaultdict(list)
    non_terminals = set()
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                head, prods = line.split(":", 1)
                head = head.strip()
                non_terminals.add(head)
                for prod in prods.split("|"):
                    grammar[head].append(prod.strip().split())
    return grammar, non_terminals


# -----------------------------------------------
# FIRST
# -----------------------------------------------

def compute_first(symbol, grammar, FIRST, non_terminals):
    # Si ya fue calculado
    if symbol in FIRST and FIRST[symbol]:
        return FIRST[symbol]

    first = set()

    # Si es terminal
    if symbol not in non_terminals:
        first.add(symbol)
        FIRST[symbol] = first
        return first

    # Si es no terminal
    for production in grammar[symbol]:
        for sym in production:
            sym_first = compute_first(sym, grammar, FIRST, non_terminals)
            first |= (sym_first - {'ε'})
            if 'ε' not in sym_first:
                break
        else:
            first.add('ε')

    FIRST[symbol] = first
    return first


# -----------------------------------------------
# FOLLOW (versión corregida)
# -----------------------------------------------

def compute_follow(grammar, FIRST, non_terminals, start_symbol):
    FOLLOW = {nt: set() for nt in non_terminals}
    FOLLOW[start_symbol].add('$')  # Fin de entrada

    changed = True
    while changed:
        changed = False
        for left, productions in grammar.items():
            for prod in productions:
                for i, sym in enumerate(prod):
                    if sym in non_terminals:
                        follow_before = len(FOLLOW[sym])
                        next_symbols = prod[i + 1:]

                        if next_symbols:
                            first_next = set()
                            for s in next_symbols:
                                # Manejo seguro: si no está en FIRST, se considera terminal
                                if s in FIRST:
                                    first_next |= (FIRST[s] - {'ε'})
                                else:
                                    first_next.add(s)

                                if s not in FIRST or 'ε' not in FIRST[s]:
                                    break
                            else:
                                first_next.add('ε')

                            FOLLOW[sym] |= (first_next - {'ε'})
                            if 'ε' in first_next:
                                FOLLOW[sym] |= FOLLOW[left]
                        else:
                            FOLLOW[sym] |= FOLLOW[left]

                        if len(FOLLOW[sym]) > follow_before:
                            changed = True
    return FOLLOW


# -----------------------------------------------
# TABLA LL(1)
# -----------------------------------------------

def build_ll1_table(grammar, FIRST, FOLLOW):
    table = defaultdict(dict)
    for nt, productions in grammar.items():
        for prod in productions:
            first_set = set()
            for sym in prod:
                if sym in FIRST:
                    first_set |= (FIRST[sym] - {'ε'})
                else:
                    first_set.add(sym)
                if 'ε' not in FIRST.get(sym, set()):
                    break
            else:
                first_set.add('ε')

            for terminal in first_set - {'ε'}:
                if terminal in table[nt]:
                    print(f"⚠️ Solapamiento en {nt} con '{terminal}' → {table[nt][terminal]} y {prod}")
                table[nt][terminal] = prod

            if 'ε' in first_set:
                for terminal in FOLLOW[nt]:
                    if terminal in table[nt]:
                        print(f"⚠️ Solapamiento en {nt} con '{terminal}' → {table[nt][terminal]} y {prod}")
                    table[nt][terminal] = prod
    return table


# -----------------------------------------------
# IMPRESIÓN
# -----------------------------------------------

def print_sets(FIRST, FOLLOW):
    print("\n===== CONJUNTOS FIRST =====")
    for nt, s in FIRST.items():
        print(f"{nt}: {s}")

    print("\n===== CONJUNTOS FOLLOW =====")
    for nt, s in FOLLOW.items():
        print(f"{nt}: {s}")


def print_ll1_table(table):
    print("\n===== TABLA LL(1) =====")
    for nt, row in table.items():
        print(f"\n{nt}:")
        for terminal, prod in row.items():
            print(f"   {terminal} → {' '.join(prod)}")


# -----------------------------------------------
# MAIN
# -----------------------------------------------

def main():
    grammar_file = "GRAMATICA_SELECCIONADA.txt"  # Asegúrate de tenerla en el mismo directorio
    grammar, non_terminals = parse_grammar(grammar_file)

    FIRST = {nt: set() for nt in non_terminals}
    for nt in non_terminals:
        compute_first(nt, grammar, FIRST, non_terminals)

    start_symbol = next(iter(grammar))  # primer símbolo como inicio
    FOLLOW = compute_follow(grammar, FIRST, non_terminals, start_symbol)

    print_sets(FIRST, FOLLOW)

    table = build_ll1_table(grammar, FIRST, FOLLOW)
    print_ll1_table(table)


if __name__ == "__main__":
    main()