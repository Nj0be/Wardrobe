from django.contrib.auth.tokens import PasswordResetTokenGenerator
import accounts.models

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: accounts.models.User, timestamp):
        return f"{user.is_active}{user.email}{timestamp}"

account_activation_token = AccountActivationTokenGenerator()
