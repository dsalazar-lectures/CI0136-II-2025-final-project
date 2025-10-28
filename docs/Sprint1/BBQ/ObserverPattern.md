# Custom Logger y Patrón Observer

## **Funcionalidad que usa el patrón**

La clase `custom_logger.py` implementa un **sistema de auditoría y registro de eventos** que permite enviar mensajes de log hacia múltiples destinos simultáneamente (archivos JSON y texto plano por ahora).
Esta arquitectura usa el **patrón de diseño Observer** para desacoplar la generación de eventos de su procesamiento o almacenamiento.

---

## **Descripción del patrón**

El patrón **Observer** define una relación **uno a muchos** entre objetos.
Cuando un **Sujeto (Subject)** publica un evento, todos los **Observadores (Observers)** suscritos son notificados y reaccionan automáticamente, sin que el sujeto necesite conocer los detalles de cada uno.

En este contexto:

- **Sujeto:** el `CustomLogger`, que genera eventos de auditoría.
- **Observadores:** los distintos _handlers_ (`JsonFileHandler`, `TxtFileHandler`), que reciben el evento y lo procesan según su propósito.

---

## **Motivación de uso**

El patrón Observer fue elegido para:

- **Desacoplar** la lógica de negocio del manejo de logs.
- **Permitir múltiples salidas** de manera simultánea sin modificar el código que genera los eventos.
- **Facilitar la extensibilidad:** agregar un nuevo destino de registro (por ejemplo, una base de datos o servicio externo) no requiere modificar la clase principal.
- **Promover la reutilización:** los mismos handlers pueden usarse en otros módulos o proyectos.

Esto cumple con el principio **Open/Closed** — el sistema está _abierto a extensión pero cerrado a modificación_.

---

## **Explicación de la implementación**

1. **Estructura de datos común**
   La clase `AuditEvent` define los campos estándar (`user`, `role`, `action`, `id_object`, `description`) que se registran en cada evento.

2. **Handlers como Observadores**
   Cada clase derivada de `logging.Handler` implementa su método `emit()` para manejar el evento de forma distinta:

   - `JsonFileHandler`: escribe el evento en formato JSON.
   - `TxtFileHandler`: registra los eventos en texto plano con formato.

3. **CustomLogger como Sujeto (Publisher)**

   - Encapsula un `logging.Logger` estándar de Python.
   - Implmenta un método `log()` que acepta directamente los campos del evento.
   - Publica el evento y delega su procesamiento a los handlers conectados.

4. **Constructor de Handlers por defecto**
   La función `build_handlers()` crea una lista de handlers preconfigurados (JSON y TXT) que pueden pasarse al `CustomLogger` al instanciarlo.

---

## **Guía para extender o reutilizar**

### **Para agregar un nuevo destino de log:**

1. Crear una nueva clase que herede de `logging.Handler`.
2. Implementar el método `emit(self, record: logging.LogRecord)` para definir el comportamiento del nuevo destino.
3. Instanciar la clase y agregarla al `CustomLogger`, por ejemplo:

```python
class DummyHandler(logging.Handler):
    def emit(self, record):
        log_entry = {
            "timestamp": timestamp,
            "level": record.levelname,
            "user": getattr(record, "user", "-"),
            "role": getattr(record, "role", "-"),
            "action": getattr(record, "action", "-"),
            "id_object": getattr(record, "id_object", "-"),
            "description": getattr(record, "description", "-"),
        }
        print(log_entry)  # Lógica personalizada

new_handler = DummyHandler()
logger = CustomLogger("AuditLogger", handlers=[new_handler])
```

---

### **Ejemplo rápido de uso**

```python
import CustomLogger
import build_handlers

logger = CustomLogger("AuditLogger", handlers=build_handlers())

logger.info(
    user="Alice",
    role="Admin",
    action="create_user",
    id_object=201,
    description="User created successfully"
)
```

Genera simultáneamente registros en `ImportantLogs.json` y `GeneralLogs.txt`
