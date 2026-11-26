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
            primary="#80594F",
            on_primary="#FFFFFF",
            surface="#F8F2E9",
            on_surface="#321813",
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

    # ---------- Dashboard ----------
    def crear_tarjeta(icono, titulo, valor, subtitulo, color):
        texto_valor = ft.Text(
            str(valor),
            size=32,
            weight=ft.FontWeight.BOLD,
            color="#FFFFFF",
        )
        tarjeta = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icono, size=40, color="#FFFFFF"),
                    ft.Column(
                        controls=[
                            ft.Text(titulo, size=16, color="#FFFFFF"),
                            texto_valor,
                            ft.Text(subtitulo, size=11, color="#F8F2E9"),
                        ],
                        spacing=3,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            bgcolor=color,
            padding=20,
            border_radius=15,
            width=350,
        )
        return tarjeta, texto_valor

    tarjeta_libros, numero_libros = crear_tarjeta(
        ft.Icons.MENU_BOOK,
        "Libros Registrados",
        len(biblioteca.libros),
        "Total en el catálogo",
        "#654038",
    )
    tarjeta_clientes, numero_clientes = crear_tarjeta(
        ft.Icons.PEOPLE,
        "Clientes Registrados",
        len(biblioteca.clientes),
        "Miembros de la biblioteca",
        "#B18B58",
    )
    tarjeta_prestamos, numero_prestamos = crear_tarjeta(
        ft.Icons.BOOK,
        "Préstamos Activos",
        len(biblioteca.prestamos),
        "Libros pendientes de devolución",
        "#80594F",
    )

    dashboard = ft.Row(
        controls=[tarjeta_libros, tarjeta_clientes, tarjeta_prestamos],
        alignment=ft.MainAxisAlignment.CENTER,
        wrap=True,
        spacing=15,
        run_spacing=15,
    )

    def actualizar_dashboard():
        numero_libros.value = str(len(biblioteca.libros))
        numero_clientes.value = str(len(biblioteca.clientes))
        numero_prestamos.value = str(len(biblioteca.prestamos))

    def actualizar_datos():
        vista_libros.refrescar()
        actualizar_dashboard()
        page.update()

    # Actualizar datos después de prestar o devolver
    vista_prestamos.al_cambiar = actualizar_datos

    def cambio_de_pestana(e):
        for vista in (vista_libros, vista_usuarios, vista_prestamos):
            vista.refrescar()

        actualizar_dashboard()
        page.update()

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
                        ft.Tab(label="Préstamos y Devoluciones

