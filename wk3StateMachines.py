from abc import ABC

class SM(ABC):
    state = 0
    startState = 0

    def start(self):
        self.state = self.startState

    # step returns the next output.
    def step(self, inp):
        (s, o) = self.getNextValues(self.state, inp)
        self.state = s
        return o

    def transduce(self, inputs):
        self.start()
        return [self.step(inp) for inp in inputs]

    def run(self, n=10):
        return self.transduce([None] * n)

    def getNextValues(self, state, inp):
        nextState = self.getNextState(state, inp)
        return (nextState, nextState)

    def getNextState(self, state, inp):
        pass


class VendingMachine(SM):
    startState = ('waiting', 0)  # The machine starts waiting with 0 money inserted
    drink_price = 75  # Price of the drink in cents

    def getNextValues(self, state, inp):
        current_state, total_money = state
        if inp == 'cancel':
            return (('canceled', 0), f"Transaction canceled. Returning ${total_money / 100:.2f}.")
        elif inp in [5, 10, 25, 100]:  # Valid inputs: nickel, dime, quarter, dollar
            total_money += inp
            if total_money >= self.drink_price:
                change = total_money - self.drink_price
                return (('dispensing', 0), f"Drink dispensed. Returning ${change / 100:.2f} in change.")
            else:
                return (('waiting', total_money), f"Amount entered: ${total_money / 100:.2f}. Insert more money.")
        else:
            return (state, "Invalid input.")

# --- Test Scenarios ---

# Scenario 1: User inputs three quarters
vending_machine = VendingMachine()
scenario1 = [25, 25, 25]  # Three quarters
print(vending_machine.transduce(scenario1))

# Scenario 2: User inputs one quarter and cancels the transaction
vending_machine = VendingMachine()  # Reset the machine
scenario2 = [25, 'cancel']  # One quarter, then cancel
print(vending_machine.transduce(scenario2))

# Scenario 3: User inputs a dime and a dollar bill
vending_machine = VendingMachine()  # Reset the machine
scenario3 = [10, 100]  # A dime, then a dollar bill
print(vending_machine.transduce(scenario3))