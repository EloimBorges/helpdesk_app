🛠️ HelpDesk Web Application
Proyecto Final – COMP 2053

📌 Descripción general

Este proyecto consiste en una aplicación web de Help Desk desarrollada con Flask, MariaDB, Bootstrap y jQuery, cuyo propósito es permitir la gestión de tickets de soporte técnico dentro de una organización.

La aplicación implementa autenticación, roles de usuario, control de acceso, comentarios dinámicos con AJAX, filtros avanzados, y una mejora adicional personalizada mediante un rol especial (INACTIVE).

El proyecto fue desarrollado siguiendo buenas prácticas de seguridad, organización del código y manejo de dependencias mediante un entorno virtual (venv).



🧱 Tecnologías utilizadas

Backend: Python, Flask
Base de datos: MariaDB
Frontend: HTML5, Bootstrap 5
Interactividad: jQuery + AJAX
Seguridad: Hash de contraseñas con Werkzeug
Entorno virtual: venv
Control de versiones: Git & GitHub



🧑‍💻 Roles del sistema

El sistema implementa control de acceso basado en roles:

🔑 ADMIN

Acceso total al sistema
Puede:
     Crear y administrar usuarios
     Asignar tickets
     Cambiar estados
     Ver todos los tickets
     Acceder a estadísticas completas

🧑‍🔧 AGENT

Usuario de soporte
Puede:
     Ver tickets asignados o sin asignar
     Cambiar estado de tickets
     Añadir comentarios

👤 USER

Usuario regular
Puede:
     Crear tickets
     Ver solo los tickets creados por él
     Comentar sus tickets

🚫 INACTIVE (Mejora adicional)

Rol especial de solo lectura
Puede:
     Ver únicamente tickets RESOLVED asignados previamente a él

No puede:
     Crear tickets
     Comentar
     Actualizar tickets
     El dashboard muestra estadísticas restringidas
     Implementado como optimización extra del proyecto



🗄️ Base de datos

La estructura de la base de datos se encuentra en el archivo schema.sql



🔐 Seguridad implementada

Contraseñas nunca se almacenan en texto plano

Uso de:
generate_password_hash()
check_password_hash()
Queries SQL parametrizadas (prevención de SQL Injection)

Rutas protegidas con:
login_required
role_required

Ruta de creación de admin protegida y deshabilitable en producción
Variables sensibles almacenadas en .env (no subido al repositorio)



📦 Dependencias principales
     Flask
     PyMySQL
     python-dotenv
     Werkzeug



🧪 Flujo de uso básico

1.Login al sistema
2.Acceso al dashboard según rol
3.Gestión de tickets
4.Comentarios dinámicos
5.Administración de usuarios (ADMIN)
6.Visualización restringida (INACTIVE)




📈 Comentarios finales sobre el proceso

Este proyecto permitió integrar múltiples conceptos aprendidos durante el curso, incluyendo:

     Desarrollo backend con Flask
     Manejo de bases de datos relacionales
     Seguridad básica en aplicaciones web
     Interactividad con AJAX
     Organización profesional de un proyecto
     Uso correcto de entornos virtuales

La implementación del rol INACTIVE y los filtros dinámicos representan mejoras adicionales que van más allá de los requisitos mínimos del proyecto.





👨‍🎓 Autor

Eloim N. Borges Millete
Estudiante de Bachillerato en Ciencias de Computadoras
Universidad Interamericana recinto de Arecibo