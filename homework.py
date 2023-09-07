from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MSG_TRAINING_TYPE: str = 'Тип тренировки'
    MSG_DURATION: str = 'Длительность'
    MSG_DISTANCE: str = 'Дистанция'
    MSG_SPEED: str = 'Ср. скорость'
    MSG_CALORIES: str = 'Потрачено ккал'

    def get_message(self) -> str:
        """Вывод сообщения о тренировке."""
        return (f'{self.MSG_TRAINING_TYPE}: {self.training_type}; '
                f'{self.MSG_DURATION}: {self.duration:.3f} ч.; '
                f'{self.MSG_DISTANCE}: {self.distance:.3f} км; '
                f'{self.MSG_SPEED}: {self.speed:.3f} км/ч; '
                f'{self.MSG_CALORIES}: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MINUTES_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите get_spent_calories'
                                  ' в %s.' % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * (self.duration * self.MINUTES_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_FOR_COUNT_CALORIES_1: float = 0.035
    COEFF_FOR_COUNT_CALORIES_2: float = 0.029
    AV_SPEED_IN_M_IN_SECOND: float = 0.278
    SM_IN_M: int = 100

    def __init__(self, action: int, duration: float,
                 weight: float, height: int):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_FOR_COUNT_CALORIES_1 * self.weight
                 + ((self.get_mean_speed() * self.AV_SPEED_IN_M_IN_SECOND) ** 2
                    / (self.height / self.SM_IN_M))
                 * self.COEFF_FOR_COUNT_CALORIES_2 * self.weight)
                * (self.duration * self.MINUTES_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    OFF_SPEED: float = 1.1
    FOR_SPEED: int = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: int, count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool
                * self.count_pool / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.OFF_SPEED)
                * self.FOR_SPEED * self.weight * self.duration)


def read_package(_workout_type: str, _data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        training_classes: dict[str, type[Training]] = {
            'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking
        }
        return training_classes[_workout_type](*_data)
    except KeyError as e:
        print(f'Неверный тип тренировочного класса: {e}')


def main(_training: Training) -> None:
    """Главная функция."""
    try:
        info = _training.show_training_info()
        print(info.get_message())
    except AttributeError:
        pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
