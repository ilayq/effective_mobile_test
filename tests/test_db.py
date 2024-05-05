import unittest

from src import FileDataBase
from src.transaction import Transaction, Category, date


class TestFileDataBase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transaction = Transaction(
            transaction_id=-1,
            transaction_date=date(2024, 5, 5),
            category=Category.income,
            total=5000.0,
            description='test'
        )
        with open('test', 'w'):
            pass

    def test_add_transaction(self):
        db = FileDataBase('test')
        db.add_transaction(self.transaction)
        assert db.get_transactions()[0] == self.transaction

    def test_edit_transaction(self):
        db = FileDataBase('test') 
        db.add_transaction(self.transaction)
        tr_id = db.get_transactions()[0].transaction_id
        new_transaction = Transaction(
            transaction_id=tr_id,
            transaction_date=date(2024, 5, 5),
            category=Category.spending,
            total=5000.0,
            description='test'
        )
        db.edit_transaction(new_transaction)
        assert db.get_transactions()[0].category == Category.spending

    def test_remove_transaction(self):
        db = FileDataBase('test') 
        db.add_transaction(self.transaction)
        assert db.get_transactions()
        tr_id = db.get_transactions()[0].transaction_id
        db.remove_transaction(tr_id)
        assert not db.get_transactions()   


if __name__ == '__main__':
    unittest.main()