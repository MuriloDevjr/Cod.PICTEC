import flet as ft
import cam
from datetime import datetime
import pandas as pd
import threading

def main(page: ft.Page):
    page.title = "AquaScan"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 700
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.BLUE_GREY_900

    # ---------------- HISTÓRICO ----------------
    def salvar_historico(tipo, resultado):
        try:
            df = pd.read_csv("historico.csv")
        except:
            df = pd.DataFrame(columns=["Data", "Hora", "Tipo", "Resultado"])

        agora = datetime.now()
        novo = {
            "Data": agora.strftime("%d/%m/%Y"),
            "Hora": agora.strftime("%H:%M"),
            "Tipo": tipo,
            "Resultado": resultado
        }

        df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
        df.to_csv("historico.csv", index=False)

    def carregar_historico():
        page.controls.clear()
        try:
            df = pd.read_csv("historico.csv")
            historico_textos = []
            for _, row in df.iterrows():
                historico_textos.append(f"{row['Tipo']} | {row['Resultado']} ({row['Hora']} {row['Data']})")
            return historico_textos
        except:
            return []

    # ---------------- TELA INICIAL ----------------
    def tela_inicial():
        page.controls.clear()
        page.add(
            ft.Column(
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Image(src="src/drop.png", width=100, height=100),
                    ft.Text("AquaScan", size=38, weight=ft.FontWeight.BOLD),
                    ft.Text("Monitoramento Inteligente da Água", size=16),
                    ft.ElevatedButton("Entrar", on_click=lambda e: tela_login())
                ]
            )
        )

    # ---------------- LOGIN ----------------
    def tela_login():
        page.controls.clear()

        email = ft.TextField(label="email", width=300)
        senha = ft.TextField(label="senha", password=True, width=300)

        def entrar(e):
            if email.value and senha.value:
                tela_dashboard()

        page.add(
            ft.Column(
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Login", size=30, weight=ft.FontWeight.BOLD),
                    email,
                    senha,
                    ft.ElevatedButton("Entrar", on_click=entrar),
                    ft.TextButton("Voltar", on_click=lambda e: tela_inicial())
                ]
            )
        )

    # ---------------- DASHBOARD ----------------
    def tela_dashboard():
        page.controls.clear()

        # Feed de análises
        analises_controles = ft.Column(spacing=5, scroll="auto")
        historico = carregar_historico()
        # mostrar mais recente em cima
        texto = reversed(historico)

        def analisar(tipo):
            def func():
                resultado = cam.analisarTipo(tipo)
                agora = datetime.now()
                texto_completo = f"{tipo} | {resultado} ({agora.strftime('%H:%M %d/%m/%Y')})"
                salvar_historico(tipo, resultado)
                analises_controles.controls.insert(0, ft.Text(texto_completo))
                page.update()
            threading.Thread(target=func).start()
            analises_controles.controls.insert(0, ft.Text(f"{tipo} | Aguardando captura..."))
            page.update()

        def card(nome, imagem_url):
            return ft.Container(
                width=160,
                height=170,
                bgcolor=ft.Colors.BLUE_GREY_800,
                border_radius=20,
                padding=10,
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK54),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Image(src=imagem_url, width=50, height=50),
                        ft.Text(nome, size=18, weight=ft.FontWeight.BOLD),
                        ft.ElevatedButton(
                            "Analisar",
                            style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE),
                            on_click=lambda e: analisar(nome.lower(), temp)
                        )
                    ]
                )
            )

        page.add(
            ft.Column(
                spacing=15,
                controls=[
                    ft.Text("Dashboard", size=28, weight=ft.FontWeight.BOLD),
                    analises_controles,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            card("pH", "src/ph.png"),
                            card("Amonia", "src/amonia.png"),
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            card("Oxigenio", "src/oxigenio.png"),
                            card("Nitrito", "src/nitrato (1).png"),
                        ]
                    ),
                    ft.ElevatedButton("Sair", on_click=lambda e: tela_inicial())
                ]
            )
        )
        page.update()
        ft.Text(texto)

    # inicia app
    tela_inicial()
    page.update()


ft.app(target=main)