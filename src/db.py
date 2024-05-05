from typing import Callable, override
from abc import abstractmethod, ABC

from .transaction import Transaction, Category, date
from .utils import find_if, find_all_if


class DataSource(ABC):
    '''Abstract class for app data source'''

    @abstractmethod
    def save_data(self) -> None:
        '''Saving data that was added in session'''
        raise NotImplementedError()
    
    @abstractmethod
    def add_transaction(self, transaction: Transaction) -> None:
        '''Add new transaction'''
        raise NotImplementedError()
    
    @abstractmethod
    def edit_transaction(self, new_data: Transaction) -> None | Exception:
        '''Edit existing Transaction, takes transaction id from new_data'''
        raise NotImplementedError()
    
    @abstractmethod
    def remove_transaction(self, transaction_id: int) -> None | Exception:
        '''Remove existing Transaction by id'''
        raise NotImplementedError()
    
    @abstractmethod
    def get_transactions(self, predicate: Callable[[Transaction], bool] | None = None) -> list[Transaction]:
        '''Returns transactions that fits for predicate'''
        raise NotImplementedError()



class FileDataBase(DataSource):
    '''Implementation of data source using txt files'''
    def __init__(self, filename: str):
        self.filename: str = filename
        self.__data: list[Transaction] = []
        self.current_transaction_id = 0
        try:
            self.__read_data()
        except ValueError:
            raise ValueError(f'Error in reading data, please check {self.filename}')

    @override
    def __read_data(self) -> None:
        with open(self.filename, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file.readlines()]
            for line_idx in range(0, len(lines), 5):
                self.current_transaction_id = line_idx
                _, transaction_date = lines[line_idx].split(': ')
                _, category = lines[line_idx + 1].split(': ')
                _, total = lines[line_idx + 2].split(': ')
                _, description = lines[line_idx + 3].split(': ')
                self.__data.append(Transaction(
                    transaction_id=self.current_transaction_id,
                    transaction_date=date.fromisoformat(transaction_date),
                    category=Category(category),
                    total=float(total),
                    description=description
                ))

    @override
    def save_data(self) -> None:
        with open(self.filename, 'w', encoding='utf-8') as file:
            stringed_data = ''
            for transaction in self.__data:
                stringed_data += str(transaction)
            file.write(stringed_data)

    @override
    def add_transaction(self, transaction: Transaction) -> None:
        self.current_transaction_id += 1
        transaction.transaction_id = self.current_transaction_id
        self.__data.append(transaction)

    @override
    def edit_transaction(self, new_data: Transaction) -> None | Exception:
        transaction_to_edit = find_if(self.__data, lambda transaction: transaction.transaction_id == new_data.transaction_id)
        if not transaction_to_edit:
            raise ValueError(f'Transaction with id {new_data.transaction_id} not found')
        transaction_to_edit.update(new_data)

    @override
    def remove_transaction(self, transaction_id: int) -> None | Exception:
        transaction_to_remove = find_if(self.__data, lambda transaction: transaction.transaction_id == transaction_id)
        if not transaction_to_remove:
            raise ValueError(f'Transaction with id {transaction_id} not found')
        self.__data.remove(transaction_to_remove)
    
    @override
    def get_transactions(self, predicate: Callable[[Transaction], bool] | None = None) -> list[Transaction]:
        if not predicate:
            return self.__data
        return find_all_if(self.__data, predicate)
