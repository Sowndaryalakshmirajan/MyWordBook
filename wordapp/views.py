from django.shortcuts import render,redirect
from django.db import transaction

from django.contrib import messages
from .models import Quickadd
from .models import WordMastery
from .models import NewWord
# from pymongo import Mongoclient   
from bson import ObjectId
import base64
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["mywordbook"]
col = db["wordmastery"]


# from django.contrib import messages
# from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'index.html')

def addnewword(request):
    return render(request,'AddNewWord.html')
def home(request):
    if request.method=="POST":
        word=request.POST['word']
        meaning=request.POST['meaning']
        obj3=Quickadd()
        obj3.Word=word
        obj3.meaning=meaning
        obj3.save()
        # quickadd=Quickadd.objects.all()
        messages.success(request, '🏆 Excellent — you nailed it! 😎')
        return redirect('home') 
    return render(request,'index.html')
    
        
# from django.db import transaction
# def wordmastery(request):
#     quick_add = list(Quickadd.objects.all())
#     index = int(request.GET.get('i', 0))

#     # safety check
#     if index >= len(quick_add):
#         return redirect('home')

#     if request.method == "POST":
#         action = request.POST.get('form_action')

#         # 🔥 SAVE ALL QUICKADD WORDS
#         if action == "save":
#             with transaction.atomic():
#                 for q in quick_add:
#                     WordMastery.objects.create(
#                         Word=q.Word,
#                         Meaning=q.meaning,
#                         DeepMeaing=request.POST.get('deep_meaning', ''),
#                         ExampleSentence=request.POST.get('example', ''),
#                         Image=request.FILES.get('image')
#                     )
#             return redirect('home')

#         # 👉 NEXT button
#         return redirect(f"/wordmastery/?i={index+1}")

#     # 👇 GET request ALWAYS returns page
#     return render(request, 'wordMastery.html', {
#         'item': quick_add[index],
#         'index': index + 1,
#         'total': len(quick_add)
#     })
# from bson import ObjectId
# import base64

# import base64
# from django.shortcuts import render, redirect
# from pymongo import MongoClient
# from bson import ObjectId
# from .models import Quickadd

# client = MongoClient("mongodb://localhost:27017/")
# db = client["mywordbook"]
# col = db["wordmastery"]

import base64
from django.shortcuts import render, redirect
from pymongo import MongoClient
from bson import ObjectId
from .models import Quickadd

client = MongoClient("mongodb://localhost:27017/")
db = client["mywordbook"]
col = db["wordmastery"]

def wordmastery(request):
    quick_add = list(Quickadd.objects.all())
    total = len(quick_add)

    if total == 0:
        return redirect('home')

    index = int(request.GET.get('i', 0))
    index = max(0, min(index, total - 1))

    mongo_id = request.GET.get('mid', '')

    if request.method == "POST":
        action = request.POST.get('action')
        mongo_id = request.POST.get('mongo_id')
        quick_id = request.POST.get('quick_id')   # 👈 IMPORTANT

        # ✅ SAVE (MongoDB)
        if action == "save":
            image_file = request.FILES.get('image')
            image_base64 = None

            if image_file:
                image_base64 = base64.b64encode(
                    image_file.read()
                ).decode('utf-8')

            result = col.insert_one({
                "word": request.POST.get('word'),
                "meaning": request.POST.get('meaning'),
                "deep_meaning": request.POST.get('deep_meaning', ''),
                "example": request.POST.get('example', ''),
                "image": image_base64
            })

            mongo_id = str(result.inserted_id)

        # ❌ DELETE (MongoDB + Quickadd)
        if action == "delete":
            # MongoDB delete
            if mongo_id:
                col.delete_one({"_id": ObjectId(mongo_id)})

            # UI source delete (Quickadd)
            if quick_id:
                Quickadd.objects.filter(id=quick_id).delete()

            mongo_id = ''
            index = max(0, index - 1)   # 👈 index safe

        # ▶ NEXT
        if action == "next":
            index += 1

        # ◀ PREVIOUS
        if action == "prev":
            index -= 1

        return redirect(f"/wordmastery/?i={index}&mid={mongo_id}")

    return render(request, 'wordMastery.html', {
        'item': quick_add[index],
        'index': index + 1,
        'total': total,
        'mongo_id': mongo_id
    })



def newword(request):
    if request.method == "POST":
        word = request.POST.get("word")
        meaning = request.POST.get("meaning")
        deep_meaning = request.POST.get("deep_meaning")
        example = request.POST.get("example")

        image_file = request.FILES.get("image")
        image_base64 = None

        if image_file:
            image_base64 = base64.b64encode(
                image_file.read()
            ).decode("utf-8")

        col.insert_one({
            "word": word,
            "meaning": meaning,
            "deep_meaning": deep_meaning,
            "example": example,
            "image": image_base64
        })

        return redirect("home")

    return render(request, "newword.html")
def allwords(request):
    # def allwords(request):
    words = list(col.find())

    # 🔥 Mongo ObjectId & image ready panna
    for w in words:
        w["_id"] = str(w["_id"])   # ObjectId → string
        if w.get("image"):
            w["image"] = f"data:image/png;base64,{w['image']}"

    return render(request, "allwords.html", {
        "words": words
    })
    # return render(request,'allwords.html')
