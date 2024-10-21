from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Friend)
admin.site.register(News)
admin.site.register(Event)
admin.site.register(Books)
admin.site.register(ChatMessage)
admin.site.register(Complain)
admin.site.register(CommunityForm)