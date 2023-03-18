from typing import Tuple, List, Dict

from util.constants import LEFT, RIGHT


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

    def __eq__(self, other):
        if not isinstance(other, PaymentOption):
            return NotImplemented
        elif self is other:
            return True
        else:
            return self.common_owned == other.common_owned \
                   and self.lux_owned == other.lux_owned \
                   and self.left_lux_cost == other.left_lux_cost \
                   and self.right_lux_cost == other.right_lux_cost \
                   and self.left_common_cost == other.left_common_cost \
                   and self.right_common_cost == other.right_common_cost \
                   and self.left_lux == other.left_lux \
                   and self.right_lux == other.right_lux \
                   and self.left_common == other.left_common \
                   and self.right_common == other.right_common \
                   and self.left_payment == other.left_payment \
                   and self.right_payment == other.right_payment \
                   and self.bank_payment == other.bank_payment

    def __hash__(self):
        return super.__hash__((self.common_owned,
                              self.lux_owned,
                              self.left_lux_cost,
                              self.right_lux_cost,
                              self.left_common_cost,
                              self.right_common_cost,
                              self.left_lux,
                              self.right_lux,
                              self.left_common,
                              self.right_common,
                              self.bank_payment))

    def total(self) -> int:
        return self.left_payment + self.right_payment + self.bank_payment

    def resources(self) -> Dict[str, List]:
        return {
            LEFT: self.left_common + self.left_lux,
            RIGHT: self.right_common + self.right_lux
        }

    def as_tuple(self) -> Tuple[int, int, int]:
        return self.left_payment, self.right_payment, self.bank_payment


NO_PAYMENT = PaymentOption()
