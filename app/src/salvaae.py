import flet as ft
import cam
from datetime import datetime
import pandas as pd
import threading


def main(page: ft.Page):
    page.title = "AquaScan"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 420
    page.window_height = 760
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.BLUE_GREY_900
    page.padding = 0

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
            "Resultado": resultado,
        }

        df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
        df.to_csv("historico.csv", index=False)

    def carregar_historico():
        try:
            df = pd.read_csv("historico.csv")
            itens = []

            for _, row in df.iloc[::-1].iterrows():
                itens.append({
                    "tipo": str(row["Tipo"]),
                    "resultado": str(row["Resultado"]),
                    "hora": str(row["Hora"]),
                    "data": str(row["Data"]),
                })

            return itens
        except:
            return []

    def tela_inicial():
        page.controls.clear()

        page.add(
            ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                controls=[
                    ft.Image(src="drop.png", width=110, height=110),
                    ft.Text("AquaScan", size=40, weight=ft.FontWeight.BOLD),
                    ft.Text("Monitoramento Inteligente da Água"),
                    ft.Button(
                        "Entrar",
                        on_click=lambda e: tela_login()
                    )
                ]
            )
        )

        page.update()

    def tela_login():
        page.controls.clear()

        email = ft.TextField(label="E-mail", width=300)
        senha = ft.TextField(label="Senha", password=True, width=300)

        def entrar(e):
            if email.value and senha.value:
                tela_dashboard()

        page.add(
            ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                controls=[
                    ft.Text("Login", size=30),
                    email,
                    senha,
                    ft.Button("Entrar", on_click=entrar),
                    ft.TextButton(
                        "Voltar",
                        on_click=lambda e: tela_inicial()
                    )
                ]
            )
        )

        page.update()

    def tela_dashboard():
        page.controls.clear()

        historico_lista = ft.ListView(
            spacing=6,
            padding=10,
            auto_scroll=False
        )

        status_text = ft.Text("", size=14)

        # ===== VER MAIS / VER MENOS =====
        historico_expandido = [False]

        historico_container = ft.Container(
            height=150,
            content=historico_lista
        )

        btn_toggle = ft.TextButton("Ver mais")

        def toggle(e):
            historico_expandido[0] = not historico_expandido[0]

            if historico_expandido[0]:
                historico_container.height = 300
                btn_toggle.text = "Ver menos"
            else:
                historico_container.height = 150
                btn_toggle.text = "Ver mais"

            page.update()

        btn_toggle.on_click = toggle
        # =================================

        def rebuild_historico():
            historico_lista.controls.clear()

            itens = carregar_historico()

            if not itens:
                historico_lista.controls.append(
                    ft.Text("Nenhuma análise ainda.")
                )

            for item in itens:
                historico_lista.controls.append(
                    ft.Text(
                        f"{item['tipo']} | {item['resultado']} | {item['hora']} {item['data']}"
                    )
                )

            page.update()

        def executar_analise(tipo, temp=None):
            status_text.value = f"Analisando {tipo.upper()}..."
            page.update()

            def rodar():
                try:
                    resultado = cam.analisarTipo(tipo, temp)
                except Exception as ex:
                    resultado = f"Erro: {ex}"

                status_text.value = f"{tipo.upper()}: {resultado}"
                salvar_historico(tipo, resultado)
                rebuild_historico()
                page.update()

            threading.Thread(target=rodar, daemon=True).start()

        campo_temp = ft.TextField(label="Temperatura (°C)", width=260, keyboard_type=ft.KeyboardType.NUMBER)

        def fechar_dlg(e):
            dlg.open = False
            page.update()

        def confirmar_temp(e):
            if not campo_temp.value:
                campo_temp.error_text = "Digite a temperatura"
                page.update()
                return
            
            valor = campo_temp.value
            dlg.open = False
            page.update()
            executar_analise(dlg.data, valor)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Temperatura da Água"),
            content=campo_temp,
            actions=[
                ft.TextButton("Cancelar", on_click=fechar_dlg),
                ft.Button("Confirmar", on_click=confirmar_temp),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = dlg

        def pedir_temperatura(tipo):
            campo_temp.value = ""
            campo_temp.error_text = None
            dlg.data = tipo 
            dlg.open = True
            page.update()

        def ao_clicar_card(nome):
            nome_lower = nome.lower()

            if(nome_lower == "amonia"):
                pedir_temperatura(nome_lower)
            else:
                executar_analise(nome_lower)
                page.update()

        def card(nome, imagem_url):
            return ft.Container(
                width=170,
                height=175,
                bgcolor=ft.Colors.BLUE_GREY_800,
                border_radius=20,
                padding=12,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Image(src=imagem_url, width=48, height=48),
                        ft.Text(nome, size=17),
                        ft.Button(
                            "Analisar",
                            on_click=lambda e, n=nome: ao_clicar_card(n)
                        )
                    ]
                )
            )

        page.add(
            ft.Column(
                controls=[
                    ft.Text("Dashboard", size=26),
                    status_text,

                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text("Histórico"),
                            btn_toggle
                        ]
                    ),
                    historico_container,

                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            card("pH", "ph.png"),
                            card("Amonia", "amonia.png")
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            card("Oxigenio", "oxigenio.png"),
                            card("Nitrito", "nitrato (1).png")
                        ]
                    )
                ]
            )
        )

        rebuild_historico()
        page.update()

    tela_inicial()


ft.run(main)