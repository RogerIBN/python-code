"""Programa de ejemplo de como funcionan las clases"""
# Declaración de la clase
from typing import Self


class Person:
    """Modelo de una persona"""

    # __init__ es la palabra clave de la función que ejecuta una clase cuando
    # se instancia
    def __init__(self, name: str, age: int):
        self.name = name  # Guarda la variable nombre como atributo del objeto
        self.age = age  # Guarda la variable edad como atributo del objeto

    def introduce_oneself(
        self,
    ) -> None:  # Método del objeto mientras accede a sus atributos
        """Método que imprime el nombre y la edad de la persona"""
        print(f"{self.name}: Mi nombre es {self.name} y tengo {self.age} años")

    # Método del objeto mientras accede a sus atributos y los de otro objeto
    def greet(self, other: Self) -> None:
        """
        Método que hace una persona salude a otra

        Parameters
        ----------
        other : Self
            La persona a saludar
        """
        print(f"{self.name}: Hola {other.name}, soy {self.name}")


def main():
    """Función principal del programa"""
    # Crear los objetos de que pertenecen a la clase persona (instanciar)
    person_1 = Person(name="Roger", age=24)
    person_2 = Person(name="Karla", age=24)

    # Probar los métodos
    person_1.introduce_oneself()
    person_2.introduce_oneself()

    person_1.greet(person_2)

    # Acceder a los atributos (Probamos si sus edades son iguales)
    print(
        f"""\
    ¿{person_1.name} y {person_2.name} tienen la misma edad?
    Respuesta: {person_1.age == person_2.age}"""
    )


if __name__ == "__main__":
    main()
