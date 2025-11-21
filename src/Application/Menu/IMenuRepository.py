from abc import ABC, abstractmethod
from src.Model.Menu.Menu import Menu


class IMenuRepository(ABC):
    @abstractmethod
    def get_menu_by_id(self, menu_id: int) -> Menu:
        pass

    @abstractmethod
    def create_menu(self, menu: Menu):
        pass

    @abstractmethod
    def delete_menu(self, menu_id: int):
        pass

    @abstractmethod
    def list_menus(self) -> list:
        pass

    @abstractmethod
    def menu_exists(self, menu_id: int) -> bool:
        pass
