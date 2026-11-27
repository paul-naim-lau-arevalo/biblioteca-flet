# Clases y funciones del sistema de biblioteca

from dataclasses import dataclass
from datetime import date, timedelta
DIAS_PRESTAMO = 7 


class BibliotecaError(Exception):
    pass


@dataclass
class Libro:
    codigo: str
    titulo: str
    autor: str
    anio: int
    disponible: bool = True


@dataclass
class Cliente:
    cedula: str
    nombre: str
    correo: str = ""
    telefono: str = ""


@dataclass
class Prestamo:
    libro: Libro
    cliente: Cliente
    fecha: date

    @property
    def fecha_limite(self) -> date:
        return self.fecha + timedelta(days=DIAS_PRESTAMO)

    @property
    def dias_atraso(self) -> int:
        return max(0, (date.today() - self.fecha_limite).days)

    @property
    def atrasado(self) -> bool:
        return self.dias_atraso > 0


class Biblioteca:
    def __init__(self):
        self.libros: list[Libro] = []
        self.clientes: list[Cliente] = []
        self.prestamos: list[Prestamo] = []

    # Libros
    def agregar_libro(self, codigo, titulo, autor, anio) -> Libro:
        codigo = (codigo or "").strip()
        titulo = (titulo or "").strip()
        autor = (autor or "").strip()
        if not codigo or not titulo or not autor:
            raise BibliotecaError("Código, título y autor son obligatorios.")
        try:
            anio = int(anio)
        except (TypeError, ValueError):
            raise BibliotecaError("El año debe ser un número.")
        if not 1 <= anio <= date.today().year:
            raise BibliotecaError("El año no es válido.")
        if self.buscar_libro(codigo):
            raise BibliotecaError(f"Ya existe un libro con el código {codigo}.")
        libro = Libro(codigo, titulo, autor, anio)
        self.libros.append(libro)
        return libro

    def buscar_libro(self, codigo) -> Libro | None:
        for libro in self.libros:
            if libro.codigo == codigo:
                return libro
        return None

    def eliminar_libro(self, codigo) -> None:
        libro = self.buscar_libro(codigo)
        if libro is None:
            raise BibliotecaError("El libro no existe.")
        if not libro.disponible:
            raise BibliotecaError("No se puede eliminar un libro que está prestado.")
        self.libros.remove(libro)

    def libros_disponibles(self) -> list[Libro]:
        disponibles = []
        for libro in self.libros:
            if libro.disponible:
                disponibles.append(libro)
        return disponibles

    # Clientes
    def agregar_cliente(self, cedula, nombre, correo="", telefono="") -> Cliente:
        cedula = (cedula or "").strip()
        nombre = (nombre or "").strip()
        correo = (correo or "").strip()
        telefono = (telefono or "").strip()
        if not cedula or not nombre:
            raise BibliotecaError("Cédula y nombre son obligatorios.")
        if correo and ("@" not in correo or "." not in correo.split("@")[-1]):
            raise BibliotecaError("El correo no es válido.")
        if self.buscar_cliente(cedula):
            raise BibliotecaError(f"Ya existe un cliente con la cédula {cedula}.")
        cliente = Cliente(cedula, nombre, correo, telefono)
        self.clientes.append(cliente)
        return cliente

    def buscar_cliente(self, cedula) -> Cliente | None:
        for cliente in self.clientes:
            if cliente.cedula == cedula:
                return cliente
        return None

    def eliminar_cliente(self, cedula) -> None:
        cliente = self.buscar_cliente(cedula)
        if cliente is None:
            raise BibliotecaError("El cliente no existe.")
        if any(p.cliente is cliente for p in self.prestamos):
            raise BibliotecaError("No se puede eliminar un cliente con libros prestados.")
        self.clientes.remove(cliente)

    # Préstamos
    def prestar(self, codigo_libro, cedula_cliente) -> Prestamo:
        libro = self.buscar_libro(codigo_libro)
        cliente = self.buscar_cliente(cedula_cliente)
        if libro is None or cliente is None:
            raise BibliotecaError("Selecciona un libro y un cliente.")
        if not libro.disponible:
            raise BibliotecaError("El libro ya está prestado.")
        cantidad = sum(1 for p in self.prestamos if p.cliente is cliente)
        if cantidad >= 3:
            raise BibliotecaError("El cliente ya tiene 3 libros prestados.")
        libro.disponible = False
        prestamo = Prestamo(libro, cliente, date.today())
        self.prestamos.append(prestamo)
        return prestamo

    def devolver(self, codigo_libro) -> Prestamo:
        prestamo = next((p for p in self.prestamos if p.libro.codigo == codigo_libro), None)
        if prestamo is None:
            raise BibliotecaError("Ese libro no tiene un préstamo activo.")
        prestamo.libro.disponible = True
        self.prestamos.remove(prestamo)
        return prestamo

    def prestamos_atrasados(self) -> list[Prestamo]:
        return [p for p in self.prestamos if p.atrasado]