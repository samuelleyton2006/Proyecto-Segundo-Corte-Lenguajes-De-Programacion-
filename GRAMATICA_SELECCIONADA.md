```bash
# Un archivo consta de statements y un fin de archivo (ENDMARKER)

file: file_refactor ENDMARKER  

file_refactor:
    | statements
    | ε



statements:
    | statement statements_tail

statements_tail:
    | NEWLINE statement statements_tail
    | ε

statement:
    | compound_stmt
    | small_stmt_line

small_stmt_line:
    | small_stmt small_stmt_line_tail NEWLINE

small_stmt_line_tail:
    | ';' small_stmt small_stmt_line_tail
    | ε

small_stmt:
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

    

#-------------

assignment:
    | single_target assignment_options type_comment

assignment_options:
    | ':' expression annotated_assignment_opt       
    | '=' single_target_chain_tail annotated_rhs 
    | augassign annotated_rhs                         

single_target_chain_tail:
    | '=' single_target single_target_chain_tail 
    | ε
    
annotated_assignment_opt:
    | '=' annotated_rhs
    | ε
    
target_assignment: 
    | single_target
    
annotated_rhs:
    | expression
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
    | 'raise' raise_stmt_tail

raise_stmt_tail:
    | expression from_expression
    | ε

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

nonlocal_name_list_tail:
    | ',' NAME nonlocal_name_list_tail
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

#------------------------ Import Statements
import_stmt:
    | 'import' import_tail
    | 'from' from_import_tail

import_tail:
    | dotted_as_names

from_import_tail:
    | dots dotted_name_opt 'import' import_from_targets

dots:
    | dot dots_tail
    | ε

dots_tail:
    | dot dots_tail
    | ε
dot:
    | '.'
    | '...'

dotted_name_opt:
    | dotted_name
    | ε

dotted_name:
    | NAME dotted_name_tail

dotted_name_tail:
    | '.' NAME dotted_name_tail
    | ε

dotted_as_name:
    | dotted_name dotted_as_name_alias

dotted_as_name_alias:
    | 'as' NAME
    | ε

dotted_as_names:
    | dotted_as_name dotted_as_names_tail

dotted_as_names_tail:
    | ',' dotted_as_name dotted_as_names_tail
    | ε

import_from_targets:
    | '(' import_from_as_names_opt ')'
    | import_from_as_names
    | '*'

import_from_as_names_opt:
    | import_from_as_names
    | ε

import_from_as_names:
    | import_from_as_name import_from_as_names_tail

import_from_as_names_tail:
    | ',' import_from_as_name import_from_as_names_tail
    | ε

import_from_as_name:
    | NAME import_from_as_alias

import_from_as_alias:
    | 'as' NAME
    | ε

#------------------------ Statemet compuesto

block:
    | NEWLINE INDENT statements DEDENT
    | simple_stmt_line


#-------------------------------- CLASES

class_def:
    | class_def_raw

class_def_raw:
    | 'class' NAME class_def_raw_parentesis ':' block  # Definicion formal de clase ( class NAME)

class_def_raw_parentesis:
    | '(' class_def_raw_argument ')'
    | ε

class_def_raw_argument:
    | arguments
    | ε

#####  FUNCIONES

function_def:
    | function_def_raw 

function_def_raw:
    | 'def' NAME '(' function_def_raw_refactor ')' function_def_raw_expression ':' func_type_comment block 
    | 'async' 'def' NAME '(' function_def_raw_refactor ')' function_def_raw_expression ':' func_type_comment block

function_def_raw_refactor:
    | params
    | ε
function_def_raw_expression:
    | '->' expression
    | ε

### PARAMETROS DE FUNCIONES

params:
    | param param_list_rest
    | ε


param_list:
    | param param_list_rest

param_list_rest:
    | ',' param param_list_rest
    | ε

param:
    | NAME param_tail

param_tail:
    | ':' expression opt_default
    | '=' expression
    | ε

opt_default:
    | '=' expression
    | ε

#### if statement

if_stmt:
    | 'if' expression ':' block elif_else_part

elif_else_part:
    | 'elif' expression ':' block elif_else_part
    | else_block
    | ε
else_block:
    | 'else' ':' block 

#### WHILE STATEMENT
while_stmt:
    | 'while' expression ':' block while_else_part

while_else_part:
    | 'else' ':' block
    | ε

# For statement
for_stmt:
    | for_prefix targets 'in' expression ':' type_comment block else_block

for_prefix:
    | 'for'
    | 'async' 'for'

# Try statement
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
    | expression except_header_as_or_comma
    | ε

except_header_as_or_comma:
    | 'as' NAME
    | ',' expression except_header_rest
    | ε

except_header_rest:
    | ',' expression except_header_rest
    | ε


finally_block:
    | 'finally' ':' block
    | ε

# Match statement


match_stmt:
    | 'match' subject_expr ':' NEWLINE INDENT case_block_list DEDENT


subject_expr:
    | expression subject_expr_tail

subject_expr_tail:
    | ',' expression subject_expr_tail_opt_comma
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
    | 'if' expression

#------------------- PATRONES-------------------------------------
patterns:
    | pattern

pattern:
    | or_pattern pattern_as_opt

pattern_as_opt:
    | 'as' pattern_capture_target
    | ε

or_pattern:
    | closed_pattern or_pattern_tail

or_pattern_tail:
    | '|' closed_pattern or_pattern_tail
    | ε

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
    | signed_number  
    | string
    | 'None' 
    | 'True' 
    | 'False' 


# Literal expressions are used to restrict permitted mapping pattern keys
literal_expr:
    | signed_number 
    | string
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
    | NAME  # Captura solo el nombre

value_pattern:
    | attr 



name_or_attr:
    | NAME attr_trail

attr:
    | NAME attr_trail_noempty  # Para hacer matching de valores como atributos
attr_tail:
    | '.' NAME attr_tail
    | ε

attr_tail_nonempty:
    | '.' NAME attr_tail


group_pattern:
    | '(' pattern ')'  # acepta parentesis para agrupar

sequence_pattern:
    | '[' pattern_list_opt ']'
    | '(' pattern_list_opt ')'

pattern_list_opt:
    | pattern pattern_list_rest
    | ε

pattern_list_rest:
    | ',' pattern pattern_list_rest
    | ε

# Mapeo para match y case


mapping_pattern:
    | '{' mapping_items '}'

mapping_items:
    | key_value_list trailing_comma_opt
    | ε

trailing_comma_opt:
    | ','
    | ε

key_value_list:
    | key_value_pair key_value_list_tail

key_value_list_tail:
    | ',' key_value_pair key_value_list_tail
    | ε

key_value_pair:
    | literal_expr ':' pattern
    | attr ':' pattern


class_pattern:
    | name_or_attr '(' class_pattern_body ')'

class_pattern_body:
    | ε
    | first_pattern class_pattern_body_continuation

class_pattern_body_continuation:
    | '=' pattern keyword_mode
    | ',' class_pattern_body_after_comma
    | ε

class_pattern_body_after_comma:
    | first_pattern class_pattern_body_continuation
    | ε

keyword_mode:
    | ',' keyword_pattern keyword_mode_rest
    | ε

keyword_mode_rest:
    | ',' keyword_pattern keyword_mode_rest
    | ε

first_pattern:
    | pattern

keyword_pattern:
    | NAME '=' pattern

# EXPRESSIONS

expressions:
    | expression expressions_tail

expressions_tail:
    | ',' expressions_tail_after_comma
    | ε

expressions_tail_after_comma:
    | expression expressions_tail
    | ε


expression:
    | disjunction expression_tail

expression_tail:
    | 'if' disjunction 'else' expression
    | ε

disjunction:
    | conjunction disjunction_tail

disjunction_tail:
    | 'or' conjunction disjunction_tail
    | ε

conjunction:
    | inversion conjunction_tail

conjunction_tail:
    | 'and' inversion conjunction_tail
    | ε

inversion:
    | inversion_tail comparison

inversion_tail:
    | 'not' inversion_tail
    | ε
# Operadores de comparacion
comparison:
    | bitwise_or comparison_tail

comparison_tail:
    | compare_op_bitwise_or_pair comparison_tail
    | ε

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

eq_bitwise_or:
    | '==' bitwise_or 
noteq_bitwise_or:
    | '!=' bitwise_or 

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
    | bitwise_and bitwise_xor_refactor


bitwise_xor_refactor:
    | '^' bitwise_and bitwise_xor_refactor
    | ε

bitwise_and:
    | shift_expr bitwise_and_refactor

bitwise_and_refactor:
    | '&' shift_expr bitwise_and_refactor
    | ε

shift_expr:
    | sum shift_expr_refactor

shift_expr_refactor:
    | '<<' sum shift_expr_refactor
    | '>>' sum shift_expr_refactor
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
    | unary_operator factor 
    | power                 

unary_operator:
    | '+'
    | '-'
    | '~'
power:
    | await_primary power_tail 

power_tail:
    | '**' factor      
    | ε
# Elementos primarios (Atributos,metodos)

await_primary:
    | 'await' primary
    | primary
    
primary:
    | atom trailer_seq

trailer_seq:
    | trailer_primary trailer_seq
    | ε

trailer_primary:
    | '.' NAME
    | '(' arguments_opt ')'
    | '[' slices ']'

arguments_opt:
    | arguments
    | ε

slices:
    | slice slices_tail

slices_tail:
    | ',' slice slices_tail
    | ε

slice:
    | slice_index


slice_index:
    | ':' expression_opt slice_step_opt       
    | expression slice_continuation 

slice_continuation:
    | ':' expression_opt slice_step_opt      
    | ε    

expression_opt:
    | expression
    | ε

slice_step_opt:
    | ':' expression_opt
    | ε

atom:
    | NAME
    | 'True' 
    | 'False' 
    | 'None' 
    | string
    | NUMBER
    | tuple
    | list
    | collection
    | '...' 

# TOKEN STRING
string:
    | STRING string_tail

string_tail: 
    | STRING string_tail 
    | ε

list:
    | '[' expressions_opt ']' 

tuple:
    | '(' expressions_opt ')' 

expressions_opt:
    | expressions
    | ε

collection:
    | '{' dict_items '}'

dict_items:
    | kvpair_list trailing_comma_opt
    | ε

kvpair_list:
    | kvpair kvpair_list_tail

kvpair_list_tail:
    | ',' kvpair_list_continuation

kvpair_list_continuation:
    | kvpair kvpair_list_tail
    | ε

kvpair:
    | expression ':' expression

trailing_comma_opt:
    | ','
    | ε

# FUNCTION CALL ARGUMENTS


arguments:
    | arg_list arguments_comma
    | ε

arguments_comma:
    | ','
    | ε

arg_list:
    | argument_item arg_list_tail
    | ε 

argument_item:
    | NAME '=' expression 
    | expression

arg_list_tail:
    | ',' argument_item arg_list_tail
    | ε

positional:
    | expression

positional_args:
    | positional positional_args_refactor

positional_args_refactor:
    | ',' positional positional_args_refactor
    | ε
    
keyword_args:
    | kwarg keyword_args_refactor

keyword_args_refactor:
    | ',' kwarg keyword_args_refactor
    | ε

kwarg:
    | NAME '=' expression 

# ASSIGNMENT TARGETS

targets:
    | single_target targets_tail

targets_tail:
    | ',' targets_tail_after_comma
    | ε

targets_tail_after_comma:
    | single_target targets_tail
    | ε

# Targets_list

targets_list_seq:
    | single_target targets_list_seq_tail

targets_list_seq_tail:
    | ',' targets_list_seq
    | ','
    | ε

# Secuencia de targets entre paréntesis (tuplas)
targets_tuple_seq:
    | single_target targets_tuple_seq_rest_comma  

targets_tuple_seq_rest_comma:
    | ',' targets_tuple_seq_rest_body             
    | ε                                           

targets_tuple_seq_rest_body:
    | single_target targets_tuple_seq_tail      
    | ε                                         

targets_tuple_seq_tail:
    | ',' single_target targets_tuple_seq_tail  
    | ε

# Un target que puede ser un nombre, un atributo o un subíndice
atom_target:
    | NAME 
    | '(' single_target ')' 
    | '(' targets_tuple_seq ')' 
    | '[' targets_list_seq ']'

# Target individual (usado en asignaciones simples o anidadas)
single_target:
    | single_target_simple noncall_trailer_seq_opt
    | '[' targets_list_seq ']'
    | '(' single_target_parenthesized ')'

single_target_parenthesized:
    | single_target target_parens_tail

target_parens_tail:
    | ',' targets_tuple_seq_rest  
    | ε

single_target_simple:
    | NAME
single_subscript_attribute_target:
    | atom noncall_trailer_seq_nonempty

noncall_trailer_seq_nonempty:
    | noncall_trailer noncall_trailer_seq_opt

noncall_trailer_seq_opt:
    | noncall_trailer noncall_trailer_seq_opt
    | ε
noncall_trailer:
    | '.' NAME
    | '[' slices ']'
t_primary:
    | atom t_primary_refactor

t_primary_refactor:
    | '.' NAME t_primary_refactor
    | '[' slices ']' t_primary_refactor
    | '(' arguments ')' t_primary_refactor
    | ε

del_targets:
    | del_target del_targets_tail
del_targets_tail:
    | ',' del_target del_targets_tail
    | ε
del_target:
    | NAME noncall_trailer_seq_opt
    | '(' del_target_parenthesized ')' noncall_trailer_seq_opt
    | '[' del_targets_opt_trailing ']' noncall_trailer_seq_opt

del_target_parenthesized:
    | del_target del_target_parens_tail

del_target_parens_tail:
    | ',' del_targets_opt_trailing 
    | ε

del_targets_opt_trailing:
    | del_targets trailing_comma_opt
    | ε
trailing_comma_opt:
    | ','
    | ε
type_expressions:
    | expression type_expressions_tail

type_expressions_tail:
    | ',' type_expressions
    | ','
    | ε

func_type_comment:
    | NEWLINE type_comment func_type_comment_refactor  
    | TYPE_COMMENT
    | ε

func_type_comment_refactor:
    | NEWLINE INDENT
    | ε
type_comment:
    | TYPE_COMMENT
    | ε

```bash