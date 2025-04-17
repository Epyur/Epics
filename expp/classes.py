class Material:
    def __init__(self, name, thickness, density, color, thermal_conductivity=None, elasticity=None):
        self.name = name
        self.thickness = thickness
        self.density = density
        self.color = color
        self.thermal_conductivity = thermal_conductivity
        self.elasticity = elasticity

    def __str__(self):
        properties = [
            f"Название: {self.name}",
            f"Толщина: {self.thickness} мм",
            f"Плотность: {self.density} кг/м³",
            f"Цвет: {self.color}",
        ]
        if self.thermal_conductivity is not None:
            properties.append(f"Теплопроводность: {self.thermal_conductivity} Вт/(м·К)")
        if self.elasticity is not None:
            properties.append(f"Упругость: {self.elasticity} МПа")

        return ", ".join(properties)

import pandas as pd

# Создание DataFrame с данными о материалах
data = {
    'name': ['Древесина', 'Металл', 'Пластик'],
    'thickness': [30, 10, 5],
    'density': [600, 7800, 900],
    'color': ['Коричневый', 'Серый', 'Прозрачный'],
    'thermal_conductivity': [0.13, 50, 0.2],
    'elasticity': [10, 200, 2]
}

df = pd.DataFrame(data)



# Создание экземпляров класса Material из DataFrame
materials = []
for index, row in df.iterrows():
    material = Material(
        name=row['name'],
        thickness=row['thickness'],
        density=row['density'],
        color=row['color'],
        thermal_conductivity=row['thermal_conductivity'],
        elasticity=row['elasticity']
    )
    materials.append(material)

# Вывод информации о материалах
for material in materials:
    print(material)