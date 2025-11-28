# Chain Of Responsibility — Customized Menu (src/Application/Menu)

## Resumen

- Implementación del patrón Chain of Responsibility para filtrar, ordenar y limitar recetas cuando se construye un menú personalizado.

## Arquitectura y responsabilidades

- `MenuContext`: objeto de contexto que contiene parámetros de la petición (favoritos, categoría, límite, modo `require_all`).
- `MenuHandler` (abstracto): base del *chain*. Provee `set_next()` para encadenar y `run()` que aplica `handle()` y delega al siguiente handler.
- Handlers concretos:
  - `FavoritesFilterHandler`: filtra recetas por ingredientes favoritos (OR/AND según `require_all`). Si no hay favoritos, devuelve lista vacía.
  - `CategoryFilterHandler`: filtra por categoría (normaliza y hace match exacto entre categorías de la receta y la categoría solicitada).
  - `ScoreAndSortHandler`: calcula una puntuación por coincidencias de ingredientes favoritos y ordena por (score desc, rating desc, title asc).
  - `LimitHandler`: recorta la lista al `limit` indicado.

## Dónde se arma la cadena

- `src/Application/Menu/CustomizedMenuService.py` crea la cadena y guarda una referencia al head:

```py
self._chain = (
    FavoritesFilterHandler()
    .set_next(CategoryFilterHandler())
    .set_next(ScoreAndSortHandler())
    .set_next(LimitHandler())
)

# head usado para ejecutar
self._head = FavoritesFilterHandler()
self._head.set_next(CategoryFilterHandler()).set_next(
    ScoreAndSortHandler()
).set_next(LimitHandler())
```

Nota: la implementación crea instancias tanto en `_chain` como en `_head`; el servicio usa `_head.run(all_recipes, ctx)` para ejecutar la cadena.

## Flujo de ejecución (alto nivel)

1. `CustomizedMenuService.recommend_by_favorites(...)` normaliza `favorites` y la `category` y construye un `MenuContext`.
2. Obtiene `all_recipes` desde `recipe_service.get_all_recipes()`.
3. Llama a `self._head.run(all_recipes, ctx)`.
4. Cada handler en la cadena recibe la lista resultante del anterior y aplica su lógica de `handle()`.
5. Resultado final: lista filtrada, ordenada y limitada de recetas.

## Detalles de implementación importantes

- Normalización: `_norm()` convierte texto a minúsculas y reemplaza `-` por espacio antes de comparar.
- `FavoritesFilterHandler`:
  - Si `ctx.favorites` está vacío devuelve `[]` (esto hace que no se recomienden recetas cuando no hay favoritos).
  - Si `ctx.require_all` es True exige que la receta contenga todos los ingredientes favoritos (AND), en otro caso requiere cualquiera (OR).
- `CategoryFilterHandler`: realiza matching exacto sobre categorías normalizadas.
- `ScoreAndSortHandler`: calcula `score` contando coincidencias por ingrediente favorito y ordena con tiebreakers.
- `LimitHandler`: devuelve `recipes[: max(ctx.limit, 0)]` (asegura límite no negativo).

## Cómo extender la cadena

- Crear un nuevo handler heredando `MenuHandler` e implementando `handle(self, recipes, ctx) -> list`.
- Añadirlo a la cadena en `CustomizedMenuService.__init__` usando `set_next()`.

Ejemplo de uso (desde el servicio)

```py
service = CustomizedMenuService()
recipes = service.recommend_by_favorites(favorites=['tomato','cheese'], category='almuerzo', limit=5)
```

## Pruebas y consejos

- Testear cada handler de forma aislada pasando una lista de recetas dummy (objetos con atributos `ingredients`, `categories`, `rating`, `title`).
- Testear la cadena completa verificando orden, filtros y límites.
- Cuidado con `FavoritesFilterHandler` — su comportamiento de devolver lista vacía si no hay favoritos es intencional; si quieres que la cadena ignore ese filtro en ausencia de favoritos, modifica `handle()` para `return recipes` cuando `favorites` esté vacío.

## Consideraciones de rendimiento

- `get_all_recipes()` trae todas las recetas en memoria antes de filtrar. Si la colección crece mucho, considera streams/paginación o filtros en la capa de repositorio para reducir carga.

## Resumen rápido (qué modificar si se quiere otra política)

- OR vs AND: `require_all` en `MenuContext` controla la lógica de `FavoritesFilterHandler`.
- Si deseas que la ausencia de favoritos signifique "no filtro" (en lugar de lista vacía), cambia el early-return en `FavoritesFilterHandler.handle()`.
- Para añadir un nuevo criterio (p. ej. filtrar por tiempo de preparación), crea `PrepTimeFilterHandler` e insértalo antes de `ScoreAndSortHandler`.

## Archivos clave

- `src/Application/Menu/CustomizedMenuHandlers.py` — implementación del chain y los handlers.
- `src/Application/Menu/CustomizedMenuService.py` — construcción del chain y punto de entrada `recommend_by_favorites`.
