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

        def card_item(nome, imagem_path, cor_borda="#9333ea"):
            def analisar_especifico(e):
                # Aqui você pode adicionar lógica específica para cada análise
                print(f"Analisando {nome}")
                # Exemplo: abrir página de análise específica
                # show_analise_detalhes(nome)
            
            return ft.Container(
                width=150,
                height=120,
                border_radius=15,
                border=ft.border.all(3, cor_borda),
                clip_behavior=ft.ClipBehavior.HARD_EDGE,  # Importante!
                
                content=ft.Stack(
                    controls=[
                        # 1️⃣ Imagem de fundo
                        ft.Image(
                            src=imagem_path,
                            width=150,
                            height=120,
                            fit="cover",
                        ),
                        
                        # 2️⃣ Overlay escuro para legibilidade
                        ft.Container(
                            width=150,
                            height=120,
                            bgcolor="#000000",
                            opacity=0.45,  # Ajuste entre 0.3 e 0.6
                        ),
                        
                        # 3️⃣ Conteúdo (texto + botão)
                        ft.Container(
                            width=150,
                            height=120,
                            padding=10,
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        nome, 
                                        size=14, 
                                        weight=ft.FontWeight.BOLD,
                                        color="#ffffff",
                                        text_align=ft.TextAlign.CENTER,
                                        max_lines=2,  # Permite quebra de linha
                                    ),
                                    ft.ElevatedButton(
                                        "Analisar",
                                        on_click=analisar_especifico,
                                        bgcolor=cor_borda,
                                        color="#ffffff",
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=8)
                                        )
                                    )
                                ]
                            )
                        )
                    ]
                )
            )

        grid = ft.GridView(
            expand=True,
            runs_count=3,
            spacing=20,
            run_spacing=20,
            controls=[
                card_item("pH", "assets/ph_analise.svg", "#3b82f6"),
                card_item("Amônia", "assets/amonia_analise.svg", "#22c55e"),
                card_item("Oxigênio", "assets/oxigenio_analise.svg", "#06b6d4"),
                card_item("Nitrito", "assets/nitrito_analise.svg", "#a855f7"),
                card_item("Amônia Crítica", "assets/amonia_critica_analise.svg", "#ef4444"),
            ]
        )

        page.add(grid)
        page.update()

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