```bash
file: [statements] ENDMARKER  # Un archivo consta de statements y un fin de archivo (ENDMARKER)

statements: statement statements_refactor     # statements es un conjunto de uno o mas statement

statements_refactor:
    | statement statements_refactor
    | ε

statement:                 # Un statement puede ser un statement compuesto o uno simple
    | compound_stmt 
    | simple_stmts 

single_compound_stmt:        # Un statement compuesto solo, consta de un statement compuesto
    | compound_stmt 


statement_newline:                    # Un statement con nueva linea es un statement compuesto solo seguido 
                                      # de un salto de linea linea o un statement simple o una nueva linea o un
    | single_compound_stmt NEWLINE    # fin de marcador
    | simple_stmts
    | NEWLINE 
    | ENDMARKER 


simple_stmts:                          #
    | simple_stmt_list NEWLINE
    | simple_stmt_list ';' NEWLINE  
    
     
simple_stmt_list:
    | simple_stmt
    | simple_stmt ';' simple_stmt_list

simple_stmt:
    | assignment
    | return_stmt
    | import_stmt
    | raise_stmt
    | pass_stmt
    | del_stmt
    | assert_stmt
    | break_stmt
    | continue_stmt
    | global_stmt
    | nonlocal_stmt

compound_stmt:
    | function_def
    | if_stmt
    | class_def
    | for_stmt
    | try_stmt
    | while_stmt
    | match_stmt

#---
assignment:
    | annotated_name_assignment
    | annotated_complex_assignment
    | chained_assignment
    | augmented_assignment

annotated_name_assignment:
    | NAME ':' expression assignment_refactor

annotated_complex_assignment:
    | '(' single_target ')' ':' expression assignment_refactor
    | single_subscript_attribute_target ':' expression assignment_refactor

assignment_refactor:
    | '=' annotated_rhs
    | ε

chained_assignment:
    | assignment_chain annotated_rhs type_comment

type_comment:
    | TYPE_COMMENT
    | ε

assignment_chain:
    | targets '='
    | targets '=' assignment_chain

augmented_assignment:
    | single_target augassign annotated_rhs


annotated_rhs: expression

augassign: # Operador de asignacion aumentada
    | '+=' 
    | '-=' 
    | '*=' 
    | '@=' 
    | '/=' 
    | '%=' 
    | '&=' 
    | '|=' 
    | '^=' 
    | '<<=' 
    | '>>=' 
    | '**=' 
    | '//=' 


################ palabras reservadas a statements

return_stmt:
    | 'return' return_stmt_expression

return_stmt_expression:
    | expression
    | ε
raise_stmt:
    | 'raise' expression from_expression  # Generar un error con un from
    | 'raise'  # Re lanzar la excepción activa dentro de un bloque except

from_expression:
    | 'from' expression
    | ε

pass_stmt:
    | 'pass' # Permite no generar errores en los condicionales usando 'pass'

break_stmt:
    | 'break'  # Rompe el statement

continue_stmt:
    | 'continue'  # Continua 


#----------------- Creacion de variables especiales

global_stmt:
    | 'global' global_name_list

global_name_list:
    | NAME global_name_list_tail

global_name_list_tail:
    | ',' NAME global_name_list_tail
    | ε

nonlocal_stmt: 'nonlocal' nonlocal_name_list

nonlocal_name_list:
    | NAME nonlocal_name_list_tail

nonlocal_name_list_tail
    | ',' NAME global_name_list_tail
    | ε


del_stmt:
    | 'del' del_targets del_stmt_terminator

del_stmt_terminator:
    | ';'
    | NEWLINE

assert_stmt: 'assert' expression assert_stmt_expression

assert_stmt_expression:
    | ',' expression
    | ε
#################### Import Statements
import_stmt:
    | import_name
    | import_from

import_name: 'import' dotted_as_names  # Importacion con comas (,) y paquetes (.) con AS de la regla dotted_as_name


import_from:
    | 'from' dots dotted_name 'import' import_from_targets
    | 'from' dots_only 'import' import_from_targets

dots:
    | dot dots_tail

dots_tail:
    | dot dots_tail
    | ε

dots_only:
    | dot dots_tail   

dot:
    | '.'
    | '...'


import_from_targets:
    | '(' import_from_as_names_opt_trailing_comma ')' 
    | import_from_as_names_no_trailing_comma
    | '*'


import_from_as_names_opt_trailing_comma:
    | import_from_as_names
    | import_from_as_names ','

import_from_as_names_no_trailing_comma:
    | import_from_as_name import_from_as_names_tail

import_from_as_names:
    | import_from_as_name import_from_as_names_tail

import_from_as_names_tail:
    | ',' import_from_as_name import_from_as_names_tail
    | ε


import_from_as_name:
    | NAME import_from_as_name_tail

import_from_as_name_tail:
    | 'as' NAME
    | ε

dotted_as_names:
    | dotted_as_name dotted_as_names_tail

dotted_as_names_tail:
    | ',' dotted_as_name dotted_as_names_tail
    | ε

dotted_as_name:
    | dotted_name dotted_as_name_tail

dotted_as_name_tail:
    | 'as' NAME
    | ε

dotted_name:
    | NAME dotted_name_tail

dotted_name_tail:
    | '.' NAME dotted_name_tail
    | ε


##### Statemet compuesto


block: # Se usa para identacion de bloques, 
    | NEWLINE INDENT statements DEDENT 
    | simple_stmts
####### CLASES

class_def:
    | class_def_raw

class_def_raw:
    | 'class' NAME class_def_raw_parentesis ':' block  # Definicion formal de clase ( class NAME)

class_def_raw_parentesis:
    | '(' class_def_rauw_argument ')'
    | ε

class_def_raw_argument
    | arguments
    | ε


#####  FUNCIONES

function_def:
    | function_def_raw 

function_def_raw: # definicion de funciones normales def () y asincronicas ->
    | 'def' NAME '(' [params] ')' ['->' expression ] ':' [func_type_comment] block 
    | 'async' 'def' NAME '(' [params] ')' ['->' expression ] ':' [func_type_comment] block 


### PARAMETROS DE FUNCIONES

params:
    | [param_list]                # lista opcional de parámetros

param_list:
    | param (',' param)* [',']    # uno o mas parámetros separados por comas, coma final opcional

param:
    | NAME [':' expression] ['=' expression]   # name [: annotation] [= default]

annotation: ':' expression
default: '=' expression 


#### if statement

if_stmt:
    | 'if' named_expression ':' block elif_stmt  
    | 'if' named_expression ':' block [else_block] 
elif_stmt:
    | 'elif' named_expression ':' block elif_stmt 
    | 'elif' named_expression ':' block [else_block] 
else_block:
    | 'else' ':' block 


#### WHILE STATEMENT
while_stmt:
    | 'while' named_expression ':' block [else_block] 



# For statement
for_stmt:
    | 'for' targets 'in' ~ expression ':' [TYPE_COMMENT] block [else_block]
    | 'async' 'for' targets 'in' ~ expression ':' [TYPE_COMMENT] block [else_block]




# Try statement

try_stmt:
    | 'try' ':' block finally_block 
    | 'try' ':' block except_block+ [else_block] [finally_block] 



# Except statement

except_block: # Manejo de errores normales
    | 'except' expression ':' block 
    | 'except' expression 'as' NAME ':' block 
    | 'except' expressions ':' block 
    | 'except' ':' block 

finally_block: # Bloque de final
    | 'finally' ':' block  

# Match statement
match_stmt: # Es como un switch 
    | "match" subject_expr ':' NEWLINE INDENT case_block+ DEDENT # Identacion, debe tener al menos un case_block

subject_expr:
    | named_expression
    | named_expression (',' named_expression)+ [',']  # uno o más sujetos separados por comas (sin '*')

case_block:
    | "case" patterns guard? ':' block  # Para cada caso, puede etener un guard que es una expresion if

guard: 'if' named_expression 



patterns:
    | pattern

pattern:
    | as_pattern
    | or_pattern

as_pattern:
    | or_pattern 'as' pattern_capture_target 

or_pattern:
    | '|'.closed_pattern+ # Acepta or

closed_pattern:
    | literal_pattern
    | capture_pattern
    | value_pattern
    | group_pattern
    | sequence_pattern
    | mapping_pattern
    | class_pattern




# Literal patterns
literal_pattern:
    | signed_number !('+' | '-')  # un numero sin signo
    | strings 
    | 'None' 
    | 'True' 
    | 'False' 


# Literal expressions are used to restrict permitted mapping pattern keys
literal_expr:
    | signed_number !('+' | '-')
    | strings
    | 'None' 
    | 'True' 
    | 'False' 
# Numero entero con signo
signed_number:
    | NUMBER
    | '-' NUMBER 
# Numero real con signo
signed_real_number:
    | real_number
    | '-' real_number 
# Numero real
real_number:
    | NUMBER 

capture_pattern:
    | pattern_capture_target 

pattern_capture_target:
    | !"_" NAME !('.' | '(' | '=')  # Captura solo el nombre

value_pattern:
    | attr !('.' | '(' | '=')  

attr:
    | name_or_attr '.' NAME  # Para hacer matching de valores como atributos

name_or_attr:
    | attr
    | NAME

group_pattern:
    | '(' pattern ')'  # acepta parentesis para agrupar

sequence_pattern:
    | '[' [ pattern (',' pattern)* [','] ] ']'  # lista 
    | '(' [ pattern (',' pattern)* [','] ] ')'  # tupla 

# Mapeo para match y case
mapping_pattern:
    | '{' '}' 
    | '{' items_pattern ','? '}' 

items_pattern:
    | ','.key_value_pattern+

key_value_pattern:
    | (literal_expr | attr) ':' pattern 


class_pattern:
    | name_or_attr '(' ')' # Clase vacia
    | name_or_attr '(' positional_patterns ','? ')'  # Clase con argumentos posicionales
    | name_or_attr '(' keyword_patterns ','? ')' # Argumentos por nombre
    | name_or_attr '(' positional_patterns ',' keyword_patterns ','? ')'  # Mezcla

positional_patterns:
    | ','.pattern+  # Lista de patrones separados por comas

keyword_patterns:
    | ','.keyword_pattern+ # lista de nombres separadas por comas

keyword_pattern:
    | NAME '=' pattern  # Asignacion de valor


# EXPRESSIONS

expressions:
    | expression (',' expression )+ [','] 
    | expression ',' 
    | expression



expression:
    | disjunction 'if' disjunction 'else' expression 
    | disjunction

assignment_expression:
    | NAME ':=' ~ expression 

named_expression:
    | assignment_expression
    | expression !':='

disjunction:
    | conjunction ('or' conjunction )+ 
    | conjunction

conjunction:
    | inversion ('and' inversion )+ 
    | inversion
inversion:
    | 'not' inversion 
    | comparison
# Operadores de comparacion
comparison:
    | bitwise_or compare_op_bitwise_or_pair+ 
    | bitwise_or

compare_op_bitwise_or_pair:
    | eq_bitwise_or
    | noteq_bitwise_or
    | lte_bitwise_or
    | lt_bitwise_or
    | gte_bitwise_or
    | gt_bitwise_or
    | notin_bitwise_or
    | in_bitwise_or
    | isnot_bitwise_or
    | is_bitwise_or

eq_bitwise_or: '==' bitwise_or 
noteq_bitwise_or:
    | ('!=' ) bitwise_or 

lte_bitwise_or: '<=' bitwise_or 

lt_bitwise_or: '<' bitwise_or 

gte_bitwise_or: '>=' bitwise_or 

gt_bitwise_or: '>' bitwise_or 

notin_bitwise_or: 'not' 'in' bitwise_or 

in_bitwise_or: 'in' bitwise_or 

isnot_bitwise_or: 'is' 'not' bitwise_or 

is_bitwise_or: 'is' bitwise_or 

# BITWISE OPERATORS

bitwise_or:
    | bitwise_xor bitwise_or_refactor
  
bitwise_or_refactor:
    | '|' bitwise_xor bitwise_or_refactor
    | ε


bitwise_xor:
    | bitwise_and bitwise_xor_tail


bitwise_xor_refactor:
    | '^' bitwise_and bitwise_xor_refactor
    | ε

bitwise_and:
    | shift_expr bitwise_and_refactor

bitwise_and_refactor:
    | '&' shitf_expr bitwise_and_refactor
    | ε

shift_expr:
    | sum shitf_expr_refacto

shift_expr_refactor:
    | '<<' sum shitf_expr_refactor
    | '>>' sum shitf_expr_refactor
    | ε

# Operaciones Aritmeticas


sum:
    | term sum_tail

sum_tail:
    | '+' term sum_tail
    | '-' term sum_tail
    | ε


term:
    | factor term_tail

term_tail:
    | '*' factor term_tail
    | '/' factor term_tail
    | '//' factor term_tail
    | '%' factor term_tail
    | '@' factor term_tail
    | ε

factor:
    | '+' factor 
    | '-' factor 
    | '~' factor 
    | power

power:
    | await_primary '**' factor 
    | await_primary


# Elementos primarios (Atributos,metodos)

await_primary: # funciones para co rutinas
    | 'await' primary 
    | primary

primary:
    | atom trailer*

trailer:
    | '.' NAME
    | '(' [arguments] ')'
    | '[' slices ']'

slices:
    | slice !',' 
    | ','.slice [','] 

slice:
    | [expression] ':' [expression] [':' [expression] ] 
    | named_expression 

atom:
    | NAME
    | 'True' 
    | 'False' 
    | 'None' 
    | string
    | NUMBER
    | (tuple | group)
    | list
    | dict
    | set
    | '...' 

# TOKEN STRING
string: STRING 

list:
    | '[' [expressions] ']' 

tuple:
    | '(' [expressions] ')' 

set:
    | '{' [expressions] '}'



# Diccionario
dict:
    | '{' [kvpair (',' kvpair)* [','] ] '}' 

kvpair: expression ':' expression 


# FUNCTION CALL ARGUMENTS

arguments:
    | [arg_list] [',']

arg_list:
    | positional_args [',' keyword_args]   # posicionales opcionales, luego opcionales keyword
    | keyword_args                         # o solo keyword args

positional_args:
    | positional (',' positional)*

positional:
    | assignment_expression    
    | expression !':='        

keyword_args:
    | kwarg (',' kwarg)*

kwarg:
    | NAME '=' expression 

# ASSIGNMENT TARGETS

targets:
    | single_target !',' 
    | single_target (',' single_target )* [','] 

targets_list_seq: ','.single_target+ [','] 

targets_tuple_seq:
    | single_target (',' single_target )+ [','] 
    | single_target ',' 


target_with_atom:
    | t_primary '.' NAME !t_lookahead 
    | t_primary '[' slices ']' !t_lookahead 
    | atom_target

atom_target:
    | NAME 
    | '(' target_with_atom ')' 
    | '(' [targets_tuple_seq] ')' 
    | '[' [targets_list_seq] ']' 

single_target:
    | single_subscript_attribute_target
    | NAME 
    | '(' single_target ')' 

single_subscript_attribute_target:
    | t_primary '.' NAME !t_lookahead 
    | t_primary '[' slices ']' !t_lookahead 

t_primary:
    | atom t_primary_refactor

t_primary_refactor:
    | '.' NAME t_primary_refactor
    | '[' slices ']' t_primary_refactor
    | '(' [arguments] ')' t_primary_ractor
    | ε

t_lookahead: '(' | '[' | '.'

# Targets for del statements

del_targets: ','.del_target+ [','] 

del_target:
    | t_primary '.' NAME !t_lookahead 
    | t_primary '[' slices ']' !t_lookahead 
    | del_t_atom

del_t_atom:
    | NAME 
    | '(' del_target ')' 
    | '(' [del_targets] ')' 
    | '[' [del_targets] ']' 


# TYPING ELEMENTS
type_expressions:
    | ','.expression+ [',']  # lista de expresiones separadas por comas (ej. int, str, bool)

func_type_comment:
    | NEWLINE TYPE_COMMENT &(NEWLINE INDENT)   # Must be followed by indented block
    | TYPE_COMMENT



```bash