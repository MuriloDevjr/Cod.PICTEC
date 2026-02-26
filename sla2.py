import flet as ft

def main(page: ft.Page):
    page.title = "AquaScan"
    page.window_width = 900
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def show_login():
        page.controls.clear()

        email = ft.TextField(width=300, label="Email")
        senha = ft.TextField(width=300, label="Senha", password=True)

        def entrar(e):
            if email.value != "" and senha.value != "":
                show_dashboard()

        login_card = ft.Container(
            width=400,
            padding=30,
            border_radius=15,
            bgcolor=ft.colors.WHITE,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("AquaScan", size=28, weight=ft.FontWeight.BOLD),
                    ft.Text("Monitoramento Inteligente da Água", size=14),
                    email,
                    senha,
                    ft.ElevatedButton(
                        "Entrar",
                        width=300,
                        on_click=entrar
                    )
                ]
            )
        )

        page.add(login_card)

    def show_dashboard():
        page.controls.clear()

        resultado = ft.Text("Nenhuma análise realizada", size=16)

        def analisar(e):
            resultado.value = "Resultado: Qualidade da água = 0.02 mg/L"
            page.update()

        sidebar = ft.Container(
            width=200,
            bgcolor=ft.colors.BLUE_700,
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text("Menu", color=ft.colors.WHITE, size=18),
                    ft.Divider(color=ft.Colors.WHITE),
                    ft.TextButton("Dashboard", style=ft.ButtonStyle(color=ft.colors.WHITE)),
                    ft.TextButton("Analisar Água", style=ft.ButtonStyle(color=ft.colors.WHITE)),
                    ft.TextButton("Sair", style=ft.ButtonStyle(color=ft.colors.WHITE), on_click=lambda e: show_login())
                ]
            )
        )

        content = ft.Container(
            expand=True,
            padding=30,
            content=ft.Column(
                controls=[
                    ft.Text("Dashboard", size=26, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        padding=20,
                        border_radius=10,
                        bgcolor=ft.Colors.BLUE_50,
                        content=ft.Column(
                            controls=[
                                ft.Text("Análise de Qualidade da Água", size=18),
                                ft.ElevatedButton(
                                    "Iniciar Análise",
                                    on_click=analisar
                                ),
                                resultado
                            ]
                        )
                    )
                ]
            )
        )

        page.add(
            ft.Row(
                expand=True,
                controls=[
                    sidebar,
                    content
                ]
            )
        )

    show_login()

ft.app(target=main)