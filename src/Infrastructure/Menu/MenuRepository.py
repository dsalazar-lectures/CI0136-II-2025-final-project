from src.Model.Menu.Menu import Menu
from src.Model.Menu.MenuDay import MenuDay
from src.Database.Menu.MenuCSV import MenuCSV
from src.Application.Menu.IMenuRepository import IMenuRepository


class MenuRepository(IMenuRepository):
    def __init__(
        self,
        csv_file_path="src/Database/Menu/menus.csv",
        custom_csv_file_path="src/Database/Menu/custom_menus.csv",
    ):
        self.menu_csv = MenuCSV(csv_file_path)
        # CSV for customized menus
        self.custom_menu_csv = MenuCSV(custom_csv_file_path)

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

    def create_customized_menu(self, recipes):
        """
        Save a customized set of recipes into the custom menus CSV and return
        a Menu object and status tuple.
        """
        menu_id = self.custom_menu_csv.save_customized(recipes, day=1)
        # Retrieve the saved menu and convert to Menu object
        db_menu = self.custom_menu_csv.get_menu_by_id(menu_id)
        if db_menu:
            daily_menus = {
                day: MenuDay(
                    breakfast_recipe_id=menu_day_data["breakfast_recipe_id"],
                    lunch_recipe_id=menu_day_data["lunch_recipe_id"],
                    dinner_recipe_id=menu_day_data["dinner_recipe_id"],
                    dessert_recipe_id=menu_day_data["dessert_recipe_id"],
                )
                for day, menu_day_data in db_menu["daily_menus"].items()
            }
            return (
                Menu(menu_id=int(db_menu["menu_id"]), daily_menus=daily_menus),
                "Customized menu created",
                201,
            )
        return None, "Error creating customized menu", 500

    def delete_menu(self, menu_id: int):
        # Try normal menus first
        if self.menu_csv.menu_exists(menu_id):
            self.menu_csv.delete_menu(menu_id)
            return True, "Menu deleted successfully", 200
        # Try custom menus
        if self.custom_menu_csv.menu_exists(menu_id):
            self.custom_menu_csv.delete_menu(menu_id)
            return True, "Customized menu deleted successfully", 200
        return None, "Menu does not exist", 404

    def list_menus(self) -> list:
        normal = self.menu_csv.list_menus()
        custom = self.custom_menu_csv.list_menus()
        # Tag menus with type
        for m in normal:
            m["menu_type"] = "normal"
        for m in custom:
            m["menu_type"] = "custom"
        return normal + custom

    def menu_exists(self, menu_id: int) -> bool:
        return self.menu_csv.menu_exists(menu_id) or self.custom_menu_csv.menu_exists(
            menu_id
        )
