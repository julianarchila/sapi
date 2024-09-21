import pokebase as pb

chesto = pb.APIResource("berry", "chesto")

print(chesto)

charmander = pb.pokemon("charmander")
print(charmander.height)
