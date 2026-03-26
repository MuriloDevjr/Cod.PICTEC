from dataclasses import field
import flet as ft
import cam

def main(page: ft.Page):
    page.title = "AquaScan"
    page.window_width = 900
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = "#0f172a"

    def show_login():
        page.controls.clear()

        email = ft.TextField(width=300, label="Email", border_radius=10)
        senha = ft.TextField(width=300, label="Senha", password=True, border_radius=10)

        def entrar(e):
            if email.value == "arroz" and senha.value == "mosca":
                show_dashboard()
            else:
                email.error_text = "Login inválido"
                page.update()

        login_card = ft.Container(
            width=380,
            padding=30,
            border_radius=20,
            bgcolor="#1e293b",
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("💧 AquaScan", size=30, weight=ft.FontWeight.BOLD),
                    ft.Text("Monitoramento Inteligente", size=14),
                    email,
                    senha,
                    ft.ElevatedButton("Entrar", width=300, on_click=entrar),
                ]
            )
        )

        page.add(login_card)

    def show_dashboard():
        page.controls.clear()

        resultado = ft.Text("Nenhuma análise realizada", size=16)

        def analisar(e):
            cam.teste()
            resultado.value = "Análise concluída"
            page.update()

        def show_analise_page(e=None):
            page.controls.clear()

            def card_item(nome):
                return ft.Container(
                    width=150,
                    height=120,
                    border_radius=15,
                    bgcolor="#1e293b",
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(nome, size=16, weight=ft.FontWeight.BOLD),
                            ft.ElevatedButton("Analisar", on_click=analisar)
                        ]
                    )
                )

            grid = ft.GridView(
                expand=True,
                runs_count=3,
                spacing=20,
                run_spacing=20,
                controls=[
                    card_item("pH"),
                    card_item("Amônia"),
                    card_item("Oxigênio"),
                    card_item("Nitrito"),
                    card_item("Amônia Crítica"),
                ]
            )

            page.add(
                ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Selecionar Análise", size=26, weight=ft.FontWeight.BOLD),
                        grid,
                        ft.ElevatedButton("Voltar", on_click=lambda e: show_dashboard())
                    ]
                )
            )

        sidebar = ft.Container(
            width=200,
            bgcolor="#1e3a8a",
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text("Menu", size=18, color="white"),
                    ft.Divider(),
                    ft.TextButton("Dashboard", on_click=lambda e: show_dashboard(), style=ft.ButtonStyle(color="white")),
                    ft.TextButton("Analisar", on_click=show_analise_page, style=ft.ButtonStyle(color="white")),
                    ft.TextButton("Sair", on_click=lambda e: show_login(), style=ft.ButtonStyle(color="white")),
                ]
            )
        )

        content = ft.Container(
            expand=True,
            padding=30,
            content=ft.Column(
                controls=[
                    ft.Text("Dashboard", size=28, weight=ft.FontWeight.BOLD),

                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=200,
                                height=120,
                                bgcolor="#1e293b",
                                border_radius=15,
                                content=ft.Column(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[ft.Text("Cadastrar")]
                                )
                            ),
                            ft.Container(
                                width=200,
                                height=120,
                                bgcolor="#1e293b",
                                border_radius=15,
                                content=ft.Column(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.ElevatedButton("Analisar", on_click=show_analise_page)
                                    ]
                                )
                            ),
                            ft.Container(
                                width=200,
                                height=120,
                                bgcolor="#1e293b",
                                border_radius=15,
                                content=ft.Column(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.ElevatedButton("Sair", on_click=lambda e: show_login())
                                    ]
                                )
                            ),
                        ],
                    ),

                    ft.Container(
                        margin=20,
                        padding=20,
                        border_radius=15,
                        bgcolor="#1e293b",
                        content=ft.Column(
                            controls=[
                                ft.Text("Resultado da Análise", size=18),
                                resultado
                            ]
                        )
                    )
                ]
            )
        )

        page.add(ft.Row([sidebar, content], expand=True))

    show_login()

ft.app(target=main)