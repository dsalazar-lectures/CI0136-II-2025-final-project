# Patrón Adapter – Ingredientes Locos
## 1. Patrón Aplicado

| Título del Patrón | Funcionalidad que lo usa |
| :--- | :--- |
| *Patrón Adapter* (Adaptador)| *Ingredientes.* Integración con proveedores externos de ingredientes. Permite convertir modelos externos al modelo interno sin modificar la lógica existente. |

## 2. Descripción y Motivación de Uso
### Descripción del Patrón
El Patrón Adapter permite que dos interfaces incompatibles trabajen juntas. Su objetivo es tomar una interfaz externa (por ejemplo, la respuesta de una API) y adaptarla a la interfaz interna que el sistema espera, sin alterar el código que consume dicha interfaz.

En nuestra implementación se tienen:

* *Interfaz Objetivo:* ```IExternalIngredientProvider```, utilizada por casos de uso para obtener ingredientes de proveedores externos.

* *Cliente:* La capa de aplicación (principalmente ```IngredientUseCase```), que espera proveedores con una API uniforme.

* *Adaptadores Concretos:* Clases como ```SpoonacularIngredientAdapter``` que traducen datos externos a las entidades internas (```Ingredient```, ```BaseIngredient```, ```CompositeIngredient```).

### Motivación de Uso

La integración con servicios externos supone un problema común: cada proveedor tiene su propio formato de datos, nombres de campos y estructuras de anidación distintas. Sin un Adapter, la aplicación tendría que incluir lógica condicional, validaciones repetidas y transformaciones manuales en sus casos de uso.

El patrón Adapter aporta las siguientes ventajas:

* *Desacacoplamiento:*
```IngredientUseCase``` no depende del formato específico de Spoonacular u otros proveedores.

* *Compatibilidad sin modificar código existente:*
Se pueden agregar nuevos proveedores implementando la misma interfaz sin tocar la lógica del dominio.

* *Testeo simplificado:*
El Adapter puede ser fácilmente moqueado implementando ```IExternalIngredientProvider```.

## 3. Explicación de la Implementación

La implementación propuesta se estructura en tres partes:

### 3.1. IExternalIngredientProvider (Interfaz Objetivo)

Define la API interna que cualquier proveedor externo debe implementar:

#### Métodos:
- ```get_ingredient_by_name()```
- ```get_ingredient_by_id()```
- ```get_ingredients_by_category()```
Todos retornan entidades internas del sistema (Ingredient o listas de ingredientes).

**Rol:** Es la interfaz esperada por ```IngredientUseCase```.

### 3.2. SpoonacularAdapter (Adaptador Concreto)

*Implementa la interfaz objetivo traduciendo datos del proveedor externo al modelo interno:*

* Contiene una referencia al cliente externo (```external_client```).

* Llama a métodos externos como ```search_ingredients(name)```.

* Convierte la respuesta en ```Ingredient```, ```BaseIngredient``` o ```CompositeIngredient```.

* Oculta formatos externos (nombres de campos, estructuras, tipos).

**Ejemplo simplificado:**
```python

class SpoonacularIngredientAdapter(IExternalIngredientProvider):
    def __init__(self, external_client):
        self.client = external_client

    def get_ingredient_by_name(self, name: str) -> List[Ingredient]:
        external_results = self.client.search_ingredients(name)
        adapted = []
        for r in external_results:
            adapted.append(
                Ingredient(
                    id=r.get('id'),
                    name=r.get('name'),
                    categories=r.get('categories', []),
                    substitutes=r.get('substitutes', []),
                    recipe_count=r.get('recipe_count', 0)
                )
            )
        return adapted
    
    def get_ingredient_by_id(self, ingredient_id: int):
        external = self.client.get_ingredient(ingredient_id)
        if not external:
            return None
        return Ingredient(
            id=external.get("id"),
            name=external.get("name"),
            categories=external.get("categoryList", []),
            substitutes=external.get("substitutes", []),
            components=external.get("components", []),
            recipe_count=external.get("recipes", 0),
        )

    def get_ingredients_by_category(self, category: str):
        external_list = self.client.search_by_category(category)
        return [self._adapt_item(item) for item in external_list]

```
### 3.3. Inyección del Adaptador (Registro / Injector)

La clase ```IngredientInjector``` se encarga de registrar y entregar el adaptador correcto para el caso de uso:

* Permite cambiar proveedores sin modificar el caso de uso.

* Favorece la inversión de dependencias.

* Centraliza la configuración del adaptador.

## 4. Integración con el Caso de Uso

```IngredientUseCase``` recibe una implementación de ```IExternalIngredientProvider```.

Flujo típico:

* El cliente solicita un ingrediente por nombre.

* ```IngredientUseCase``` busca primero en el repositorio interno.

* Si no existe, consulta el proveedor externo usando el adaptador.

* El adaptador traduce la respuesta al modelo interno.

Este flujo permite combinar repositorios locales con datos externos sin mezclar responsabilidades.

## 5. Guía de Extensión y Reutilización

El diseño del Patrón Adapter facilita integrar nuevos proveedores manteniendo el Principio Open-Close: se añaden nuevas clases sin modificar las existentes.

### 5.1. Extender con Nuevos Proveedores Externos

Para añadir un nuevo proveedor:

* Crear un nuevo adaptador que implemente ```IExternalIngredientProvider```.

* Mapear las propiedades del proveedor al modelo interno ```Ingredient```.

* Registrar el adaptador en el ```Injector```.