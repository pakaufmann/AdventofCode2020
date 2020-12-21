import itertools


class Food:
    def __init__(self, line: str):
        parts = line.split(" (contains ")
        self.ingredients = parts[0].split(" ")
        self.allergens = parts[1].replace(")", "").split(", ")


with open("inputs/day21.txt", "r") as f:
    foods = [Food(line.replace("\n", "")) for line in f]
    allergens = set(itertools.chain(*(food.allergens for food in foods)))
    ingredients = set(itertools.chain(*(food.ingredients for food in foods)))
    allergens_to_foods: dict[str, list[Food]] = dict(
        (allergen, list(filter(lambda f: allergen in f.allergens, foods))) for allergen in allergens)

    possibly_allergic = set()

    for allergen, ingredient in itertools.product(allergens, ingredients):
        in_all_foods = all(ingredient in food.ingredients for food in allergens_to_foods[allergen])

        if in_all_foods:
            possibly_allergic.add(ingredient)


def day21_part1():
    not_allergic_ingredients = ingredients - possibly_allergic
    print(sum(len(set(food.ingredients).intersection(not_allergic_ingredients)) for food in foods))


def day21_part2():
    ingredient_to_allergens: dict[str, set[str]] = dict()

    for ingredient, allergen in itertools.product(possibly_allergic, allergens):
        in_all_foods = all(ingredient in food.ingredients for food in (allergens_to_foods[allergen]))

        if in_all_foods:
            possible = ingredient_to_allergens.get(ingredient, set())
            possible.add(allergen)
            ingredient_to_allergens[ingredient] = possible

    while not all(len(val) == 1 for val in ingredient_to_allergens.values()):
        unambiguous_allergens = set(itertools.chain(*filter(lambda x: len(x) == 1, ingredient_to_allergens.values())))

        for ingredient, remaining_allergens in ingredient_to_allergens.items():
            if len(remaining_allergens) > 1:
                ingredient_to_allergens[ingredient] = remaining_allergens - unambiguous_allergens

    ingredient_to_allergen = sorted(
        dict((ingredient, list(allergen)[0]) for ingredient, allergen in ingredient_to_allergens.items()).items(),
        key=lambda x: x[1]
    )

    print(",".join(map(lambda x: x[0], ingredient_to_allergen)))
