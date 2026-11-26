import flet as ft

from biblioteca import Biblioteca
from IngresoLibro import VistaLibros
from IngresoUsuario import VistaUsuarios
from PrestamoLibro import VistaPrestamos


def main(page: ft.Page):
    page.title = "Sistema de Control de Biblioteca"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F8F2E9"
    page.theme = ft.Theme(
        color_scheme_seed="#80594F",
        color_scheme=ft.ColorScheme(
            primary="#80594F", on_primary="#FFFFFF",
            surface="#F8F2E9", on_surface="#321813",
            outline="#B18B58",
        ),
        divider_color="#B18B58",
    )
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
                    label_color="#654038",
                    unselected_label_color="#321813",
                    indicator_color="#80594F",
                    divider_color="#B18B58",
                    tabs=[
                        ft.Tab(label="Ingreso de Libros"),
                        ft.Tab(label="Ingreso de Usuarios"),
                        ft.Tab(label="Préstamos y Devoluciones"),
                    ]
                ),
                ft.TabBarView(
                    expand=True,
                    controls=[
                        ft.Container(
                            content=vista_libros,
                            bgcolor="#EADCC8",
                            padding=20,
                            border_radius=12,
                            border=ft.Border.all(1, "#C3A174"),
                        ),
                        ft.Container(
                            content=vista_usuarios,
                            bgcolor="#EADCC8",
                            padding=20,
                            border_radius=12,
                            border=ft.Border.all(1, "#C3A174"),
                        ),
                        ft.Container(
                            content=vista_prestamos,
                            bgcolor="#EADCC8",
                            padding=20,
                            border_radius=12,
                            border=ft.Border.all(1, "#C3A174"),
                        ),
                    ],
                ),
            ],
        ),
    )
    page.add(tabs)


if __name__ == "__main__":
    ft.run(main)
