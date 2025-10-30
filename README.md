# Proyecto-Segundo-Corte-Lenguajes-De-Programacion-
Samuel Esteban Leyton Muñoz - Felipe Morales Robelto - William Alfonso Giraldo 

# Expresiones aceptadas
## 1. Operadores Lógicospython# OR (menor precedencia)
x or y
a or b or c

AND
x and y
a and b and c

NOT (precedencia más alta en lógicos)
not x
not (a and b)
## 2. Operadores de Comparaciónpython# Igualdad
x == y
x != y

Relacionales
x < y
x <= y
x > y
x >= y


x is y
x is not y 
## 3. Operadores Aritméticos
x + y
x - y
a + b - c

Multiplicación, división y módulo (mayor precedencia que +/-)
x * y
x / y
x % y
a * b / c % d

Potencia (mayor precedencia)
x ** y
2 ** 8

Unarios (mayor precedencia)
+x
-x
## 4. Precedencia de Operadores (de menor a mayor)
1. or                    Más bajo
2. and
3. not
4. ==, !=, <, <=, >, >=, in, is, is not
5. +, -                  (suma/resta)
6. *, /, %              (multiplicación/división)
7. +x, -x               (unarios)
8. **                   
## 5. Átomos (Valores básicos)python# Literales
42                  # Enteros
"texto"            # Cadenas
True, False        # Booleanos
None               # None

Variables
x
nombre
_privado


self
self.atributo
## 6. Acceso y Llamadas
funcion()
funcion(arg1, arg2)
funcion(a, b, c)

Acceso a atributos con punto
objeto.atributo
obj.metodo()
self.nombre

Acceso encadenado
objeto.atributo.metodo()
persona.direccion.ciudad

Indexación
lista[0]
matriz[i]
dict[key]

Indexación encadenada
lista[0][1]
matriz[i][j][k]

Combinaciones
objeto.metodo()[0]
lista[0].atributo
funcion().metodo()
## 7. Estructuras de Datos
[]
[1, 2, 3]
[x, y, z]

Tuplas
()                  # Tupla vacía
(1,)                # Tupla de un elemento
(1, 2, 3)           # Tupla múltiple
(x, y)

 Diccionarios
{"a": 1, "b": 2}
{key: value}

# Conjuntos
{1, 2, 3}
{x, y, z}

## 8. Expresiones entre Paréntesis
(a * b) / c
((x + y) * z)
## 9. Expresiones Complejas Soportadas
2 + 3 * 4                    # = 14
(2 + 3) * 4                  # = 20
2 ** 3 ** 2                  # = 512 (asociatividad derecha)
10 + 20 / 5 - 3              # = 11

Expresiones lógicas complejas
x > 5 and y < 10
a == b or c != d
not (x > 0 and y > 0)
(x > 5 and y > 10) or z == 0

Acceso encadenado complejo
objeto.metodo()[0].atributo
lista[i].metodo(arg).propiedad
funcion(a, b).resultado[0]

Expresiones en argumentos
funcion(x + y, a * b)
metodo(lista[0], dict[key])
llamada(obj.attr, 10 + 20)


## Expresiones NO Soportadas

[x for x in range(10)]      

## Expresiones lambda
lambda x: x + 1              

## Operadores bit a bit
x & y, x | y, x ^ y         

## Slicing
lista[1:5]                

## Asignación múltiple
x, y = 1, 2              

## Operador ternario
x if condicion else y     

## Walrus operator
(x := 10)                

## f-strings
f"Valor: {x}"            

## Desempaquetado
*args, **kwargs           

## @ (decoradores o matmul)
@decorator                  