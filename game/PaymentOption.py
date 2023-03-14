from typing import Tuple


def payment(l_payment: int, r_payment: int):
    return PaymentOption(l_payment, r_payment, 0)


def bank_payment(bank: int):
    return PaymentOption(0, 0, bank)


class PaymentOption:
    def __init__(self,
                 l_payment: int,
                 r_payment: int,
                 b_payment: int):
        self.left_payment: int = l_payment
        self.right_payment: int = r_payment
        self.bank_payment: int = b_payment

    def total(self):
        return self.left_payment + self.right_payment + self.bank_payment

    def as_tuple(self) -> Tuple[int, int, int]:
        return self.left_payment, self.right_payment, self.bank_payment


NO_PAYMENT = PaymentOption(0, 0, 0)
