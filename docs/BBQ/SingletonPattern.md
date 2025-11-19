## Custom Logger y Patrón Singleton

## **Funcionalidad que usa el patrón**

La clase `CustomLogger` implementa un **sistema de auditoría y registro de eventos** que permite enviar mensajes de log hacia múltiples destinos.

Esta arquitectura usa el **patrón de diseño Singleton** para asegurar que solo exista **una única instancia** de la clase `CustomLogger` en toda la aplicación, proporcionando un punto de acceso global y consistente para todas las operaciones de registro.

---

## **Descripción del patrón**

El patrón **Singleton** (Instancia Única) restringe la instanciación de una clase a un solo objeto. Es útil cuando se necesita exactamente un objeto para coordinar acciones en todo el sistema.

En este contexto:

- **Instancia Única:** el `CustomLogger`, que centraliza la configuración de _logging_ (niveles, _handlers_) y actúa como el único punto de publicación de eventos.

---

## **Motivación de uso**

El patrón Singleton fue elegido para:

- **Garantizar la unicidad:** Asegura que todos los componentes de la aplicación utilicen la **misma configuración de registro** y el mismo conjunto de _handlers_ (destinos de log).
- **Control de Recursos:** Evita la creación redundante de objetos `logging.Logger` y _handlers_ potencialmente costosos, optimizando el uso de recursos como conexiones de archivo o de red.
- **Punto de Acceso Global:** Proporciona un **punto de acceso conocido** para el sistema de _logging_, facilitando el uso del logger en cualquier parte del código sin tener que pasarlo como argumento.
- **Principio DRY (Don't Repeat Yourself):** Centraliza la lógica de inicialización en la clase misma.

---

## **Explicación de la implementación**

1.  **Implementación de Singleton ($\_\_new\_\_$)**
    La lógica para asegurar una única instancia reside en el método especial `__new__`:

    - Se verifica si ya existe una instancia (`_instance = None`).
    - Si no existe, se llama al constructor de la clase base y se almacena la nueva instancia en `_instance`.
    - Se genera un identificador único (`_instance_id`) para confirmar la inicialización.
    - Si ya existe, simplemente se devuelve la instancia existente.

2.  **Inicialización Controlada ($\_\_init\_\_$)**
    El método `__init__` incluye un _flag_ (`_initialized`) para asegurar que la lógica de configuración (establecer el nombre, nivel y agregar _handlers_) se ejecute **solo la primera vez** que se crea la instancia (en la primera llamada a `CustomLogger()`).

3.  **CustomLogger como Centralizador**

    - El constructor encapsula el `logging.Logger` estándar de Python.
    - El método `log()` acepta los campos del evento de auditoría y delega su procesamiento al `logging.Logger` subyacente, utilizando los _handlers_ configurados en la primera instanciación.

---

## **Guía para extender o reutilizar**

### **Para utilizar la instancia única:**

Debido a que el patrón Singleton está implementado en el método `__new__`, siempre se obtiene la misma instancia sin necesidad de pasarla o importarla de un módulo específico.

```python
# Primera llamada: inicializa el Singleton y ejecuta __init__
# Output: [INFO] Singleton CustomLogger inicializado con ID SID-XXXXXXXX
logger1 = CustomLogger(name="AppLogger", handlers=[...])

# Segunda llamada: devuelve la misma instancia de logger1
# No se ejecuta __init__ de nuevo, no se muestra el mensaje de inicialización
logger2 = CustomLogger()

# logger1 y logger2 son la misma instancia
print(logger1 is logger2)  # True
```

En el proyecto, el logger se instancia al iniciar la aplicación en `app.py`. De este modo, sólo es necesario importar `CustomLogger` y realizar `logger = CustomLogger()`.

### **Para agregar un nuevo destino de log (Handler):**

1.  Crear una nueva clase que herede de `logging.Handler`.
2.  Implementar el método `emit(self, record: logging.LogRecord)` para definir el comportamiento del nuevo destino.

**El nuevo _handler_ debe pasarse en la PRIMERA llamada al constructor:**

```python
import logging
from custom_logger import CustomLogger

class DatabaseHandler(logging.Handler):
    # Lógica para escribir el evento en una Base de Datos
    def emit(self, record):
        print(f"[{record.levelname}] Escribiendo en DB: {getattr(record, 'action', '-')}")

# Primer y Único lugar donde se configura el Logger
first_logger = CustomLogger(
    name="AuditLogger",
    handlers=[DatabaseHandler()], # Pasar todos los handlers aquí
    level=logging.DEBUG
)

# Uso del Singleton en cualquier otro lugar del código
# Simplemente se llama al constructor. Se obtendrá la instancia ya configurada.
other_module_logger = CustomLogger()

other_module_logger.log(
    level="INFO",
    user="ServiceAccount",
    role="System",
    action="MaintenanceTask",
    description="Daily cleanup completed.",
)
```

---

## **Ejemplo rápido de uso (como Singleton)**

```python
from src.Shared.Logs.custom_logger import CustomLogger

# 1. Configurar el Singleton (normalmente en el punto de entrada de la aplicación)
# El logger está configurado con handlers si se le pasan aquí.
logger_config = CustomLogger("AuditLogger", handlers=[...]) # Añadir handlers reales

# 2. Obtener la misma instancia en cualquier otra parte del código
logger_in_module = CustomLogger()

logger_in_module.log(
    level="INFO",
    user="Alice",
    role="Admin",
    action="create_user",
    id_object=201,
    description="User created successfully"
)

# El output de la consola/archivos de log reflejará el evento.
```

En general, para iplementar los logs a lo largo de la arquitectura, sólo es necesario importar `CustomLogger` y realizar el paso 2 del ejemplo anterior.
