# Registro de libros
import flet as ft

from biblioteca import Biblioteca, BibliotecaError


class VistaLibros(ft.Column):
    def __init__(self, biblioteca: Biblioteca, notificar, al_cambiar=lambda: None):
        super().__init__(spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)
        self.biblioteca = biblioteca
        self.notificar = notificar
        self.al_cambiar = al_cambiar

        self.codigo = ft.TextField(label="Código", width=140)
        self.titulo = ft.TextField(label="Título", expand=True)
        self.autor = ft.TextField(label="Autor", expand=True)
        self.anio = ft.TextField(
            label="Año", width=100, input_filter=ft.NumbersOnlyInputFilter()
        )
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Código")),
                ft.DataColumn(ft.Text("Título")),
                ft.DataColumn(ft.Text("Autor")),
                ft.DataColumn(ft.Text("Año")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("")),
            ],
            rows=[],
        )
        self.controls = [
            ft.Text("Ingreso de Libros", size=20, weight=ft.FontWeight.BOLD),
            ft.Row([self.codigo, self.titulo]),
            ft.Row(
                [
                    self.autor,
                    self.anio,
                    ft.FilledButton("Agregar libro", icon=ft.Icons.ADD, on_click=self.agregar),
                ]
            ),
            ft.Divider(),
            self.tabla,
        ]
        self.refrescar(actualizar=False)

    def agregar(self, e):
        try:
            self.biblioteca.agregar_libro(
                self.codigo.value, self.titulo.value, self.autor.value, self.anio.value
            )
        except BibliotecaError as err:
            self.notificar(str(err))
            return
        for campo in (self.codigo, self.titulo, self.autor, self.anio):
            campo.value = ""
        self.notificar("Libro agregado.")
        self.refrescar()
        self.al_cambiar()

    def eliminar(self, codigo):
        try:
            self.biblioteca.eliminar_libro(codigo)
        except BibliotecaError as err:
            self.notificar(str(err))
            return
        self.notificar("Libro eliminado.")
        self.refrescar()
        self.al_cambiar()

    def refrescar(self, actualizar=True):
        self.tabla.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(l.codigo)),
                    ft.DataCell(ft.Text(l.titulo)),
                    ft.DataCell(ft.Text(l.autor)),
                    ft.DataCell(ft.Text(str(l.anio))),
                    ft.DataCell(ft.Text("Disponible" if l.disponible else "Prestado")),
                    ft.DataCell(
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            tooltip="Eliminar libro",
                            on_click=lambda e, c=l.codigo: self.eliminar(c),
                        )
                    ),
                ]
            )
            for l in self.biblioteca.libros
        ]
        if actualizar:
            self.update()
