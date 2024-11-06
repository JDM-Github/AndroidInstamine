import re
import random
from datetime import datetime

class Utility:

    @staticmethod
    def generate_verification_code():
        return str(random.randint(100000, 999999))

    @staticmethod
    def get_size(size, percentage):
        return size[0] * percentage, size[1] * percentage

    @staticmethod
    def get_value_percentage(size, percentage):
        return size * percentage

    @staticmethod
    def is_strong_password(password):
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'[0-9]', password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        return True

    @staticmethod
    def set_color(widget, color):
        widget.color.rgba = color

    @staticmethod
    def validate_not_empty(widget, field_name, error_msg, error_color, success_color, error_callback):
        if widget.input.text.strip() == "":
            Utility.set_color(widget, error_color)
            error_callback({'message': error_msg})
            return False
        Utility.set_color(widget, success_color)
        return True

    @staticmethod
    def validate_birthday(widget, error_color, success_color, at_least_years_user, error_callback):
        birthday = widget.input.text.strip()
        try:
            birth_date = datetime.strptime(birthday, "%m/%d/%Y")
            current_date = datetime.now()

            if birth_date > current_date:
                Utility.set_color(widget, error_color)
                error_callback({'message': "Birthday cannot be a future date. Please enter a valid date."})
                return False

            # Ginawa atleast 3 years old. 
            age = (current_date - birth_date).days // 365
            if age < at_least_years_user:
                Utility.set_color(widget, error_color)
                error_callback({'message': f"You must be at least {at_least_years_user} years old to enter."})
                return False

            Utility.set_color(widget, success_color)
            return True

        except ValueError:
            # If date format is invalid
            Utility.set_color(widget, error_color)
            error_callback({'message': "Invalid date format. Please use MM/DD/YYYY."})
            return False

    @staticmethod
    def validate_email(widget, email_pattern, error_color, success_color, error_callback):
        email = widget.input.text.strip()
        if email == "":
            Utility.set_color(widget, error_color)
            error_callback({'message': "Email cannot be empty. Please enter a valid email address."})
            return False
        elif not re.match(email_pattern, email):
            Utility.set_color(widget, error_color)
            error_callback({'message': "Invalid email format. Please enter a valid email address."})
            return False
        Utility.set_color(widget, success_color)
        return True

    @staticmethod
    def validate_password(widget, confirm_widget, error_color, success_color, error_callback, check_strength=False):
        password = widget.input.text.strip()
        if password == "":
            Utility.set_color(widget, error_color)
            error_callback({'message': "Password cannot be empty. Please enter a valid password."})
            return False
        if check_strength and not Utility.is_strong_password(password):
            Utility.set_color(widget, error_color)
            error_callback({'message': "Password is too weak. It must be at least 8 characters long, include a mix of uppercase and lowercase letters, numbers, and special characters."})
            return False
        if confirm_widget.input.text.strip() != password:
            Utility.set_color(widget, error_color)
            Utility.set_color(confirm_widget, error_color)
            error_callback({'message': "Passwords do not match. Please ensure both passwords are identical."})
            return False
        Utility.set_color(widget, success_color)
        Utility.set_color(confirm_widget, success_color)
        return True
