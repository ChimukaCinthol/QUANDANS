from string import ascii_letters
import flet as ft
import time
from Database.logInDatabase import DatabaseManager


def create_account_page(page: ft.Page):
    user_name = ft.Ref[ft.TextField]()
    email_address = ft.Ref[ft.TextField]()
    password = ft.Ref[ft.TextField]()
    password_two = ft.Ref[ft.TextField]()
    feedback = ft.Ref[ft.Text]()

    def filter_input(un, ea, p, pt):
        """
        :param un: Username entered by the user
        :param ea: Email address entered by the user
        :param p: password entered by the user
        :param pt: password two entered by the user
        :return: is a string that say the conditions
        """
        try:
            if f"{ea[-10:-1]}{ea[-1]}" == "@gmail.com" or f"{ea[-10:-1]}{ea[-1]}" == "@yahoo.com" and un.isalpha():
                return "Email address, password and user name entered are valid"
            elif f"{ea[-10:-1]}{ea[-1]}" != "@gmail.com" or f"{ea[-10:-1]}{ea[-1]}" != "@yahoo.com":
                return "Email address used is not supported .Instead use '@gmail.com' or '@yahoo.com'"
            elif p != pt:
                return "Passwords don't match "
        except IndexError:
            print("Handle the error in filter function")

    def add_new_user(e):
        un = user_name.current.value
        ea = email_address.current.value
        p = password.current.value
        pt = password_two.current.value
        datamanager = DatabaseManager(db_name="log_in_database")
        if un != "" and ea != "":
            fd = filter_input(un, ea, p, pt)
            if fd == "Email address, password and user name entered are valid":
                #When lauching the appication the password should be hashed and salted
                datamanager.insert_user(username=un, email=ea, password=pt)
            elif fd == "Passwords don't match ":
                feedback.current.value = "Passwords don't match "
                page.update()
            elif fd == "Email address used is not supported .Instead use '@gmail.com' or '@yahoo.com'":
                feedback.current.value = "Use '@gmail.com' or '@yahoo.com'"
                page.update()
        else:
            feedback.current.value = "Fields can't be null"
            page.update()

    create_account_controls = ft.Column(
        controls=[
            ft.TextField(ref=user_name, label="User name", width=300, bgcolor=ft.colors.WHITE, color=ft.colors.BLACK54),
            ft.TextField(ref=email_address, label="Email address", width=300, bgcolor=ft.colors.WHITE,
                         color=ft.colors.BLACK54),
            ft.TextField(ref=password, label="Password", width=300, bgcolor=ft.colors.WHITE, color=ft.colors.BLACK54),
            ft.TextField(ref=password_two, label="Re-enter password", width=300, bgcolor=ft.colors.WHITE,
                         color=ft.colors.BLACK54),
            ft.Text(ref=feedback, value=""),
            ft.OutlinedButton(text="Create Account", on_click=add_new_user)
        ]
    )
    create_account_controls_container = ft.Container(
        width=350,
        height=450,
        bgcolor=ft.colors.TEAL,
        border=ft.border.all(width=0, color="white"),
        border_radius=10,
        padding=ft.padding.only(top=20, right=15, bottom=20, left=15),
        content=ft.Stack(
            controls=[create_account_controls]
        )
    )

    return create_account_controls_container
