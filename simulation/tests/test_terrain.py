from simulation.model.terrain import Terrain

grass = Terrain("Grass", ".", 100, 2)
print(grass.name)
print(grass.char)
print(grass.resource_max)
print(grass.regen)

grass.resource = 99
grass.regenerate()

assert grass.resource == 100


instancia = grass.new_instance()
print(instancia.char)