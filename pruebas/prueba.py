import math  # Importamos la librería para usar π (pi)

class Circulo:
    # Constructor: recibe el radio como parámetro
    def __init__(self, radio):
        self.radio = radio

    # Método para calcular el área del círculo
    def calcular_area(self):
        area = math.pi * (self.radio ** 2)
        return area

# --- Programa principal ---
# Pedir al usuario el radio
r = float(input("Ingrese el radio del círculo: "))

# Crear un objeto de la clase Circulo
mi_circulo = Circulo(r)

# Calcular y mostrar el área
print("El área del círculo con radio ")
