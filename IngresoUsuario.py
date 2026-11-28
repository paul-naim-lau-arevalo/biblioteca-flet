# Registro de usuarios
import flet as ft

from biblioteca import Biblioteca, BibliotecaError


class VistaUsuarios(ft.Column):
    def __init__(self, biblioteca: Biblioteca, notificar, al_cambiar=lambda: None):
        super().__init__(spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)
        self.biblioteca = biblioteca
        self.notificar = notificar
        self.al_cambiar = al_cambiar
        # casillas de ttexto para usuarios
        self.cedula = ft.TextField(label="Cédula", width=180)
        self.nombre = ft.TextField(label="Nombre completo", width=300)
        self.correo = ft.TextField(label="Correo", width=380, keyboard_type=ft.KeyboardType.EMAIL)
        self.telefono = ft.TextField(
            label="Teléfono", width=160, input_filter=ft.NumbersOnlyInputFilter()
        )
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Ingrese Cédula")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Correo")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("")),
            ],
            rows=[],
        )
        self.controls = [
            ft.Text("Ingreso de Usuarios", size=20, weight=ft.FontWeight.BOLD),
            ft.Row([self.cedula, self.nombre]),
            ft.Row(
                [
                    self.correo,
                    self.telefono,
                    ft.FilledButton("Agregar usuario", icon=ft.Icons.PERSON_ADD, on_click=self.agregar),
                ]
            ),
            ft.Divider(),
            self.tabla,
        ]
        self.refrescar(actualizar=False)

    def agregar(self, e):
        try:
            self.biblioteca.agregar_cliente(
                self.cedula.value, self.nombre.value, self.correo.value, self.telefono.value
            )
        except BibliotecaError as err:
            self.notificar(str(err))
            return
        for campo in (self.cedula, self.nombre, self.correo, self.telefono):
            campo.value = ""
        self.notificar("Usuario agregado.")
        self.refrescar()
        self.al_cambiar()

    def eliminar(self, cedula):
        try:
            self.biblioteca.eliminar_cliente(cedula)
        except BibliotecaError as err:
            self.notificar(str(err))
            return
        self.notificar("Usuario eliminado.")
        self.refrescar()
        self.al_cambiar()

    def refrescar(self, actualizar=True):
        self.tabla.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(c.cedula)),
                    ft.DataCell(ft.Text(c.nombre)),
                    ft.DataCell(ft.Text(c.correo)),
                    ft.DataCell(ft.Text(c.telefono)),
                    ft.DataCell(
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            tooltip="Eliminar usuario",
                            on_click=lambda e, ced=c.cedula: self.eliminar(ced),
                        )
                    ),
                ]
            )
            for c in self.biblioteca.clientes
        ]
        if actualizar:
            self.update()
