
file: [statements] ENDMARKER  # Un archivo consta de statements y un fin de archivo (ENDMARKER)

statements: statement+      # statements es un conjunto de uno o mas statement

statement:                 # Un statement puede ser un statement compuesto o uno simple
    | compound_stmt 
    | simple_stmts 

single_compound_stmt:        # Un statement compuesto solo, consta de un statement compuesto
    | compound_stmt 


statement_newline:                    # U statement con nueva linea es un statement compuesto solo seguido 
                                      # de un salto de linea linea o un statement simple o una nueva linea o un
    | single_compound_stmt NEWLINE    # fin de marcador
    | simple_stmts
    | NEWLINE 
    | ENDMARKER 


simple_stmts:                          # Statements simples constan de un simple statement, si halla un ';' falla el 
                                       # Analizador
    | simple_stmt !';' NEWLINE         # Not needed, there for speedup
    | ';'.simple_stmt+ [';'] NEWLINE   # Uno o mas statement separados por ; y el final puede terminar en ; con un salto
                                       # de linea