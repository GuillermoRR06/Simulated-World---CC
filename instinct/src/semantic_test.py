from lexer.lexer import Lexer
from nodes.nodes import DumpAst
from parser.parser import Parser
from semantic.semantic import SemanticAnalyzer

def run_test(title, code_str):
    print(f"\n----- Pruebas: {title} ----")
    try:
        lex = Lexer(code_str)
        tokens = lex.Tokenize()
        pars = Parser(tokens, None, None)
        ast = pars.Parse()

        analyzer = SemanticAnalyzer()
        analyzer.Analyze(ast)
        
        print(tokens)
        
        DumpAst(ast)

    except SemanticError as e:
        print(f"Error Semantico Capturado: {e}")
    except Exception as e:
        print(f"Error inesperado {e}")

test_code = """ # uruk.ins
creature Uruk
faction isengard
health 80
vision 6
lifespan 400
start:
if health < 20 goto flee
if enemy_dist == 1 goto bite
if enemy_dist > 0 goto hunt
if health > 70 and allies_near < 2 goto breed
if allies_near > 3 goto celebrate
wander:
move(random % 3 - 1, random % 3 - 1, 1)
goto start
bite:
consume(enemy_dx, enemy_dy, 15, 15)
goto start
hunt:
move(enemy_dx, enemy_dy, 2)
goto start
flee:
move(-enemy_dx, -enemy_dy, 3)
goto start
breed:
# bred in the pits of Isengard
if see(x, y + 1) != GROUND goto wander
reproduce(0, 1, 30)
goto start
celebrate:
say("meat is back on the menu")
roar("we are the fighting Uruk-hai")
goto start """


run_test("Caso del pdf", test_code)