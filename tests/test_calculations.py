import pytest # type: ignore
from app.calculations import add, subtract, multiply, divide, BankAccount

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (1, 2, 3),
    (2, 3, 5),
    (-1, 1, 0),
])
def test_add(num1, num2, expected):
    print("testing add function")
    assert add(num1, num2) == expected

@pytest.mark.parametrize("num1, num2, expected", [
    (1, 2, -1),
    (2, 3, -1),
    (-1, 1, -2),
])
def test_subtract(num1, num2, expected):
    assert subtract(num1, num2) == expected

@pytest.mark.parametrize("num1, num2, expected", [
    (1, 2, 2),
    (2, 3, 6),
    (-1, 1, -1),
])
def test_multiply(num1, num2, expected):
    assert multiply(num1, num2) == expected

@pytest.mark.parametrize("num1, num2, expected", [
    (1, 2, 0.5),
    (2, 3, 0.6666666666666666),
    (-1, 1, -1),
])
def test_divide(num1, num2, expected):
    assert divide(num1, num2) == expected

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000),
])
def test_bank_transaction_insufficient_funds(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected 

def test_bank_transaction_insufficient_funds(bank_account):
    with pytest.raises(Exception):
        bank_account.withdraw(200)


