from src.Model.Menu.MenuDay import MenuDay


class Menu:
    def __init__(
        self,
        menu_id: int,
        daily_menus: dict[int, MenuDay],
    ):
        self.menu_id = menu_id
        self.daily_menus = daily_menus

    def to_dict(self):
        return {
            "menu_id": self.menu_id,
            "daily_menus": {
                day: menu_day.to_dict() for day, menu_day in self.daily_menus.items()
            },
        }
