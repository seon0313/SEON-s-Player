class Easing:
    def ease_in_out_cubic(x: float) -> float:
        return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2

    def ease_in_expo(x: float) -> float:
        return 0 if x == 0 else 2 ** (10 * x - 10)

    def ease_in_out_expo(x: float) -> float:
        if x == 0:
            return 0
        elif x == 1:
            return 1
        elif x < 0.5:
            return (2 ** (20 * x - 10)) / 2
        else:
            return (2 - 2 ** (-20 * x + 10)) / 2

