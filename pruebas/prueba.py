def factorial(n: int):
    """Factorial recursivo para n >= 0."""
    if n < 0:
        raise ValueError("n debe ser no negativo")
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# Ejemplo
if __name__ == "__main__":
    for i in range(6):
        print(factorial(i))  