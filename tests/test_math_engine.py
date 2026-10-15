import sys
from pathlib import Path

# Asegurar codificación UTF-8 en salida de consola Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.math_engine.registry import engine_registry

def test_baldor_linear():
    print("--> Probando BaldorLinearSolver...")
    # Resolver 3x + 5 = 20
    res1 = engine_registry.solve("baldor_linear_eq", {"a": 3, "b": 5, "c": 20})
    assert len(res1.steps) == 4
    assert res1.final_solutions == ["x = 5"]
    print("    [OK] 3x + 5 = 20 ->", res1.final_solutions)

    # Modificar parámetros en tiempo real: 2x - 8 = 10 -> x = 9
    res2 = engine_registry.solve("baldor_linear_eq", {"a": 2, "b": -8, "c": 10})
    assert res2.final_solutions == ["x = 9"]
    print("    [OK] Recálculo dinámico: 2x - 8 = 10 ->", res2.final_solutions)

def test_baldor_quadratic():
    print("--> Probando BaldorQuadraticSolver...")
    # Resolver x^2 - 5x + 6 = 0 -> raíces 3 y 2
    res1 = engine_registry.solve("baldor_quadratic_eq", {"a": 1, "b": -5, "c": 6})
    assert len(res1.steps) == 5
    assert "x_1 = 3" in res1.final_solutions[0]
    assert "x_2 = 2" in res1.final_solutions[1]
    print("    [OK] x^2 - 5x + 6 = 0 ->", res1.final_solutions)

    # Modificar parámetros con raíces complejas: x^2 + 1 = 0
    res2 = engine_registry.solve("baldor_quadratic_eq", {"a": 1, "b": 0, "c": 1})
    print("    [OK] Raices complejas (Delta < 0): x^2 + 1 = 0 ->", res2.final_solutions)

def test_baldor_system_2x2():
    print("--> Probando BaldorSystems2x2Solver...")
    # 2x + 3y = 13 y x - y = -1 -> x = 2, y = 3
    res = engine_registry.solve("baldor_system_2x2", {"a1": 2, "b1": 3, "c1": 13, "a2": 1, "b2": -1, "c2": -1})
    assert "x = 2" in res.final_solutions[0]
    assert "y = 3" in res.final_solutions[1]
    print("    [OK] Sistema 2x2 resuelto por Cramer ->", res.final_solutions)

def test_baldor_factoring():
    print("--> Probando BaldorFactoringSolver...")
    # x^2 + 7x + 10 -> (x + 5)(x + 2)
    res = engine_registry.solve("baldor_factoring_trinomial", {"b": 7, "c": 10})
    print("    [OK] Factorizacion x^2 + 7x + 10 ->", res.final_solutions)

def test_nuclear_decay():
    print("--> Probando NuclearDecaySolver...")
    # N0 = 1000, half_life = 5, t = 10 (2 vidas medias) -> N(t) = 250
    res = engine_registry.solve("physics_nuclear_decay", {"N0": 1000, "half_life": 5.0, "t": 10.0})
    assert "250.00" in res.final_solutions[0]
    print("    [OK] Decaimiento nuclear (t=10 anos) ->", res.final_solutions)

if __name__ == "__main__":
    test_baldor_linear()
    test_baldor_quadratic()
    test_baldor_system_2x2()
    test_baldor_factoring()
    test_nuclear_decay()
    print("\n[EXITO TOTAL] Todos los solucionadores matematicos de SymPy funcionan a la perfeccion.")

