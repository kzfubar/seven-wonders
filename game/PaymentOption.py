from typing import Tuple, List


def payment(cost: int, resources: List[str]) -> int:
    return cost * len(resources)


def to_list(l):
    if l is None:
        return []
    return l


class PaymentOption:
    def __init__(self,
                 common_owned: List[str] = None,
                 lux_owned: List[str] = None,
                 left_lux_cost: int = 2,
                 right_lux_cost: int = 2,
                 left_common_cost: int = 2,
                 right_common_cost: int = 2,
                 left_lux: List[str] = None,
                 right_lux: List[str] = None,
                 left_common: List[str] = None,
                 right_common: List[str] = None,
                 bank_payment: int = 0):
        self.common_owned = to_list(common_owned)
        self.lux_owned = to_list(lux_owned)

        self.left_lux_cost = left_lux_cost
        self.right_lux_cost = right_lux_cost
        self.left_common_cost = left_common_cost
        self.right_common_cost = right_common_cost

        self.left_lux = to_list(left_lux)
        self.right_lux = to_list(right_lux)
        self.left_common = to_list(left_common)
        self.right_common = to_list(right_common)

        self.left_payment: int = payment(left_lux_cost, self.left_lux) \
                                 + payment(left_common_cost, self.left_common)
        self.right_payment: int = payment(right_common_cost, self.right_common) \
                                  + payment(right_lux_cost, self.right_lux)

        self.bank_payment: int = bank_payment

    def total(self):
        return self.left_payment + self.right_payment + self.bank_payment

    def as_tuple(self) -> Tuple[int, int, int]:
        return self.left_payment, self.right_payment, self.bank_payment


NO_PAYMENT = PaymentOption(0, 0, 0)
