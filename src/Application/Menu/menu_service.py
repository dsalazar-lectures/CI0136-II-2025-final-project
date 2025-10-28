from typing import List, Dict


def generate_menus(recipes, count) -> List[Dict]:
    # Obteraining number of recipes
    n_recipes = len(recipes)

    # If there are no recipes, we simply return an empty list
    if n_recipes == 0:
        return []

    # Generate menus
    menus = []
    for i in range(1, count + 1):
        recipe = recipes[(i - 1) % n_recipes]
        menus.append(
            {
                "menu": f"Menú #{i}",
                "recipe": recipe.to_dict(),
            }
        )
    return menus
