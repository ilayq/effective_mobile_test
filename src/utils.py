from typing import Iterable, Callable
from datetime import date
from .transaction import Transaction, Category


def find_if[T](collection: Iterable[T], predicate: Callable[[T], bool]) -> T | None:
    '''Returns the first element of collection that fits for predicate'''
    for item in collection:
        if predicate(item):
            return item
    return None


def find_all_if[T](collection: Iterable[T], predicate: Callable[[T], bool]) -> list[T]:
    '''Returns all elements of collection fit for predicate'''
    result = []
    for item in collection:
        if predicate(item):
            result.append(item)
    return result


def read_value[T](value_type: Callable[[str], T], field_name: str) -> T:
    '''Reads from stding while cast to value_type return error'''
    input_string = ''
    if field_name:
        input_string = f'Введите {field_name}:'
    while True:
        try: 
            return value_type(input(input_string))
        except ValueError:
            pass

def read_transaction(read_id: bool = False) -> Transaction:
        '''Reads all data about transaction except id (by default)'''
        tr_id = -1
        if read_id:
            tr_id = read_value(int, 'идентификатор')
        tr_date = read_value(date.fromisoformat, 'дату в формате гггг-мм-дд')
        category = read_value(Category, 'категорию (Расход / Доход)')
        total = read_value(float, 'сумму')
        description = read_value(str, 'описание')
        return Transaction(
                transaction_id=tr_id,
                transaction_date=tr_date,
                category=category,
                total=total,
                description=description
            )

def read_value_or_skip[T](value_type: Callable[[str], T], field_name: str) -> tuple[T | str, bool]:
    '''Reads from stding while cast to value_type return error or input not equal to "-"'''
    if value_type is str:
        value = input(f'Введите {field_name} ("-" чтобы пропустить): ')
        if value.strip() == '-':
            return value, True
        return value, False
            
    while value := input(f'Введите {field_name} ("-" чтобы пропустить): '):
        try:
            casted_value = value_type(value)
            skip = False
            break
        except ValueError:
            if value.strip() == '-':
                casted_value = value
                skip = True
                break
    return casted_value, skip
