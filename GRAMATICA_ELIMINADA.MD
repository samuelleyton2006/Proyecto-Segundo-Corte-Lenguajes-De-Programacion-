```bash

decorators: ('@' named_expression NEWLINE )+ # DECORATORS

yield_stmt: yield_expr  # YIELD EXPRESSIONS
# PARAMETROS 
slash_no_default:
    | param_no_default+ '/' ',' 
    | param_no_default+ '/' &')' 
slash_with_default:
    | param_no_default* param_with_default+ '/' ',' 
    | param_no_default* param_with_default+ '/' &')' 

star_etc:
    | '*' param_no_default param_maybe_default* [kwds] 
    | '*' param_no_default_star_annotation param_maybe_default* [kwds] 
    | '*' ',' param_maybe_default+ [kwds] 
    | kwds 

kwds:
    | '**' param_no_default 

param_no_default:
    | param ',' TYPE_COMMENT? 
    | param TYPE_COMMENT? &')' 
param_no_default_star_annotation:
    | param_star_annotation ',' TYPE_COMMENT? 
    | param_star_annotation TYPE_COMMENT? &')' 
param_with_default:
    | param default ',' TYPE_COMMENT? 
    | param default TYPE_COMMENT? &')' 
param_maybe_default:
    | param default? ',' TYPE_COMMENT? 
    | param default? TYPE_COMMENT? &')' 
param: NAME annotation? 
param_star_annotation: NAME star_annotation 
annotation: ':' expression 
star_annotation: ':' star_expression 
default: '=' expression  | invalid_default

### WITH STATEMENT
with_stmt:
    | 'with' '(' ','.with_item+ ','? ')' ':' [TYPE_COMMENT] block 
    | 'with' ','.with_item+ ':' [TYPE_COMMENT] block 
    | 'async' 'with' '(' ','.with_item+ ','? ')' ':' block 
    | 'async' 'with' ','.with_item+ ':' [TYPE_COMMENT] block 

with_item:
    | expression 'as' star_target &(',' | ')' | ':') 
    | expression 

# Exceptions 
except_star_block:
    | 'except' '*' expression ':' block 
    | 'except' '*' expression 'as' NAME ':' block 
    | 'except' '*' expressions ':' block 
# Type (ALIAS)
type_alias:
    | "type" NAME [type_params] '=' expression 


type_params:
    | '[' type_param_seq ']' 

type_param_seq: ','.type_param+ [','] 

type_param:
    | NAME [type_param_bound] [type_param_default] 
    | '*' NAME [type_param_starred_default] 
    | '**' NAME [type_param_default] 

type_param_bound: ':' expression 
type_param_default: '=' expression 
type_param_starred_default: '=' star_expression 

group:
    | '(' (yield_expr | named_expression) ')' 
    lambdef:
    | 'lambda' [lambda_params] ':' expression 

lambda_params:
    | lambda_parameters

# lambda_parameters etc. duplicates parameters but without annotations
# or type comments, and if there's no comma after a parameter, we expect
# a colon, not a close parenthesis.  (For more, see parameters above.)
#
lambda_parameters:
    | lambda_slash_no_default lambda_param_no_default* lambda_param_with_default* [lambda_star_etc] 
    | lambda_slash_with_default lambda_param_with_default* [lambda_star_etc] 
    | lambda_param_no_default+ lambda_param_with_default* [lambda_star_etc] 
    | lambda_param_with_default+ [lambda_star_etc] 
    | lambda_star_etc 

lambda_slash_no_default:
    | lambda_param_no_default+ '/' ',' 
    | lambda_param_no_default+ '/' &':' 

lambda_slash_with_default:
    | lambda_param_no_default* lambda_param_with_default+ '/' ',' 
    | lambda_param_no_default* lambda_param_with_default+ '/' &':' 

lambda_star_etc:
    | '*' lambda_param_no_default lambda_param_maybe_default* [lambda_kwds] 
    | '*' ',' lambda_param_maybe_default+ [lambda_kwds] 
    | lambda_kwds 

lambda_kwds:
    | '**' lambda_param_no_default 

lambda_param_no_default:
    | lambda_param ',' 
    | lambda_param &':' 
lambda_param_with_default:
    | lambda_param default ',' 
    | lambda_param default &':' 
lambda_param_maybe_default:
    | lambda_param default? ',' 
    | lambda_param default? &':' 
lambda_param: NAME 



# Generadores
for_if_clauses:
    | for_if_clause+ 

for_if_clause:
    | 'async' 'for' star_targets 'in' ~ disjunction ('if' disjunction )* 
    | 'for' star_targets 'in' ~ disjunction ('if' disjunction )* 

listcomp:
    | '[' named_expression for_if_clauses ']' 

setcomp:
    | '{' named_expression for_if_clauses '}' 

genexp:
    | '(' ( assignment_expression | expression !':=') for_if_clauses ')' 

dictcomp:
    | '{' kvpair for_if_clauses '}' 

```