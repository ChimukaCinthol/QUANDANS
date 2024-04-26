import time
import flet as ft
from flet_core import MainAxisAlignment

from views.home import home_page
from create_account import create_account_page
from Database.logInDatabase import DatabaseManager


def main(page: ft.Page):
    page.title = "QUANDANS study assistant app"


    user_name = ft.Ref[ft.TextField]()
    email_address = ft.Ref[ft.TextField]()
    password = ft.Ref[ft.TextField]()
    feedback = ft.Ref[ft.Text]()

    def verify_log_in(e):
        if user_name.current.value != "" and email_address.current.value != "" and password.current.value != "":

            #checking if user exists in the database
            database_manager = DatabaseManager(db_name="log_in_database")
            database_manager.create_table()
            db_response = database_manager.check_user(username=user_name.current.value,
                                                      email=email_address.current.value,
                                                      password=password.current.value
                                                      )
            print(db_response)
            #db_response can either be true or false
            if db_response:
               feedback.current.value = "Log in successful"
               feedback.current.color = "blue"
               database_manager.close()
               time.sleep(1.4)
               page.go("/second_home")
            else:
                feedback.current.value = "No user with provided details found! "
                feedback.current.color = "red"
                page.update()
                time.sleep(2)
                feedback.current.value = ""
                page.update()
        else:
            feedback.current.value = "Provide your details!"
            feedback.current.color = "red"
            user_name.on_focus = True
        page.update()

    forgot_password_create_account = ft.Row(
        controls=[
            ft.IconButton(icon=ft.icons.PASSWORD_ROUNDED, highlight_color="white", tooltip="forgot password"),
            ft.IconButton(icon=ft.icons.VERIFIED_USER_SHARP, highlight_color="white", tooltip="create account",
                          on_click=lambda _: page.go("/create_account_page")
            )
        ]
    )

    log_in_controls = ft.Column(
        controls=[
            ft.TextField(ref=user_name, label="User name", width=300, bgcolor=ft.colors.WHITE, color=ft.colors.BLACK54),
            ft.TextField(ref=email_address, label="Email address", width=300, bgcolor=ft.colors.WHITE,
                         color=ft.colors.BLACK54),
            ft.TextField(ref=password, label="Password", width=300, bgcolor=ft.colors.WHITE, color=ft.colors.BLACK54),
            ft.Text(ref=feedback, value=""),
            forgot_password_create_account,
            ft.OutlinedButton(text="Log In", on_click=verify_log_in)
        ]
    )
    '''
     for custom border use the code snippet below

       border=ft.border.Border(
                left=ft.border.Side(2, "red"),  # Set the left border color to red
                right=ft.border.Side(2, "blue"),  # Set the right border color to blue
                top=ft.border.Side(2, "green"),  # Set the top border color to green
                bottom=ft.border.Side(2, "yellow"),  # Set the bottom border color to yellow
      ),
    '''
    ft.AppBar(title=ft.Text("Quandans log in portal"), bgcolor=ft.colors.SURFACE_VARIANT),
    log_in_controls_container = ft.Container(
        width=350,
        height=450,
        bgcolor=ft.colors.TEAL,
        border=ft.border.all(width=0, color="white"),
        border_radius=10,
        padding=ft.padding.only(top=20, right=15, bottom=20, left=15),

        content=ft.Stack(
            controls=[
                log_in_controls,
            ]
        )
    )
    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                route="/",
                controls=[
                    log_in_controls_container
                ],
            )
        )
        if page.route == "/second_home":
            token="2edhdnddbcvc"
            page.views.append(
                ft.View(
                    route=f"/second_home{token}",
                    controls=[
                        ft.AppBar(title=ft.Text("SECOND HOME PAGE"), bgcolor=ft.colors.SURFACE_VARIANT),
                        home_page(page, token),
                        ft.ElevatedButton(text="LOG OUT", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        if page.route == "/create_account_page":
            page.views.append(
                ft.View(
                    route="/create_account_page",
                    controls=[
                        ft.AppBar(title=ft.Text("Create Account Page"), bgcolor=ft.colors.SURFACE_VARIANT),
                        create_account_page(page),
                        ft.ElevatedButton(text="LOG OUT", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main, view=ft.WEB_BROWSER)
