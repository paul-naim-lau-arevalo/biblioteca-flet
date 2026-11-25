import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from biblioteca import Biblioteca, BibliotecaError


class PruebasBiblioteca(unittest.TestCase):
    def setUp(self):
        self.b = Biblioteca()
        self.b.agregar_libro("L1", "Don Quijote", "Cervantes", "1605")
        self.b.agregar_cliente("8-123-456", "Ana Pérez", "ana@correo.com", "60001234")

    def test_libro_invalido(self):
        with self.assertRaises(BibliotecaError):
            self.b.agregar_libro("", "x", "y", "2000")
        with self.assertRaises(BibliotecaError):
            self.b.agregar_libro("L2", "x", "y", "abc")
        with self.assertRaises(BibliotecaError):
            self.b.agregar_libro("L2", "x", "y", "9999")

    def test_codigo_duplicado(self):
        with self.assertRaises(BibliotecaError):
            self.b.agregar_libro("L1", "Otro", "Autor", "2000")

    def test_cliente_invalido(self):
        with self.assertRaises(BibliotecaError):
            self.b.agregar_cliente("1", "Luis", "sin-arroba")
        with self.assertRaises(BibliotecaError):
            self.b.agregar_cliente("8-123-456", "Repetido")

    def test_prestamo_y_devolucion(self):
        self.b.prestar("L1", "8-123-456")
        self.assertFalse(self.b.buscar_libro("L1").disponible)
        self.assertEqual(self.b.libros_disponibles(), [])
        with self.assertRaises(BibliotecaError):
            self.b.prestar("L1", "8-123-456")
        self.b.devolver("L1")
        self.assertTrue(self.b.buscar_libro("L1").disponible)
        self.assertEqual(self.b.prestamos, [])

    def test_no_eliminar_con_prestamo(self):
        self.b.prestar("L1", "8-123-456")
        with self.assertRaises(BibliotecaError):
            self.b.eliminar_libro("L1")
        with self.assertRaises(BibliotecaError):
            self.b.eliminar_cliente("8-123-456")
        self.b.devolver("L1")
        self.b.eliminar_libro("L1")
        self.b.eliminar_cliente("8-123-456")

    def test_devolver_sin_prestamo(self):
        with self.assertRaises(BibliotecaError):
            self.b.devolver("L1")


if __name__ == "__main__":
    unittest.main()
