"""
Poner los lenguajes de programación únicos en una estructura de datos.
"""


def main():
    """Main function"""
    # %%
    personas = [
        {
            "id": 0,
            "nombre": "Pedro",
            "edad": 35,
            "skills": [
                {"lenguajes": ["java", "python", "scala"]},
                {"sistemasOperativos": ["ubuntu", "windows"]},
                {"idiomas": ["español", "ingles"]},
            ],
        },
        {
            "id": 0,
            "nombre": "Javier",
            "edad": 22,
            "skills": [
                {"lenguajes": ["c++", "c#", "scala"]},
                {"sistemasOperativos": ["windows"]},
                {"idiomas": ["español", "francés"]},
            ],
        },
        {
            "id": 0,
            "nombre": "Samuel",
            "edad": 29,
            "skills": [
                {"sistemasOperativos": ["suse-linux", "windows"]},
                {"lenguajes": ["java", "python"]},
                {"idiomas": ["español", "italiano"]},
            ],
        },
    ]
    # %% Con set comprehension
    lenguajes_personas = {
        lenguaje
        for persona in personas
        for skill in persona.get("skills", [])
        for lenguaje in skill.get("lenguajes", [])
    }
    print(f"{lenguajes_personas=}")


# %%
if __name__ == "__main__":
    main()
