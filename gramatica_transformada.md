```bash
#----------------- OPERADORES----------------------------------------

sum:
    | sum '+' term 
    | sum '-' term 
    | term

term:
    | term '*' factor 
    | term '/' factor 
    | term '//' factor 
    | term '%' factor 
    | term '@' factor 
    | factor


# ------------------------ TRANSFORMACION----------------------------
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
    | ε) term_tail
    | ε


# -------------------------OPERADORES LOGICOS--------------------------
bitwise_or:
    | bitwise_or '|' bitwise_xor 
    | bitwise_xor

bitwise_xor:
    | bitwise_xor '^' bitwise_and 
    | bitwise_and

bitwise_and:
    | bitwise_and '&' shift_expr 
    | shift_expr

shift_expr:
    | shift_expr '<<' sum 
    | shift_expr '>>' sum 
    | sum

# -------------------- TRANSFORMACION ----------------------------------

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
#------------------------ASIGNACION-------------------------------------

assignment:
    | NAME ':' expression assigment_refactor  # Asignacion de anotacion para variables (x: int) y (x: int=3)
    | ('(' single_target ')'  # Anotacion con parentesis () o con objetos complejos (obj.attr: str)
         | single_subscript_attribute_target) ':' expression assigment_refactor
    | (targets '=' )+ annotated_rhs !'=' [TYPE_COMMENT] # Uno o mas pares de asignaciones (a = b = 3)
    | single_target augassign ~ annotated_rhs # Asignacion aumentada 

# -------------------- TRANSFORMACION ----------------------------------

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


#--------------------------RETURN---------------------------------------
return_stmt: 
    | 'return' [expression]  # Palabra reservada return y posibilidad de devolver valores 

raise_stmt:
    | 'raise' expression ['from' expression ]  # Generar un error con un from
    | 'raise'  # Re lanzar la excepción activa dentro de un bloque except


# -------------------- TRANSFORMACION ----------------------------------

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

# -------------------- GLOBAL----------------------------------
global_stmt: 'global' ','.NAME+  # Creacion de una o mas variables Globales usando , y NAME (global x,y)

# -------------------- TRANSFORMACION ----------------------------------
global_stmt:
    | 'global' global_name_list

global_name_list:
    | NAME global_name_list_tail

global_name_list_tail:
    | ',' NAME global_name_list_tail
    | ε

#-----------------------Nonlocal--------------------------------------

nonlocal_stmt: 'nonlocal' ','.NAME+ # Creacion de variables de tipo nonlocal (permite usar variables de funciones, en una funcion)

# -------------------- TRANSFORMACION ----------------------------------

nonlocal_stmt: 'nonlocal' nonlocal_name_list

nonlocal_name_list:
    | NAME nonlocal_name_list_tail

nonlocal_name_list_tail
    | ',' NAME global_name_list_tail
    | ε

#-----------------------del statement-----------------------------------
del_stmt:
    | 'del' del_targets &(';' | NEWLINE)  

# -------------------- TRANSFORMACION ----------------------------------
del_stmt:
    | 'del' del_targets del_stmt_terminator

del_stmt_terminator:
    | ';'
    | NEWLINE

#-----------------------assert_stmt-----------------------------------
assert_stmt: 'assert' expression [',' expression] 

# -------------------- TRANSFORMACION ----------------------------------

assert_stmt: 'assert' expression assert_stmt_expression

assert_stmt_expression:
    | ',' expression
    | ε 


#-----------------------import_from-----------------------------------

import_from:
    | 'from' ('.' | '...')* dotted_name 'import' import_from_targets 
    | 'from' ('.' | '...')+ 'import' import_from_targets 

# -------------------- TRANSFORMACION ----------------------------------
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

#----------------import_from_targets:-----------------------------------


import_from_targets:
    | '(' import_from_as_names [','] ')' 
    | import_from_as_names !','
    | '*' 

import_from_as_names:
    | ','.import_from_as_name+ 

import_from_as_name:
    | NAME ['as' NAME ] 

dotted_as_names:
    | ','.dotted_as_name+  # una o mas concurrencias separadas por ,

dotted_as_name:
    | dotted_name ['as' NAME ]  # import AS 

dotted_name:
    | dotted_name '.' NAME  # import .NAME
    | NAME

# -------------------- TRANSFORMACION ----------------------------------

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
#----------------class_def_raw-----------------------------------

class_def_raw:
    | 'class' NAME ['(' [arguments] ')' ] ':' block  # Definicion formal de clase ( class NAME)

# -------------------- TRANSFORMACION ----------------------------------
class_def_raw:
    | 'class' NAME class_def_raw_parentesis ':' block  # Definicion formal de clase ( class NAME)

class_def_raw_parentesis:
    | '(' class_def_rauw_argument ')'
    | ε

class_def_raw_argument
    | arguments
    | ε
```bash