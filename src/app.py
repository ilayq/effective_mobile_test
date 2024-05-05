from os import read
from typing import Callable
from .db import DataSource
from .transaction import Transaction, Category
from .utils import read_value, date, read_transaction, read_value_or_skip


class FinanceControllerApp:
    def __init__(self, data_source: DataSource):
        self.db = data_source
        self.__count_balance()

    def run(self):
        '''Main function to run app'''
        while True:
            print('Выберите действие:\n\
                \r1. Вывести баланс\n\
                \r2. Вывести все записи\n\
                \r3. Редактировать запись\n\
                \r4. Добавить запись\n\
                \r5. Удалить запись\n\
                \r6. Поиск по записям\n\
                \r7. Выход\n')
            command = read_value(int, '')
            match command:
                case 1:
                    print(self.__count_balance())
                case 2:
                    for transaction in self.db.get_transactions():
                        print(f'Идентификатор: {transaction.transaction_id}')
                        print(transaction)
                case 3:
                    self.edit_transaction_command()
                case 4:
                    self.add_transaction_command()
                case 5:
                    self.remove_transaction_command()
                case 6:
                    self.find_transactions()
                case 7:
                    break

    def edit_transaction_command(self) -> None:
        '''Handler for editing transactions, reads new data about transaction from stdin and updates it in db'''
        try:
            self.db.edit_transaction(read_transaction(read_id=True))
        except ValueError as e:
            print(e)

    def add_transaction_command(self) -> None:
        '''Handler for adding new transactions, reads data about transaction from stdin and add it in db'''
        transaction = read_transaction()
        self.db.add_transaction(transaction)

    def remove_transaction_command(self) -> None:
        '''Handler for removing transactions, reads transaction id from stdin and removes it in db'''
        tr_id = read_value(int, 'идентификатор')
        try:
            self.db.remove_transaction(tr_id)
        except ValueError as e:
            print(e)

    def find_transactions(self) -> None:
        '''Handler for filtering transactions, reads data for search from stdin, makes predicate and send it to db'''
        tr_date, skip_date = read_value_or_skip(date.fromisoformat, 'дату')
        category, skip_category = read_value_or_skip(Category, 'категорию')
        total, skip_total = read_value_or_skip(float, 'сумму')
        description, skip_description = read_value_or_skip(str, 'описание')
        print(skip_category or (self.db.get_transactions()[1].category == category))
        print(skip_date or (self.db.get_transactions()[1].transaction_date == tr_date))
        print(skip_total or (self.db.get_transactions()[1].total == total))
        print(skip_description or (description in self.db.get_transactions()[1].description))
        print(description, skip_description)
        filter: Callable[[Transaction], bool] = lambda transaction:  (skip_date or (transaction.transaction_date == tr_date)) and\
                                                                     (skip_category or (transaction.category == category)) and\
                                                                     (skip_total or (transaction.total == total)) and\
                                                                     (skip_description or (description in transaction.description))
        for transaction in self.db.get_transactions(filter):
            print(f'Идентификатор: {transaction.transaction_id}')
            print(transaction)
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.db.save_data()

    def __count_balance(self) -> float:
        return sum(
                    transaction.total
                    if transaction.category == Category.income
                    else -transaction.total
                    for transaction in self.db.get_transactions()
                )
        
    