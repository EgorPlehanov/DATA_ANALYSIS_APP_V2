from app import DataAnalysisApp

from flet import Page, app, AppView


def main(page: Page):
    page.title = "Data Analysis App"
    page.padding = 0
    app = DataAnalysisApp(page)
    page.add(app)
    page.update()

app(target=main)#, view=AppView.WEB_BROWSER)


'''
=============================
|     ЗАПУСК ПРИЛОЖЕНИЯ     |
=============================
venv\Scripts\activate
flet run .\main.py -d
=============================
'''