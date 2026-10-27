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

        analyzer = SemanticAnalyzer(None)
        analyzer.Analyze(ast)
        
        print(tokens)
        
        DumpAst(ast)

    except SemanticError as e:
        print(f"Error Semantico Capturado: {e}")
    except Exception as e:
        print(f"Error inesperado {e}")

test_code_1 = """ # uruk.ins
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

test_code_2 = """# hobbit.ins
creature Hobbit
faction shire
health 60
vision 5
lifespan 300
start:
if enemy_dist >= 0 goto flee
if health > 45 and total_allies < 20 goto breed
if reserve_here > 0 and health < 80 goto second_breakfast
if ally_dist > 1 goto go_ally
wait(1)
goto start
flee:
say("they are taking us to Isengard")
move(-enemy_dx, -enemy_dy, 2)
goto start
second_breakfast:
consume(0, 0, 10, 10)
goto start
go_ally:
move(ally_dx, ally_dy, 1)
goto start
breed:
if see(x + 1, y) == GROUND goto breed_right
if see(x - 1, y) == GROUND goto breed_left
wait(1)
goto start
breed_right:
reproduce(1, 0, 20)
goto start
breed_left:
reproduce(-1, 0, 20)
goto start
"""

test_code_3 = """# ent.ins
creature Ent
faction fangorn
health 150
vision 4
lifespan 1000
start:
home_x = x
home_y = y
watch:
if enemy_dist == 1 goto hit
if enemies_near > 0 and roars_near == 0 goto warn
if x != home_x or y != home_y goto go_home
if health < 150 goto roots
wait(1)
goto watch
hit:
attack(enemy_dx, enemy_dy, 12)
goto watch
warn:
roar("hoom, hom, do not be hasty")
goto watch
roots:
consume(0, 0, 3, 3)
goto watch
go_home:
dx = (home_x > x) - (home_x < x)
dy = (home_y > y) - (home_y < y)
move(dx, dy, 1)
goto watch
"""

test_code_4 = """# dwarf.ins
creature Dwarf
faction erebor
health 100
vision 3
lifespan 600
start:
if last_roar == "khazad ai-menu" goto rescue
if object_dist == 1 and health < 100 goto mine
dx = random % 3 - 1
dy = random % 3 - 1
steps = 0
walk:
if steps >= 5 goto start
if enemy_dist == 1 goto shout
move(dx, dy, 1)
steps = steps + 1
goto walk
mine:
# never too greedily and too deep
if name(x + object_dx, y + object_dy) != "Rock" goto start
consume(object_dx, object_dy, 20, 20)
goto start
shout:
roar("khazad ai-menu")
goto start
rescue:
say("and my axe")
move(ally_dx, ally_dy, 2)
goto start
"""


run_test("Caso del pdf", test_code_1)
run_test("Caso del pdf", test_code_2)
run_test("Caso del pdf", test_code_3)
run_test("Caso del pdf", test_code_4)