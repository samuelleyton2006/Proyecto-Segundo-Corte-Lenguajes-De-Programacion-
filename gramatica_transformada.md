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

#----------------param-----------------------------------

params:
    | [param_list]                # lista opcional de parámetros

param_list:
    | param (',' param)* [',']    # uno o mas parámetros separados por comas, coma final opcional
param:
    | NAME [':' expression] ['=' expression]   # name [: annotation] [= default]

# -------------------- TRANSFORMACION ----------------------------------

params:
    | ε
    | param_list
    | param_list ','


param_list:
    | param param_list_rest

param_list_rest:
    | ',' param param_list_rest
    | ε

param:
    | NAME param_tail

param_tail:
    | ':' expression param_default_opt
    | '=' expression
    | ε

param_default_opt:
    | '=' expression
    | ε

#----------------IF STATEMENT-----------------------------------


if_stmt:
    | 'if' named_expression ':' block elif_stmt  
    | 'if' named_expression ':' block [else_block]
elif_stmt:
    | 'elif' named_expression ':' block elif_stmt 
    | 'elif' named_expression ':' block [else_block]
else_block:
    | 'else' ':' block

# -------------------- TRANSFORMACION ----------------------------------
if_stmt:
    | 'if' named_expression ':' block elif_stmt  
    | 'if' named_expression ':' block else_block
elif_stmt:
    | 'elif' named_expression ':' block elif_stmt 
    | 'elif' named_expression ':' block else_block
else_block:
    | 'else' ':' block
    | ε

#----------------FOR STATEMENT-----------------------------------

for_stmt:
    | 'for' star_targets 'in' ~ star_expressions ':' [TYPE_COMMENT] block [else_block] 
    | 'async' 'for' star_targets 'in' ~ star_expressions ':' [TYPE_COMMENT] block [else_block] 

# -------------------- TRANSFORMACION ----------------------------------

for_stmt:
    | for_prefix targets 'in' expression ':' type_comment_opt block else_block_opt

for_prefix:
    | 'for'
    | 'async' 'for'

type_comment_opt:
    | TYPE_COMMENT
    | ε

else_block_opt:
    | else_block
    | ε


#----------------TRY STATEMENT-----------------------------------


try_stmt:
    | 'try' ':' block finally_block 
    | 'try' ':' block except_block+ [else_block] [finally_block] 
    | 'try' ':' block except_star_block+ [else_block] [finally_block] 

# -------------------- TRANSFORMACION ----------------------------------
try_stmt:
    | 'try' ':' block try_continuation

try_continuation:
    | finally_block
    | except_block_list else_block finally_block

except_block_list:
    | except_block except_block_list_tail

except_block_list_tail:
    | except_block except_block_list_tail
    | ε

except_block:
    | 'except' except_header ':' block

except_header:
    | expression 'as' NAME
    | expression
    | expressions
    | ε

finally_block:
    | 'finally' ':' block
    | ε

#----------------MATCH STATEMENT-----------------------------------


match_stmt: # Es como un switch 
    | "match" subject_expr ':' NEWLINE INDENT case_block+ DEDENT # Identacion, debe tener al menos un case_block

subject_expr:
    | named_expression
    | named_expression (',' named_expression)+ [',']  # uno o más sujetos separados por comas (sin '*')

case_block:
    | "case" patterns guard? ':' block  # Para cada caso, puede etener un guard que es una expresion if

guard: 'if' named_expression 


# -------------------- TRANSFORMACION ----------------------------------


match_stmt:
    | 'match' subject_expr ':' NEWLINE INDENT case_block_list DEDENT


subject_expr:
    | named_expression subject_expr_tail

subject_expr_tail:
    | ',' named_expression subject_expr_tail_opt_comma
    | ε

subject_expr_tail_opt_comma:
    | ',' 
    | ε


case_block_list:
    | case_block case_block_list_tail

case_block_list_tail:
    | case_block case_block_list_tail
    | ε


case_block:
    | 'case' patterns guard_opt ':' block

guard_opt:
    | guard
    | ε

guard:
    | 'if' named_expression

#-------sequence_pattern:-----------------------------------------------

sequence_pattern:
    | '[' [ pattern (',' pattern)* [','] ] ']'  # lista 
    | '(' [ pattern (',' pattern)* [','] ] ')'  # tupla


# -------------------- TRANSFORMACION ----------------------------------

sequence_pattern:
    | '[' pattern_list_opt ']'
    | '(' pattern_list_opt ')'

pattern_list_opt:
    | pattern pattern_list_rest
    | ε

pattern_list_rest:
    | ',' pattern pattern_list_rest
    | ',' 
    | ε


#----------Mapping pattern--------------------------------------------
mapping_pattern:
    | '{' '}' 
    | '{' items_pattern ','? '}' 

items_pattern:
    | ','.key_value_pattern+

key_value_pattern:
    | (literal_expr | attr) ':' pattern

# -------------------- TRANSFORMACION ----------------------------------

mapping_pattern:
    | '{' mapping_items '}'

mapping_items:
    | ε
    | key_value_list
    | key_value_list ','

key_value_list:
    | key_value_pair key_value_list_tail

key_value_list_tail:
    | ',' key_value_pair key_value_list_tail
    | ε

key_value_pair:
    | literal_expr ':' pattern
    | attr ':' pattern

#----------------------------class pattern---------------------------------------


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


# -------------------- TRANSFORMACION ----------------------------------


class_pattern:
    | name_or_attr '(' class_pattern_body ')'

class_pattern_body:
    | ε
    | positional_patterns class_pattern_body_rest
    | keyword_patterns class_pattern_body_comma_opt

class_pattern_body_rest:
    | ',' keyword_patterns class_pattern_body_comma_opt
    | class_pattern_body_comma_opt

class_pattern_body_comma_opt:
    | ','
    | ε

#----------------------------comparison---------------------------------------


comparison:
    | bitwise_or compare_op_bitwise_or_pair+ 
    | bitwise_or

# -------------------- TRANSFORMACION ----------------------------------


comparison:
    | bitwise_or comparison_tail

comparison_tail:
    | compare_op_bitwise_or_pair comparison_tail
    | ε
#----------------------------await---------------------------------------
await_primary: # funciones para co rutinas
    | 'await' primary 
    | primary

primary:
    | atom trailer*

trailer:
    | '.' NAME
    | '(' [arguments] ')'
    | '[' slices ']'
# -------------------- TRANSFORMACION ----------------------------------

await_primary:
    | 'await' primary
    | atom trailer_seq

primary:
    | atom trailer_seq

trailer_seq:
    | trailer trailer_seq
    | ε

trailer:
    | '.' NAME
    | '(' arguments_opt ')'
    | '[' slices ']'

arguments_opt:
    | arguments
    | ε


#----------------------------slices---------------------------------------


slices:
    | slice !',' 
    | ','.slice [','] 

slice:
    | [expression] ':' [expression] [':' [expression] ] 
    | named_expression 

# -------------------- TRANSFORMACION ----------------------------------
slices:
    | slice slices_tail

slices_tail:
    | ',' slice slices_tail
    | ε

slice:
    | slice_index
    | named_expression

slice_index:
    | expression_opt ':' expression_opt slice_step_opt

expression_opt:
    | expression
    | ε

slice_step_opt:
    | ':' expression_opt
    | ε

#----------------------------DICT Y SET---------------------------------------


set: '{' star_named_expressions '}' 


dict:
    | '{' [double_starred_kvpairs] '}' 

double_starred_kvpairs: ','.double_starred_kvpair+ [','] 

double_starred_kvpair:
    | '**' bitwise_or 
    | kvpair

# -------------------- TRANSFORMACION ----------------------------------

collection:
    | '{' dict_or_set '}'

collection_content:
    | kvpair kvpair_list_tail     # dict
    | expression set_list_tail    # set
    | ε    

# Diccionario o set
kvpair_list_tail:
    | ',' kvpair kvpair_list_tail
    | ε

set_list_tail:
    | ',' expression set_list_tail
    | ε

#----------------------------arg_list---------------------------------------


arg_list:
    | positional_args [',' keyword_args]   # posicionales opcionales, luego opcionales keyword
    | keyword_args                         # o solo keyword args
# -------------------- TRANSFORMACION ----------------------------------

arg_list:
    | positional_args arg_list_refactor
    | keyword_args
arg_list_refactor:
    | ',' keyword_args
    | ε


#----------------------------positional_args--------------------------------------

positional_args:
    | positional (',' positional)*

# -------------------- TRANSFORMACION ----------------------------------
positional_args:
    | positional positional_args_refactor

positional_args_refactor:
    | ',' positional positional_args_refactor
    | ε

```bash