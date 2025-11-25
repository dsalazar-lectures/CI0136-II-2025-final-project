from unittest.mock import MagicMock


class MockMenuRepository:
    def __init__(self):
        self.menus = {}
        self.next_id = 1

    def create_menu(self, menu):
        menu.menu_id = self.next_id
        self.menus[self.next_id] = menu
        self.next_id += 1
        mock_menu = MagicMock()
        mock_menu.menu_id = menu.menu_id
        return mock_menu, "Menu created successfully", 201

    def get_menu_by_id(self, menu_id):
        return self.menus.get(menu_id)

    def delete_menu(self, menu_id):
        if menu_id in self.menus:
            del self.menus[menu_id]
            return True, "Menu deleted successfully", 200
        return None, "Menu does not exist", 404

    def list_menus(self):
        return list(self.menus.values())

    def menu_exists(self, menu_id):
        return menu_id in self.menus
