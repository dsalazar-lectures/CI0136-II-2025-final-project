# src/Application/Menu/ICustomizedMenuService.py
from abc import ABC, abstractmethod
from typing import List, Optional, Any

LIMIT_OF_INGREDIENTS = 10


class ICustomizedMenuService(ABC):
    @abstractmethod
    def recommend_by_favorites(
        self,
        favorites: List[str] | str,
        category: Optional[str] = None,
        limit: int = LIMIT_OF_INGREDIENTS,
    ) -> List[Any]:
        pass
