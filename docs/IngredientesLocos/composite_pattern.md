# Patrón Composite - Ingredientes Locos

## 1. Patrón Aplicado

| Título del Patrón | Funcionalidad que lo usa |
| :--- | :--- |
| *Patrón Composite* (Compuesto) | *Ingredientes.* Permite tratar ingredientes simples y compuestos de la misma forma. |

## 2. Descripción y Motivación de Uso

### Descripción del Patrón

El Patrón Composite permite componer objetos en estructuras de árbol para representar jerarquías. El objetivo es que el código que utiliza estos objetos pueda tratar a los objetos base (*hojas*) y a los objetos compuestos (*ramas*) de manera uniforme a través de una interfaz común (*Componente*).

En nuestra implementación se tienen:
* *Componente Base:* La clase abstracta *Ingredient*, de la cual heredan las otras dos clases de Ingrediente.
* *Hoja:* La clase concreta *BaseIngredient* (ingrediente elemental que no está compuesto de otros ingredientes).
* *Rama:* La clase concreta *CompositeIngredient* (ingrediente compuesto por otros ingredientes).

### Motivación de Uso

La naturaleza de los ingredientes en una aplicación de recetas es recursiva: un ingrediente puede ser elemental o estar compuesto por otros ingredientes, que a su vez pueden ser compuestos.

La implementación de Composite tiene las siguientes ventajas:
1.  *Uniformidad:* Permite que el repositorio (**IngredientRepository**) y los casos de uso (**IngredientUseCase**) interactúen con cualquier tipo de ingrediente usando solo los métodos definidos en la interfaz Ingredient (ej: to_json(), is_base_ingredient()), eliminando la necesidad de lógica condicional compleja.
2.  *Transparencia:* El cliente (la capa de aplicación) no necesita saber si está trabajando con una hoja o una rama, simplificando la lógica de la aplicación.

## 3. Explicación de la Implementación

La implementación se estructura en tres partes:

### 3.1. Ingredient (Componente)

La clase base que define la interfaz común:

* *Propiedades:* id, name, categories, substitutes, recipe_count. No se incluyen los componentes, ya que los BaseIngredient no tienen los tienen.
* *Métodos Comunes:* \_\_str__, _format_fields(), add_recipe(), has_substitutes(), update_categories(), update_substitutes().
* *Métodos Abstractos:* is_base_ingredient() y to_json() (deben ser implementados por las subclases).

### 3.2. BaseIngredient (Hoja)

Implementa la funcionalidad de un ingrediente simple, es decir, que no está compuesto por otros ingredientes (ej: Azúcar, Huevo):

* Hereda de Ingredient.
* Retorna *True* en is_base_ingredient().
* Retorna el diccionario de to_json() con el tipo *base* y sin la sección de componentes.

### 3.3. CompositeIngredient (Compuesto)

Implementa la funcionalidad de un ingrediente que contiene otros ingredientes (ej: Mermelada):

* Hereda de Ingredient.
* Contiene la lista *self.components: List[str]* que almacena sus sub-ingredientes (Composición/Agregación).
* Retorna *False* en is_base_ingredient().
* Retorna el diccionario de to_json() con el tipo *composite* y con una sección de componentes.
* Incluye métodos para gestionar la lista de componentes (ej: update_components()).

## 4. Guía de Extensión y Reutilización

El diseño del Patrón Composite facilita la extensión sin modificar la base del código (Principio **Open-Close**).

### 4.1. Extender con Nuevos Tipos de Ingredientes Base

Si se necesita un ingrediente simple con propiedades adicionales se puede:

1.  *Crear una nueva clase* que herede directamente de *Ingredient*.
2.  *Añadir el nuevo atributo* en el constructor __init__.
3.  *Implementar los métodos abstractos* (is_base_ingredient retorna True, y to_json incluye la nueva propiedad).
4.  El nuevo tipo de ingrediente es accedido a través de la misma interfaz **Ingredient**.

### 4.2. Extender la Funcionalidad de Ingredientes Compuestos

Para añadir funcionalidad específica a los compuestos (como buscar todos los ingredientes base de un ingrediente):

1.  *Añadir el nuevo método* (get_base_ingredients) a la clase *CompositeIngredient*.
2.  Este método puede iterar sobre la lista *self.components* y hacer llamados recursivamente hasta obtener todos los ingredientes base.
