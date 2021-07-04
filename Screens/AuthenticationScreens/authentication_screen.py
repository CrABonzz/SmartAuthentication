import smtplib
from abc import ABCMeta, abstractmethod
from email.mime.text import MIMEText
from tkinter import Label, Button

from Screens import login
from Utils.common import ADMIN_PASSWORD, ADMIN_MAIL, MAX_FAILED_LOGIN_ATTEMPTS
from Utils.json_utils import update_failed_login
from Utils.tkinter_utils import destroy_screens, add_screen


class AuthScreen(object, metaclass=ABCMeta):
    """
    Interface for any screen performing user authentication
    """

    @abstractmethod
    def __init__(self, auth):
        """
        :param auth: Verifier class
        :type auth: Authenticator
        """
        super(AuthScreen, self).__init__()
        self.authenticator = auth

        self.password_not_recog_screen = None

    @abstractmethod
    def screen(self):
        """
        :return: The handle to the screen
        """
        pass

    @abstractmethod
    def password(self):
        """
        :return: The raw password
        """
        pass

    @abstractmethod
    def handle_register(self, register_screen):
        """
        This screen register page
        :param register_screen: The register screen
        :type register_screen: <class 'tkinter.Toplevel'><class 'tkinter.Toplevel'>
        """
        pass

    @abstractmethod
    def handle_login(self, login_screen, username, email):
        """
        This screen login page
        :param login_screen: The login screen
        :type login_screen: <class 'tkinter.Toplevel'><class 'tkinter.Toplevel'>
        :param username: Username of the failed user
        :type username: str
        :param email: Email of the failed user
        :type email: str
        """
        pass

    def _password_not_recognised(self, login_screen):
        self.password_not_recog_screen = add_screen(login_screen, "Invalid password", "150x100")

        Label(self.password_not_recog_screen, text="Invalid Password ").pack()
        Button(self.password_not_recog_screen, text="OK",
               command=lambda: destroy_screens(self.password_not_recog_screen)).pack()

    def _login_failed(self, login_screen, username, email):
        """
        :param login_screen: The login screen
        :type login_screen: <class 'tkinter.Toplevel'><class 'tkinter.Toplevel'>
        :param username: Username of the failed user
        :type username: str
        :param email: Email of the failed user
        :type email: str
        """
        login.login_success = False

        update_failed_login(username, email)

        self._notify_user_mail(username, email)
        self._password_not_recognised(login_screen)

    def _notify_user_mail(self, username, email):
        body_of_email = username + " Failed login attempt to your user"
        sender = "smart_authentication@gmail.com"
        receivers = [email]

        msg = MIMEText(body_of_email, "html")
        msg["Subject"] = username + " many failed login attempts"
        msg["From"] = sender
        msg["To"] = ", ".join(receivers)

        s = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)
        s.login(user=ADMIN_MAIL, password=ADMIN_PASSWORD)
        s.sendmail(sender, receivers, msg.as_string())
        s.quit()
