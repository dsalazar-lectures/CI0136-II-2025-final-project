import ast

class Recipe:
    def __init__(self, id, name, categories, ingredients, duration, instructions,
                 portions, author, califications_sumatory, califications_amount, users_used_recipe):
        self.id = int(id)
        self.name = name
        self.categories = ast.literal_eval(categories)
        self.ingredients = ast.literal_eval(ingredients)
        self.duration = int(duration)
        self.instructions = instructions
        self.portions = int(portions)
        self.author = author
        self.califications_sumatory = int(califications_sumatory)
        self.califications_amount = int(califications_amount)
        self.users_used_recipe = int(users_used_recipe)

    @property
    def rating(self):
        return self.califications_sumatory / self.califications_amount if self.califications_amount > 0 else 0
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "categories": self.categories,
            "ingredients": self.ingredients,
            "duration": self.duration,
            "instructions": self.instructions,
            "portions": self.portions,
            "author": self.author,
            "rating": self.rating,
            "amount of users that have used this recipe": self.users_used_recipe,
        }

