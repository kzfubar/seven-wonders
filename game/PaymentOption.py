from util.constants import LEFT, RIGHT


def payment(cost: int, resources: list[str]) -> int:
    return cost * len(resources)


class PaymentOption:
    def __init__(
        self,
        common_owned: list[str] | None = None,
        lux_owned: list[str] | None = None,
        left_lux_cost: int = 2,
        right_lux_cost: int = 2,
        left_common_cost: int = 2,
        right_common_cost: int = 2,
        left_lux: list[str] | None = None,
        right_lux: list[str] | None = None,
        left_common: list[str] | None = None,
        right_common: list[str] | None = None,
        bank_payment: int = 0,
    ) -> None:
        self.common_owned = common_owned or []
        self.lux_owned = lux_owned or []

        self.left_lux_cost = left_lux_cost
        self.right_lux_cost = right_lux_cost
        self.left_common_cost = left_common_cost
        self.right_common_cost = right_common_cost

        self.left_lux = left_lux or []
        self.right_lux = right_lux or []
        self.left_common = left_common or []
        self.right_common = right_common or []

        self.left_payment: int = payment(left_lux_cost, self.left_lux) + payment(
            left_common_cost, self.left_common
        )
        self.right_payment: int = payment(
            right_common_cost, self.right_common
        ) + payment(right_lux_cost, self.right_lux)

        self.bank_payment: int = bank_payment

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, PaymentOption):
            return NotImplemented
        if self is value:
            return True
        return (
            self.common_owned == value.common_owned
            and self.lux_owned == value.lux_owned
            and self.left_lux_cost == value.left_lux_cost
            and self.right_lux_cost == value.right_lux_cost
            and self.left_common_cost == value.left_common_cost
            and self.right_common_cost == value.right_common_cost
            and self.left_lux == value.left_lux
            and self.right_lux == value.right_lux
            and self.left_common == value.left_common
            and self.right_common == value.right_common
            and self.left_payment == value.left_payment
            and self.right_payment == value.right_payment
            and self.bank_payment == value.bank_payment
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.common_owned,
                self.lux_owned,
                self.left_lux_cost,
                self.right_lux_cost,
                self.left_common_cost,
                self.right_common_cost,
                self.left_lux,
                self.right_lux,
                self.left_common,
                self.right_common,
                self.bank_payment,
            )
        )

    def total(self) -> int:
        return self.left_payment + self.right_payment + self.bank_payment

    def resources(self) -> dict[str, list]:
        return {
            LEFT: self.left_common + self.left_lux,
            RIGHT: self.right_common + self.right_lux,
        }

    def as_tuple(self) -> tuple[int, int, int]:
        return self.left_payment, self.right_payment, self.bank_payment


NO_PAYMENT = PaymentOption()
