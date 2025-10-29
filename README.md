# Proyecto-Segundo-Corte-Lenguajes-De-Programacion-
Samuel Esteban Leyton Muñoz - Felipe Morales Robelto - William Alfonso Giraldo 



## 1. Sentencias Simples

Asignaciones: x = 5, x += 10, x -= 2, x *= 3, x /= 2, x %= 5
Asignación a índices: lista[0] = 10
Llamadas a funciones: funcion(), funcion(arg1, arg2)
Acceso a atributos: objeto.atributo, obj.metodo()
Sentencias de control: break, continue, pass
Return: return, return valor
Delete: del variable
Import: import modulo, import modulo as alias, from modulo import item, from modulo import item as alias
Print: print(), print(arg1, arg2)

## 2. Sentencias Compuestas
If-Elif-Else
While
For
Definicion de Funciones
Definicion de Clases
Try-Except-Finally
## 3. Expresions
Operadores Lógicos
and, or, not
Operadores de Comparación
==, !=, <, <=, >, >=, in, is, is not

## Operadores Aritméticos

Suma y resta: +, -
Multiplicación, división, módulo: *, /, %
Potencia: **
Unarios: +x, -x
## 4. Estructuras de Datos
Listas
Tuplas
Diccionarios
Conjuntos
## 5. Literales

Números enteros: 42, 0, -10
Números decimales: 3.14, 0.5
Cadenas: "texto", 'texto'
Booleanos: True, False
None: None
## 6. Identificadores y Palabras Reservadas

Variables: x, nombre, _privado
self: self.atributo, self.metodo()

## 7. Características Avanzadas
Acceso encadenado

objeto.atributo.metodo().otro_atributo
lista[0][1][2]
funcion()(otra_funcion())

Parámetros con Anotaciones de Tipo
Expresiones complejas
## 8. Bloques con Indentación
La gramática maneja correctamente la indentación de Python con tokens especiales:

TAB: inicio de indentación
TABend: fin de indentación
NEWLINE: nueva línea

# Limitaciones (No incluye):
❌ Comprensiones de listas/diccionarios: [x for x in lista]
❌ Decoradores: @decorador
❌ Lambda functions: lambda x: x + 1
❌ Argumentos *args y **kwargs
❌ Context managers: with ... as ...:
❌ Assertions: assert condicion
❌ Global/Nonlocal: global x, nonlocal y
❌ Yield: yield valor
❌ Async/Await
❌ Type hints complejos (Union, etc.)
❌ F-strings: f"texto {variable}"
❌ Slicing: lista[1:3], lista[::2]
❌ Operadores bit a bit: &, |, ^, ~, <<, >>