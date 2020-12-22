import sys
import re
import itertools
from collections import Counter, defaultdict

pattern = re.compile(r"^(\w+(?: \w+)*) \(contains (\w+(?:, \w+)*)\)$")

joint_count = Counter()
ingredient_count = Counter()
allergen_count = Counter()
for line in sys.stdin:
    line = line.strip()
    if line:
        m = pattern.match(line)
        name, allergens = m.groups()
        allergens = allergens.split(", ")
        ingredients = name.split(" ")
        joint = itertools.product(ingredients, allergens)
        ingredient_count.update(ingredients)
        allergen_count.update(allergens)
        joint_count.update(joint)

joint_count = defaultdict(int, joint_count)
ingredient_count = defaultdict(int, ingredient_count)
allergen_count = defaultdict(int, allergen_count)

ingredients_can_contain = {}
ingredients_with_no_allergens = set()
for ingredient in ingredient_count:
    can_contain = set()
    for allergen in allergen_count:
        if joint_count[(ingredient, allergen)] == allergen_count[allergen]:
            # Allergen always occurs with this ingredient
            can_contain.add(allergen)
    if can_contain:
        ingredients_can_contain[ingredient] = can_contain
    else:
        ingredients_with_no_allergens.add(ingredient)
print("Part 1:", sum(ingredient_count[ig] for ig in ingredients_with_no_allergens))


ingredient_allergen_pairs = []
while len(ingredients_can_contain) > 0:
    ig, allergens = min(ingredients_can_contain.items(), key=lambda x: len(x[1]))
    assert len(allergens) == 1
    allergen = next(iter(allergens))
    ingredient_allergen_pairs.append((ig, allergen))
    del ingredients_can_contain[ig]
    for allergens in ingredients_can_contain.values():
        if allergen in allergens:
            allergens.remove(allergen)
ingredients, _ = zip(*sorted(ingredient_allergen_pairs, key=lambda x: x[1]))
print(",".join(ingredients))
