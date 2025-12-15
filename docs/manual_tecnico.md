# 📘 Manual Técnico  
**HelpDesk Web Application – COMP 2053**

## 1. Introducción
Este documento describe la arquitectura técnica, estructura del código y funcionamiento interno de la aplicación web **HelpDesk**, desarrollada como proyecto final del curso COMP 2053.

El objetivo es que cualquier desarrollador o evaluador pueda comprender, instalar y mantener el sistema.

---

## 2. Arquitectura General
La aplicación utiliza una arquitectura MVC simplificada:

- Vista: HTML, Bootstrap, Jinja2  
- Controlador: Flask (Python)  
- Modelo: MariaDB  
- Interactividad: jQuery + AJAX  
- Seguridad: Werkzeug

---

## 3. Estructura del Proyecto

helpdesk_app/
├── app.py
├── schema.sql
├── requirements.txt
├── README.md
├── templates/
├── static/
├── docs/
└── venv/

---

## 4. Base de Datos
El sistema utiliza MariaDB con tres tablas principales:
- users
- tickets
- ticket_comments

La estructura completa se encuentra en `schema.sql`.

---

## 5. Seguridad
- Contraseñas hasheadas
- SQL parametrizado
- Control de acceso por roles
- Variables sensibles en `.env`

---

## 6. Roles del Sistema
- ADMIN
- AGENT
- USER
- INACTIVE (solo lectura)

---

## 7. Dashboard
El dashboard muestra estadísticas filtradas según el rol.

---

## 8. Tickets
Gestión completa de tickets con permisos por rol.

---

## 9. Comentarios AJAX
Comentarios dinámicos sin recargar la página.

---

## 10. Filtros y Búsqueda
Filtros por status, prioridad y búsqueda por título.

---

## 11. CSS Personalizado
Archivo `custom.css` para mejoras visuales.

---

## 12. Entorno Virtual
Uso de venv para manejo de dependencias.

---

## 13. Variables de Entorno
Configuradas mediante `.env`.

---

## 14. Conclusión
Proyecto completo y funcional con mejoras adicionales.

---

## 15. Autor
Estudiante de Bachillerato en Ciencias de Computadoras  
Curso COMP 2053
