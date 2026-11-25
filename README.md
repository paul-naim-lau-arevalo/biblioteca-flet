# Programación III - Sistema de Control de Biblioteca

## Proyecto grupal: Biblioteca con Python y Flet

En este repositorio estaremos trabajando en un sistema sencillo para llevar el control de los libros, usuarios y préstamos de una biblioteca.

Para esto utilizamos Python, clases, listas y Flet, que nos permite crear la interfaz gráfica del programa.

## ¿Cómo funciona?

El programa cuenta con tres pestañas:

- Ingreso de libros: permite registrar y eliminar libros, además de consultar si están disponibles.
- Ingreso de usuarios: permite registrar y eliminar los usuarios de la biblioteca.
- Préstamos y devoluciones: permite prestar un libro disponible a un usuario y registrar su devolución.

Los datos se guardan en listas mientras el programa está abierto. Al cerrarlo, se pierden los registros de la sesión.

El programa comprueba que no se repitan los códigos de los libros ni las cédulas de los usuarios. Tampoco permite prestar un libro que ya está prestado o eliminar registros asociados a un préstamo activo.

## ¿Cómo ejecutarlo?

Desde la terminal, con Python 3.10 o superior:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flet run main.py
```

En Windows, para activar el entorno desde CMD, utilizar `.venv\Scripts\activate.bat` en lugar de `source .venv/bin/activate`.

También podemos abrir el programa en el navegador con `flet run --web main.py`.

## Archivos del programa

- `main.py`: ventana principal.
- `biblioteca.py`: clases y funciones para manejar los datos.
- `IngresoLibro.py`: registro de libros.
- `IngresoUsuario.py`: registro de usuarios.
- `PrestamoLibro.py`: préstamos y devoluciones.

## Pruebas

Para comprobar la lógica del programa:

`python -m unittest discover -s tests -v`

## Trabajo en equipo

Cada integrante puede realizar sus aportes al programa y compartirlos mediante GitHub para que podamos revisar e integrar los cambios.

**Materia:** Programación III  
**Universidad:** Universidad Interamericana de Panamá
