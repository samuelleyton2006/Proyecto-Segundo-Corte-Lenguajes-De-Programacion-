```bash

sum:
    | term sum_tail

sum_tail:
    | ('+' term) sum_tail
    | ('-' term) sum_tail
    | ε



term:
    | factor term_tail

term_tail:
    | ('*' factor) term_tail
    | ('/' factor) term_tail
    | ('//' factor) term_tail
    | ('%' factor) term_tail
    | ('@' factor) term_tail
    | ε




bitwise_or:
    | bitwise_xor bitwise_or_tail

bitwise_or_tail:
    | '|' bitwise_xor bitwise_or_tail
    | ε



bitwise_xor:
    | bitwise_and bitwise_xor_tail

bitwise_xor_tail:
    | '^' bitwise_and bitwise_xor_tail
    | ε

bitwise_and:
    | shift_expr bitwise_and_tail

bitwise_and_tail:
    | '&' shift_expr bitwise_and_tail
    | ε


shift_expr:
    | sum shift_expr_tail

shift_expr_tail:
    | '<<' sum shift_expr_tail
    | '>>' sum shift_expr_tail
    | ε



dotted_name:
    | NAME dotted_name_tail

dotted_name_tail:
    | '.' NAME dotted_name_tail
    | ε


t_primary:
    | atom t_primary_tail

t_primary_tail:
    | trailer t_primary_tail
    | ε

trailer:
    | '.' NAME
    | '(' [arguments] ')'
    | '[' slices ']'

```bash