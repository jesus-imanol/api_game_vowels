from django.db import models

class Animal(models.Model):
    VOWEL_CHOICES = [
        ('a', 'A'),
        ('e', 'E'),
        ('i', 'I'),
        ('o', 'O'),
        ('u', 'U'),
    ]
    
    name = models.CharField(max_length=100)
    starting_vowel = models.CharField(max_length=1, choices=VOWEL_CHOICES)
    image = models.ImageField(upload_to='animals/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    difficulty = models.IntegerField(default=1)
    animals = models.ManyToManyField(Animal, related_name='levels')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['difficulty', 'name']
    
    def __str__(self):
        return f"{self.name} (Nivel {self.difficulty})"

class UserProgress(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='progress')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='user_progress')
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    last_played = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'level']
        ordering = ['-last_played']
    
    def __str__(self):
        return f"{self.user.username} - {self.level.name} - {self.score}%"

class CustomAnimalImage(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='custom_animals')
    name = models.CharField(max_length=100)
    starting_vowel = models.CharField(max_length=1, choices=Animal.VOWEL_CHOICES)
    image = models.ImageField(upload_to='custom_animals/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"