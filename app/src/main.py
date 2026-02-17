from dataclasses import field
import flet as ft

@ft.control
class Button(ft.Button):
    expand: int = field(default_factory=lambda: 1)


@ft.control
class LoginButton(Button):
    bgcolor: ft.Colors = ft.Colors.BLUE_700
    color: ft.Colors = ft.Colors.BLACK

@ft.control
class RegisterButton(Button):
    bgcolor: ft.Colors = ft.Colors.BLUE_GREY
    color: ft.Colors = ft.Colors.BLACK

@ft.control
class loginPage(ft.Container):
    def init(self):
        self.width = 500
        self.height = 100
        
        self.content = ft.Column(
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Row(
                    controls=[
                        LoginButton(content = "Login"),
                        RegisterButton(content = "Register")
                    ]
                )
            ]
        )

def main(page: ft.Page):

    page.title = "App"
    log = loginPage()

    page.add(log)


ft.run(main)
