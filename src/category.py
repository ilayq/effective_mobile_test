from enum import Enum


class Category(Enum):
    income = 'Доход'
    spending = 'Расход'

    def __str__(self) -> str:
        '''Returns string representaion of value'''
        return str(self.value)
