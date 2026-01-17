from django.contrib import admin

# Register your models here.
from .models import Quickadd
from .models import WordMastery
from .models import NewWord
admin.site.register(Quickadd)
admin.site.register(WordMastery)
admin.site.register(NewWord)
