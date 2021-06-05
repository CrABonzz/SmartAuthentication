import smtplib
from abc import ABCMeta, abstractmethod
from email.mime.text import MIMEText
from tkinter import Label, Button

from Screens import login
from Utils.common import ADMIN_PASSWORD, ADMIN_MAIL
from Utils.json_utils import update_failed_login
from Utils.tkinter_utils import destroy_screens, add_screen


class IAuthScreen(object, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, auth):
        super(IAuthScreen, self).__init__()
        self.authenticator = auth

        self.password_not_recog_screen = None

    @abstractmethod
    def screen(self):
        pass

    @abstractmethod
    def password(self):
        pass

    @abstractmethod
    def handle_register(self, register_screen):
        pass

    @abstractmethod
    def handle_login(self, login_screen, username, email):
        pass

    def _password_not_recognised(self, login_screen):
        self.password_not_recog_screen = add_screen(login_screen, "Invalid password", "150x100")

        Label(self.password_not_recog_screen, text="Invalid Password ").pack()
        Button(self.password_not_recog_screen, text="OK",
               command=lambda: destroy_screens(self.password_not_recog_screen)).pack()

    def _login_failed(self, login_screen, username, email):
        login.login_success = False

        update_failed_login(username, email)

        self._notify_user_mail(username, email)
        self._password_not_recognised(login_screen)

    def _notify_user_mail(self, username, email):
        # TODO: not every failed. but once in 5 failures...?
        body_of_email = username + "Failure on entering user "
        sender = "smart_authentication@gmail.com"
        receivers = ["b281055@gmail.com"]

        msg = MIMEText(body_of_email, "html")
        msg["Subject"] = username + " many failed login attempts"
        msg["From"] = sender
        msg["To"] = ", ".join(receivers)

        s = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)
        s.login(user=ADMIN_MAIL, password=ADMIN_PASSWORD)
        s.sendmail(sender, receivers, msg.as_string())
        s.quit()
