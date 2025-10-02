from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("" , views.index , name = "index"),
    path("Missingitems" , views.Missingitems , name = "MissingItems"),
    path("AddItem" , views.AddItem , name = "AddItem"),
    path("ViewMessages", views.viewmessages, name = "viewmessages"),
    path("messages" , views.messages, name="messages"),
    path("Extmessage/<int:id>", views.MessageInDetail, name = "MessageinDetail"),
    path("ContactOwner/<int:id>", views.ContactOwner, name = "ContactOwner" ),
    path("SaveMessage" , views.SaveMessage , name="SaveMessage"),
    path("MarkAsFound" , views.found , name="MarkAsFound"),
    path("Reply" , views.Reply , name="reply"),
    path("ViewsentMessages", views.viewsentmessages, name = "viewsentmessages"),
    path("sentmessages", views.sentmessages , name="sentmessages"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)