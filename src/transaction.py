from datetime import date
from dataclasses import dataclass, asdict
from typing import Self

from .category import Category


transaction_field_translations = {
    'transaction_date': 'Дата',
    'category': 'Категория',
    'total': 'Сумма',
    'description': 'Описание'
}


@dataclass
class Transaction:
    transaction_id: int
    transaction_date: date
    category: Category
    total: float
    description: str


    def as_dict(self) -> dict:
        return asdict(self)

    def update(self, data: Self) -> None:
        '''Accept another Transaction and copies its fields'''
        for attr in self.as_dict():
            if attr != 'transaction_id' and data.as_dict().get(attr, None):
                self.__setattr__(attr, data.as_dict()[attr])

    def __str__(self) -> str:
        '''Special representaion for app'''
        result = ''
        for attr, value in self.as_dict().items():
            if attr != 'transaction_id':
                result += f'{transaction_field_translations[attr]}: {value}\n'
        return result + '\n'
