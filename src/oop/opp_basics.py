"""Programa de ejemplo de como funcionan las clases"""
# Declaración de la clase
from typing import Self


class Persona:
    """Modelo de una persona"""

    # __init__ es la palabra clave de la función que ejecuta una clase cuando
    # se instancia
    def __init__(self, nombre: str, edad: int):
        self.nombre = nombre  # Guarda la variable nombre como atributo del objeto
        self.edad = edad  # Guarda la variable edad como atributo del objeto

    def presentarse(self) -> None:  # Método del objeto mientras accede a sus atributos
        """Método que imprime el nombre y la edad de la persona"""
        print(f"{self.nombre}: Mi nombre es {self.nombre} y tengo {self.edad} años")

    # Método del objeto mientras accede a sus atributos y los de otro objeto
    def saludar(self, other: Self) -> None:
        """
        Método que hace una persona salude a otra

        Parameters
        ----------
        other : Self
            La persona a saludar
        """
        print(f"{self.nombre}: Hola {other.nombre}, soy {self.nombre}")


def main():
    """Función principal del programa"""
    # Crear los objetos de que pertenecen a la clase persona (instanciar)
    persona_1 = Persona(nombre="Roger", edad=24)
    persona_2 = Persona(nombre="Karla", edad=24)

    # Probar los métodos
    persona_1.presentarse()
    persona_2.presentarse()

    persona_1.saludar(persona_2)

    # Acceder a los atributos (Probamos si sus edades son iguales)
    print(
        f"""\
    ¿{persona_1.nombre} y {persona_2.nombre} tienen la misma edad?
    Respuesta: {persona_1.edad == persona_2.edad}"""
    )


if __name__ == "__main__":
    main()
