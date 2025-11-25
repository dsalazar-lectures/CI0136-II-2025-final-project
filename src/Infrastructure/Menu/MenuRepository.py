from src.Model.Menu.Menu import Menu
from src.Model.Menu.MenuDay import MenuDay
from src.Database.Menu.MenuCSV import MenuCSV
from src.Application.Menu.IMenuRepository import IMenuRepository
from src.Shared.Logs.custom_logger import CustomLogger

logger = CustomLogger()


class MenuRepository(IMenuRepository):
    def __init__(self, csv_file_path="src/Database/Menu/menus.csv"):
        self.menu_csv = MenuCSV(csv_file_path)

    def get_menu_by_id(self, menu_id: int) -> Menu:
        db_menu = self.menu_csv.get_menu_by_id(menu_id)
        if db_menu:
            logger.log(
                level="info",
                user="system",
                role="-",
                action="Get menu",
                id_object=str(menu_id),
                description=f"Menu {menu_id} retrieved successfully",
            )
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
        logger.log(
            level="warning",
            user="system",
            role="-",
            action="Get menu",
            id_object=str(menu_id),
            description=f"Menu {menu_id} not found",
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
        logger.log(
            level="info",
            user="system",
            role="-",
            action="Create menu",
            id_object=str(menu.menu_id),
            description=f"Menu {menu.menu_id} created successfully with {len(daily_menus)} days",
        )
        return menu, "Menu created successfully", 201

    def delete_menu(self, menu_id: int):
        if not self.menu_exists(menu_id):
            logger.log(
                level="warning",
                user="system",
                role="-",
                action="Delete menu",
                id_object=str(menu_id),
                description=f"Menu {menu_id} does not exist",
            )
            return None, "Menu does not exist", 404
        self.menu_csv.delete_menu(menu_id)
        logger.log(
            level="info",
            user="system",
            role="-",
            action="Delete menu",
            id_object=str(menu_id),
            description=f"Menu {menu_id} deleted successfully",
        )
        return True, "Menu deleted successfully", 200

    def list_menus(self) -> list:
        return self.menu_csv.list_menus()

    def menu_exists(self, menu_id: int) -> bool:
        return self.menu_csv.menu_exists(menu_id)
