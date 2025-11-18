from src.Model.Menu.Menu import Menu
from src.Database.Menu.MenuCSV import MenuCSV
from src.Application.Menu.IMenuRepository import IMenuRepository


class MenuRepository(IMenuRepository):
    def __init__(self, csv_file_path="src/Database/Menu/menus.csv"):
        self.menu_csv = MenuCSV(csv_file_path)

    def get_menu_by_id(self, menu_id: int) -> Menu:
        db_menu = self.menu_csv.get_menu_by_id(menu_id)
        if db_menu:
            return Menu(
                menu_id=int(db_menu["menu_id"]),
                breakfast_recipe_id=int(db_menu["breakfast_recipe_id"]),
                lunch_recipe_id=int(db_menu["lunch_recipe_id"]),
                dinner_recipe_id=int(db_menu["dinner_recipe_id"]),
                dessert_recipe_id=int(db_menu["dessert_recipe_id"]),
            )
        return None

    def create_menu(self, menu: Menu):
        if self.menu_exists(menu.menu_id):
            return None, "Menu already exists", 400

        created_menu_data = self.menu_csv.create_menu(menu)
        if created_menu_data:
            menu_entity = Menu(
                menu_id=int(created_menu_data["menu_id"]),
                breakfast_recipe_id=int(created_menu_data["breakfast_recipe_id"]),
                lunch_recipe_id=int(created_menu_data["lunch_recipe_id"]),
                dinner_recipe_id=int(created_menu_data["dinner_recipe_id"]),
                dessert_recipe_id=int(created_menu_data["dessert_recipe_id"]),
            )
            return menu_entity, "Menu created successfully", 201
        return None, "Failed to create menu", 400

    def update_menu(self, menu: Menu):
        if not self.menu_exists(menu.menu_id):
            return None, "Menu does not exist", 404
        # Update logic to be implemented
        return None, "Update functionality not implemented", 501

    # TODO(): Implement delete and list methods
    # def delete_menu(self, menu_id: int):
    #     pass

    # def list_menus(self) -> list:
    #     pass

    def menu_exists(self, menu_id: int) -> bool:
        return self.menu_csv.menu_exists(menu_id)
