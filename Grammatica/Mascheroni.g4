grammar Mascheroni;

    start
        : (APPROXIMATE)? construct+ EOF
        ;

    construct
        : 'to' 'construct' NAME (base_construct_res)? 'given' base_construct_params 'do' step+ 'done'             # BaseConstruct
        | 'to' 'construct' NAME inductive_construct_res 'given' inductive_construct_params 'do' step+ 'done'      # InductiveConstruct
        ;

    // Construct base:
    base_construct_res
        : typed_name (',' typed_name)*
        ;

    base_construct_params
        : typed_name (',' typed_name)*
        ;

    // Construct induttivi:
    inductive_construct_res
        : typed_name_name (',' typed_name_name)*
        ;

    inductive_construct_params
        : (typed_name | typed_int_name) (',' (typed_name | typed_int_name))*
        ;
    
    // Passi:
    step
        : show                                                                  # StepShow
        | 'let' NAME '=' int_expression                                         # StepAssignement
        | 'define' named_expression                                             # StepDefine
        | 'with' named_expression ('and' named_expression)* 'do' step+ 'done'   # StepWith
        | ifs                                                                   # StepIfs
        ;

    show
        : 'show'                                                                # ShowNoLabel
        | 'showLabel'                                                           # ShowLabel
        ;
    
    // Blocco if / if-else:
    ifs
        : 'if' condition 'then' step+ 'fi'                                      # IfThen
        | 'if' condition 'then' step+ 'else' step+ 'fi'                         # IfElseThen
        ;

    condition
        : op='!' expr=condition                                                 # ConditionNot
        | left=int_expression op=('<' | '<=' | '>' | '>=') right=int_expression # ConditionComparison
        | left=int_expression op=('==' | '!=') right=int_expression             # ConditionEquality
        | '(' condition ')'                                                     # ConditionParens
        ;

    named_expression
        : ente_expression 'as' inductive_names ('upto' int_expression)?
        ;

    inductive_name
        : expression_name                                                       # InductiveExpression
        | name_name                                                             # InductiveNameName
        | int_name                                                              # InductiveInt
        | NAME                                                                  # InductiveName
        ;
    
    inductive_names
        : inductive_name (',' inductive_name)*
        ;

    
    // Espressioni sugli enti:
    ente_expression
        : Type=(SEGMENT | RAY | LINE | CIRCLE) '[' ente_expression ',' ente_expression ']'      # EnteExpressionPrimitive
        | left=ente_expression op=('^' | '^0' | '^1') right=ente_expression                     # EnteExpressionIntersection
        | NAME '(' invocation_params ')'                                                        # EnteExpressionInvocation
        | inductive_name                                                                        # EnteExpressionName
        ;

    invocation_params
        : ente_expression (',' ente_expression)*
        ;


    // Espressioni intere:
    int_expression
        : left=int_expression op=('*' | '/' | '%') right=int_expression     # IntExpressionMulDivMod
        | left=int_expression op=('+' | '-') right=int_expression           # IntExpressionAddSub
        | NAME                                                              # IntExpressionID
        | INT                                                               # IntExpressionInt
        | '(' int_expression ')'                                            # IntExpressionParens
        ;

    
    // Nomi:
    int_name
        : NAME '_' INT
        ;

    name_name
        : NAME '_' NAME
        ;

    expression_name
        : NAME '_' '(' int_expression ')'
        ;

    
    // Nomi tipizzati:
    typed_name
        : Type=(POINT | SEGMENT | RAY | LINE | CIRCLE) NAME
        ;
        
    typed_int_name
        : Type=(POINT | SEGMENT | RAY | LINE | CIRCLE) int_name
        ;
    
    typed_name_name
        : Type=(POINT | SEGMENT | RAY | LINE | CIRCLE) name_name
        ;
    
    APPROXIMATE : 'approximate';
    POINT       : 'point';
    SEGMENT     : 'segment';
    RAY         : 'ray';
    LINE        : 'line';
    CIRCLE      : 'circle';
    NAME        : [a-zA-Z]+;
    INT         : [0-9]+;

    SEP         : ',';
    MUL         : '*';
    DIV         : '/';
    MOD         : '%';
    PLUS        : '+';
    MINUS       : '-';
    EQUAL       : '==';
    NOTEQUAL    : '!=';
    GREATER     : '>';
    GREATEREQ   : '>=';
    LESS        : '<';
    LESSEQ      : '<=';
    BOOLNOT     : '!';
    INTERSECT   : '^';
    INTERSECTFR : '^0';
    INTERSECTSC : '^1';
    
    WS: [ \r\n\t]+ -> skip ;