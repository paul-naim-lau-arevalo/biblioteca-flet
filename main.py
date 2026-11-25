import flet as ft

from biblioteca import Biblioteca
from IngresoLibro import VistaLibros
from IngresoUsuario import VistaUsuarios
from PrestamoLibro import VistaPrestamos


def main(page: ft.Page):
    page.title = "Sistema de Control de Biblioteca"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    biblioteca = Biblioteca()

    def notificar(mensaje: str):
        page.show_dialog(ft.SnackBar(ft.Text(mensaje)))

    vista_libros = VistaLibros(biblioteca, notificar)
    vista_usuarios = VistaUsuarios(biblioteca, notificar)
    vista_prestamos = VistaPrestamos(biblioteca, notificar)

    # Actualizamos los libros después de un préstamo o devolución.
    vista_prestamos.al_cambiar = vista_libros.refrescar

    def cambio_de_pestana(e):
        # Actualizamos los datos al cambiar de pestaña.
        for vista in (vista_libros, vista_usuarios, vista_prestamos):
            vista.refrescar()

    tabs = ft.Tabs(
        length=3,
        selected_index=0,
        expand=True,
        on_change=cambio_de_pestana,
        content=ft.Column(
            expand=True,
            controls=[
                ft.TabBar(
                    tabs=[
                        ft.Tab(label="Ingreso de Libros"),
                        ft.Tab(label="Ingreso de Usuarios"),
                        ft.Tab(label="Préstamos y Devoluciones"),
                    ]
                ),
                ft.TabBarView(
                    expand=True,
                    controls=[vista_libros, vista_usuarios, vista_prestamos],
                ),
            ],
        ),
    )
    page.add(tabs)


if __name__ == "__main__":
    ft.run(main)
