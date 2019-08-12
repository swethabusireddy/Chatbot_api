from rbasis.urlrouter import router
from . import views

def RegPath():
    router.register(r'answer', views.answer, "answer", "")
