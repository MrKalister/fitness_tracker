from typing import Optional


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = (duration)
        self.distance = (distance)
        self.speed = (speed)
        self.calories = (calories)

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.'
                )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories()
                              )
        return(message)


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        return ((coeff_calorie_1 * self.get_mean_speed()
                - coeff_calorie_2) * self.weight
                / self.M_IN_KM * self.duration * 60
                )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coeff_calorie_1: float = 0.035
        coeff_calorie_2: int = 2
        coeff_calorie_3: float = 0.029
        return ((coeff_calorie_1 * self.weight + (self.get_mean_speed()
                ** coeff_calorie_2
                // self.height) * coeff_calorie_3
                * self.weight) * self.duration * 60
                )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        coeff_calorie_1: float = 1.1
        coeff_calorie_2: int = 2
        return ((self.get_mean_speed() + coeff_calorie_1)
                * coeff_calorie_2 * self.weight
                )


def read_package(workout_type: str, data: list) -> str:
    """Прочитать данные полученные от датчиков."""
    DICT_training = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    select_training = DICT_training[workout_type]
    if workout_type == 'SWM':
        return select_training(data[0], data[1], data[2], data[3], data[4])
    elif workout_type == 'RUN':
        return select_training(data[0], data[1], data[2])
    elif workout_type == 'WLK':
        return select_training(data[0], data[1], data[2], data[3])


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())
    


# тестовые данные
if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)