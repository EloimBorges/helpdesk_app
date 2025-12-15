# 📗 Manual de Usuario  
**HelpDesk Web Application – COMP 2053**

---

## 1. Introducción

Este manual de usuario describe cómo utilizar la aplicación web **HelpDesk**, diseñada para gestionar solicitudes de soporte técnico (tickets) dentro de una organización.

El sistema cuenta con distintos tipos de usuarios, cada uno con permisos específicos.

---

## 2. Acceso al Sistema

### Inicio de Sesión
1. Acceda a la página principal del sistema.
2. Ingrese su **correo electrónico** y **contraseña**.
3. Presione el botón **Login**.

Si las credenciales son correctas, será redirigido al **Dashboard**.

---

## 3. Dashboard

El dashboard muestra un resumen general de los tickets según el rol del usuario:

- Total de tickets
- Tickets abiertos (OPEN)
- Tickets en progreso (IN_PROGRESS)
- Tickets cerrados (RESOLVED)

⚠️ Los datos mostrados dependen del rol asignado.

---

## 4. Roles de Usuario

### 👑 ADMIN
El administrador tiene acceso total al sistema:
- Crear y administrar usuarios
- Asignar tickets
- Cambiar estados de tickets
- Ver todos los tickets
- Acceder a estadísticas completas

---

### 🧑‍🔧 AGENT
Usuario de soporte técnico:
- Ver tickets asignados o sin asignar
- Cambiar estado de tickets
- Añadir comentarios a los tickets

---

### 👤 USER
Usuario regular:
- Crear tickets
- Ver solo los tickets creados por él
- Añadir comentarios a sus tickets

---

### 🚫 INACTIVE
Usuario con acceso limitado:
- Puede ver **únicamente tickets cerrados (RESOLVED)** que estuvieron asignados a él
- No puede crear tickets
- No puede comentar ni modificar tickets

---

## 5. Gestión de Tickets

### Crear Ticket
*(Disponible para USER y ADMIN)*
1. Seleccione **Crear Ticket**
2. Complete el formulario:
   - Título
   - Descripción
   - Prioridad
3. Presione **Guardar**

---

### Ver Tickets
- Acceda a la sección **Tickets**
- El listado se filtra automáticamente según su rol

---

### Filtros y Búsqueda
En la página de tickets puede:
- Filtrar por **Status**
- Filtrar por **Prioridad**
- Buscar por **título**
- Restablecer filtros con el botón **Reset**

Los resultados se actualizan automáticamente.

---

## 6. Detalle del Ticket

Al seleccionar un ticket podrá:
- Ver la descripción completa
- Ver su estado y prioridad
- Ver a quién está asignado
- Leer los comentarios asociados

### Actualizar Ticket
*(Solo ADMIN y AGENT)*
- Cambiar el estado
- Asignar el ticket a un agente

---

## 7. Comentarios

- Los comentarios se pueden añadir desde el detalle del ticket
- Se envían sin recargar la página (AJAX)
- Cada comentario muestra:
  - Usuario
  - Fecha
  - Contenido

⚠️ Usuarios INACTIVE no pueden comentar.

---

## 8. Administración de Usuarios (ADMIN)

El administrador puede:
- Crear nuevos usuarios
- Asignar roles
- Cambiar roles existentes

Los cambios se aplican inmediatamente.

---

## 9. Cerrar Sesión

Para salir del sistema:
1. Presione **Logout** en la barra superior
2. Será redirigido a la pantalla de inicio de sesión

---

## 10. Consideraciones Finales

- El sistema adapta sus funciones según el rol del usuario
- Las acciones no permitidas se bloquean automáticamente
- El rol INACTIVE fue implementado como una mejora adicional del sistema

---

## 11. Autor

Estudiante de Bachillerato en Ciencias de Computadoras  
Curso COMP 2053
