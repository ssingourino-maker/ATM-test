from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty

# بيانات الحساب التجريبية
account = {
    "name": "pycode.hubb",
    "balance": 75000,
    "pin": "1111",
    "type": "savings account"
}


# 1. شاشة تسجيل الدخول
class LoginScreen(Screen):
    def verify_pin(self, pin_text):
        if pin_text == account["pin"]:
            if "error_label" in self.ids:
                self.ids.error_label.text = ""
            self.manager.current = "menu"
            self.manager.get_screen("menu").update_welcome()
        else:
            if "error_label" in self.ids:
                self.ids.error_label.text = "❌ Invalid PIN! Try again."


# 2. شاشة القائمة الرئيسية
class MenuScreen(Screen):
    welcome_text = StringProperty("")

    def update_welcome(self):
        self.welcome_text = f"Welcome, {account['name']}"


# 3. شاشة عرض الرصيد
class BalanceScreen(Screen):
    balance_text = StringProperty("")

    def on_enter(self):
        self.balance_text = f"Your Balance: {account['balance']} DZD"


# 4. شاشة الإيداع والسحب
class TransactionScreen(Screen):
    transaction_type = StringProperty("")
    message_text = StringProperty("")

    def perform_transaction(self, amount_str):
        try:
            amount = int(amount_str)
            if amount <= 0:
                self.message_text = "❌ Amount must be > 0"
                return

            if self.transaction_type == "Deposit":
                account["balance"] += amount
                self.message_text = f"✅ Deposited successfully!\nNew Balance: {account['balance']}"
            elif self.transaction_type == "Withdraw":
                if amount > account["balance"]:
                    self.message_text = "❌ Insufficient funds!"
                else:
                    account["balance"] -= amount
                    self.message_text = f"💸 Please collect cash!\nNew Balance: {account['balance']}"
        except ValueError:
            self.message_text = "❌ Please enter a valid number."


# 5. شاشة تفاصيل الحساب
class DetailsScreen(Screen):
    details_text = StringProperty("")

    def on_enter(self):
        self.details_text = (
            f"Name: {account['name']}\n"
            f"Balance: {account['balance']} DZD\n"
            f"Type: {account['type']}"
        )


# مدير الشاشات العام
class WindowManager(ScreenManager):
    pass


class ATMApp(App):
    def build(self):
        return WindowManager()


if __name__ == '__main__':
    ATMApp().run()
