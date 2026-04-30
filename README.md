
# Triton Lexical Analyzer

This lexical analyzer is designed mainly for Triton (essentially Python).

Lexer.py is a program that reads Triton code and divides it into tokens. Tokens have an ID and belong to categories,
this way interpretation (contextualization) of Triton code is possible rather than just characters.


## Functionality

The lexer scans code in the following order:

1. NEWLINE
2. WHITESPACE / TAB
3. COMMENTS
4. LETTER / UNDERSCORE
    1. BOOLEAN
    2. KEYWORDS
    3. DATA TYPES
    4. IDENTIFIERS
5. NUMBERS
6. STRINGS
7. OPERATORS
8. DELIMITERS
9. UNKNOWN (ERROR)

---

## Rules
* NEWLINES
    - Must be exactly chars '\n'

* WHITESPACE / TAB
    - Ignored unless part of a string (detected by ' ' or '\t')

* COMMENTS
    - Starting with # gets ignored until NEWLINE

* LETTER / UNDERSCORE
    * BOOLEAN or KEYWORDS
        - KEYWORDS are reserved words (if, for, return, etc.)
        - BOOLEAN are also keywords, but for better display they get detected by either of 'True' or 'False'

    * DATA TYPES
        - 


    * IDENTIFIERS


* NUMBERS


* STRINGS


* OPERATORS


* DELIMITERS


* UNKNOWN (ERROR)


