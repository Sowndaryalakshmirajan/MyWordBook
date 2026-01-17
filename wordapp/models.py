from django.db import models

# Create your models here.

class Quickadd(models.Model):
    Word=models.CharField(max_length=100)
    meaning=models.TextField()

class WordMastery(models.Model):
    Word=models.CharField(max_length=100)
    Meaning=models.TextField()
    DeepMeaing=models.TextField()
    ExampleSentence=models.TextField()
    Image=models.ImageField()

class NewWord(models.Model):
    Word=models.CharField(max_length=100)
    Meaning=models.TextField()
    DeepMeaing=models.TextField()
    ExampleSentence=models.TextField()
    Image=models.ImageField()
    
    