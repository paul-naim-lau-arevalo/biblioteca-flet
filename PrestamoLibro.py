# Préstamos y devoluciones
import flet as ft

from biblioteca import Biblioteca, BibliotecaError


class VistaPrestamos(ft.Column):
    def __init__(self, biblioteca: Biblioteca, notificar, al_cambiar=lambda: None):
        super().__init__(spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)
        self.biblioteca = biblioteca
        self.notificar = notificar
        self.al_cambiar = al_cambiar

        self.libro = ft.Dropdown(label="Libro disponible", expand=True, options=[])
        self.cliente = ft.Dropdown(label="Cliente", expand=True, options=[])
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Código")),
                ft.DataColumn(ft.Text("Libro")),
                ft.DataColumn(ft.Text("Cliente")),
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Fecha límite")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("")),
            ],
            rows=[],
        )
        self.controls = [
            ft.Text("Préstamos y Devoluciones", size=20, weight=ft.FontWeight.BOLD),
            ft.Row(
                [
                    self.libro,
                    self.cliente,
                    ft.FilledButton("Prestar", icon=ft.Icons.BOOKMARK_ADD, on_click=self.prestar),
                ]
            ),
            ft.Divider(),
            ft.Text("Libros prestados actualmente", weight=ft.FontWeight.BOLD),
            self.tabla,
        ]
        self.refrescar(actualizar=False)

    def prestar(self, e):
        try:
            self.biblioteca.prestar(self.libro.value, self.cliente.value)
        except BibliotecaError as err:
            self.notificar(str(err))
            return
        self.libro.value = None
        self.notificar("Préstamo registrado.")
        self.refrescar()
        self.al_cambiar()

    def devolver(self, codigo):
        try:
            self.biblioteca.devolver(codigo)
        except BibliotecaError as err:
            self.notificar(str(err))
            return
        self.notificar("Libro devuelto.")
        self.refrescar()
        self.al_cambiar()

    def refrescar(self, actualizar=True):
        # Actualizamos los libros y usuarios disponibles.
        self.libro.options = [
            ft.DropdownOption(key=l.codigo, text=f"{l.codigo} - {l.titulo}")
            for l in self.biblioteca.libros_disponibles()
        ]
        self.cliente.options = [
            ft.DropdownOption(key=c.cedula, text=f"{c.cedula} - {c.nombre}")
            for c in self.biblioteca.clientes
        ]
        if self.libro.value not in [o.key for o in self.libro.options]:
            self.libro.value = None
        if self.cliente.value not in [o.key for o in self.cliente.options]:
            self.cliente.value = None
        self.tabla.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(p.libro.codigo)),
                    ft.DataCell(ft.Text(p.libro.titulo)),
                    ft.DataCell(ft.Text(p.cliente.nombre)),
                    ft.DataCell(ft.Text(p.fecha.isoformat())),
                    ft.DataCell(ft.Text(p.fecha_limite.isoformat())),
                    ft.DataCell(
                        ft.Text(
                            f"Atrasado {p.dias_atraso} día(s)" if p.atrasado else "A tiempo",
                            color=ft.Colors.RED if p.atrasado else ft.Colors.GREEN,
                            weight=ft.FontWeight.BOLD,
                        )
                    ),
                    ft.DataCell(
                        ft.TextButton(
                            "Devolver",
                            icon=ft.Icons.KEYBOARD_RETURN,
                            on_click=lambda e, c=p.libro.codigo: self.devolver(c),
                        )
                    ),
                ]
            )
            for p in self.biblioteca.prestamos
        ]
        if actualizar:
            self.update()
