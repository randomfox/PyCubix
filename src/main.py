from app import App
from settings import Settings

filename = 'cfg/settings.json'
settings = Settings()
settings.load(filename)

app = App(settings)
app.run()
