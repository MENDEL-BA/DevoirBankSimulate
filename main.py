import re
import sys


class Account:
    def __init__(self, name, balance, showBalanceAfterTransaction=True):
        self.name = name
        self.balance = balance
        self.startingBalance = balance
        self.showBalanceAfterTransaction = showBalanceAfterTransaction
        self.transactions = []

    def getName(self):
        return self.name

    def getBalance(self):
        return self.balance

    def showBalance(self):
        print('%s: le solde est le $%0.2f.' % (self.name, self.balance))
        print()

    def showTransactions(self):
        balance = self.startingBalance
        print('   op       amount     balance')
        print('--------  ----------  ----------')
        print('                      %10.2f  ' % balance)
        for transaction in self.transactions:
            [op, amount] = transaction
            if op == 'w':
                opLabel = 'withdraw'
                balance -= amount
            else:
                opLabel = 'deposit'
                balance += amount
            print('%-8s  %10.2f  %10.2f' % (opLabel, amount, balance))
        print()

    def withdrawal(self, amount):
        if amount > self.balance:
            print("Desole, Votre solde est insufisant!")
        else:
            print('%s: Retrait $%0.2f.' % (self.name, amount))
            self.balance = float('%.2f' % (self.balance - amount))  # prevent accumulation error
            self.transactions.append(['w', amount])
            if self.showBalanceAfterTransaction:
                self.showBalance()

    def deposit(self, amount):
        print('%s: depot $%0.2f.' % (self.name, amount))
        self.balance = float('%.2f' % (self.balance + amount))  # prevent accumulation error
        self.transactions.append(['d', amount])
        if self.showBalanceAfterTransaction:
            self.showBalance()

    def processTransactions(account):
        while True:
            amount = None
            op = Input().getOperation()
            if op == 'q':
                break
            elif op == 't':
                account.showTransactions()
            elif op is not None:
                amount = Input().getAmount()

            if amount is None:
                pass
            elif op == 'd':
                account.deposit(amount)
            else:
                account.withdrawal(amount)


class Input:
    def getOperation(self):
        op = input('Entrer d pour un depot, w pour un retrait, t pour une transaction, ou q pour quitter: ')
        if op not in set('qdwt'):
            print('Operation non permise.  Veuillez reessayer.')
            op = None
        return op

    def validateDollarAmount(self, amountStr):
        tooMuchPrecision = re.compile('.*\.\d\d\d.*')
        if tooMuchPrecision.match(str(amountStr)):
            raise Exception('Vous ne pouvez pas fournir des fractions de cent.')

    def getAmount(self):
        amount = None
        try:
            value = input('Entrer le solde : ')
            amount = float(value)
            if amount <= 0:
                raise Exception('Le solde doit etre positif.')
            self.validateDollarAmount(value)
        except ValueError:
            print('Montant invaalide. Veuillez reesseyer')
        except Exception as e:
            print(e)
            amount = None

        return amount


class Test:
    def __init__(self):
        self.numTests = 0
        self.numPass = 0

    def testBalance(self, account, expected):
        self.numTests += 1
        actual = account.getBalance()
        name = account.getName()
        if actual == expected:
            self.numPass += 1
            print('%s: OK      solde = %.2f' % (name, actual))
        else:
            print('%s: ERROR   solde = %.2f, error %.2f' % (name, actual, expected))

    def summarizeResults(self):
        numFailed = self.numTests - self.numPass
        print()
        print('%d tests total' % self.numTests)
        if numFailed == 0:
            print('all passed')
        else:
            print('%d passed' % self.numPass)
            print('%d failed' % numFailed)
        return numFailed == 0

    def run(self):
        a1 = Account('a1', 0, False)
        self.testBalance(a1, 0)

        a2 = Account('a2', 100, False)
        self.testBalance(a2, 100)

        a1.deposit(10)
        a1.deposit(10)
        a1.deposit(10)
        a1.withdrawal(5)
        self.testBalance(a1, 25.0)

        a2.withdrawal(25)
        a2.withdrawal(15)
        a2.withdrawal(0.50)
        a2.deposit(15)
        self.testBalance(a2, 74.5)

        a1.withdrawal(3.25)
        a1.deposit(4)
        self.testBalance(a1, 25.75)

        a2.deposit(1.30)
        a2.withdrawal(11.29)
        self.testBalance(a2, 64.51)

        allPassed = self.summarizeResults()
        return allPassed


class App:
    defaultBalance = 0.0

    def usage(self):
        print('usage: %s [-t|amount]' % sys.argv[0])
        print('ici -t signifie  test')
        print('et le solde est franc CFA')

    def parseAndValidateBalance(self, value):
        try:
            balance = float(value)
            if balance < 0:
                raise Exception('Le solde ne peur etre negatif.')
            Input().validateDollarAmount(value)
        except ValueError:
            raise Exception('Veullez entrer un solde valide.')
        return balance

    def getArgs(self):
        isTestFlag = False
        balance = App.defaultBalance

        if len(sys.argv) > 2:
            raise Exception('Les parametres sont erronés.')
        elif len(sys.argv) == 2:
            value = sys.argv[1]
            if value == '-t':
                isTestFlag = True
            else:
                balance = self.parseAndValidateBalance(value)

        return (isTestFlag, balance)

    def processUserInputs(self, balance):
        print('Bienvenue dans votre Banque.')
        account = Account('MOn compte ', balance)
        account.showBalance()
        account.processTransactions()

    def run(self):
        try:
            (isTestFlag, balance) = self.getArgs()
        except Exception as e:
            print(e)
            self.usage()
            sys.exit(1)

        if not isTestFlag:
            self.processUserInputs(balance)
        elif not Test().run():
            sys.exit(1)


def main():
    App().run()
    sys.exit(0)

main()