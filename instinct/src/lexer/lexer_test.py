from lexer import Lexer
from tokens import TokenType, Token

codigo_prueba = '''attack(10, 20, 5)
if health < 20 and enemy_dist < 3: say("Cuidado")
x= -7 % 2 goto'''


print("---TOKENIZANDO---")
lexer = Lexer(codigo_prueba)
try:
    tokens = lexer.Tokenize()
    for token in tokens:
        print(token)
    print("\n El token funciono correctamente")
except Exception as e:
    print(f"\n Error en el lexer: {e}")