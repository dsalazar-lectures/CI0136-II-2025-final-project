from src.Model.Menu.Menu import Menu
from src.Model.Menu.MenuDay import MenuDay
from src.Database.Menu.MenuCSV import MenuCSV
from src.Application.Menu.IMenuRepository import IMenuRepository


class MenuRepository(IMenuRepository):
    def __init__(self, csv_file_path="src/Database/Menu/menus.csv"):
        self.menu_csv = MenuCSV(csv_file_path)

    def get_menu_by_id(self, menu_id: int) -> Menu:
        db_menu = self.menu_csv.get_menu_by_id(menu_id)
        if db_menu:
            # Convert dictionary daily_menus to MenuDay objects
            daily_menus = {
                day: MenuDay(
                    breakfast_recipe_id=menu_day_data["breakfast_recipe_id"],
                    lunch_recipe_id=menu_day_data["lunch_recipe_id"],
                    dinner_recipe_id=menu_day_data["dinner_recipe_id"],
                    dessert_recipe_id=menu_day_data["dessert_recipe_id"],
                )
                for day, menu_day_data in db_menu["daily_menus"].items()
            }
            return Menu(
                menu_id=int(db_menu["menu_id"]),
                daily_menus=daily_menus,
            )
        return None

    def create_menu(self, menu_data):
        created_menu = self.menu_csv.create_menu(menu_data)
        # Convert dictionary daily_menus to MenuDay objects
        daily_menus = {
            day: MenuDay(
                breakfast_recipe_id=menu_day.breakfast,
                lunch_recipe_id=menu_day.lunch,
                dinner_recipe_id=menu_day.dinner,
                dessert_recipe_id=menu_day.dessert,
            )
            for day, menu_day in created_menu["daily_menus"].items()
        }
        menu = Menu(
            menu_id=int(created_menu["menu_id"]),
            daily_menus=daily_menus,
        )
        return menu, "Menu created successfully", 201

    # TODO(JM): Implement CSV functions
    def delete_menu(self, menu_id: int) -> bool:
        if not self.menu_exists(menu_id):
            return None, "Menu does not exist", 404
        return self.menu_csv.delete_menu(menu_id)

    def list_menus(self) -> list:
        return self.menu_csv.list_menus()

    def menu_exists(self, menu_id: int) -> bool:
        return self.menu_csv.menu_exists(menu_id)
