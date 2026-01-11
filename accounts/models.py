from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinLengthValidator
from django.core.exceptions import ValidationError

def validate_image_size(image):
    max_size = 2 * 1024 * 1024  
    if image.size > max_size:
        raise ValidationError("Image file size must be less than 2 MB")

class User(AbstractUser):
    username = models.CharField(
        primary_key=True,
        max_length=15,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message='Username can only contain letters, numbers, and underscores'
            ),
            MinLengthValidator(3, message='Username must be at least 3 characters long')
        ]
    )
    name = models.CharField(
        max_length=50,
        validators=[
            MinLengthValidator(1, message='Name must be at least 1 character long')
        ]
    )
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, max_length=160)
    avatar = models.ImageField(
        upload_to="avatars/", 
        blank=True, 
        null=True, 
        validators=[validate_image_size]
    )
    banner = models.ImageField(
        upload_to="banners/", 
        blank=True, 
        null=True, 
        validators=[validate_image_size]
    )
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    follower_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=30, blank=True)
    website = models.URLField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"@{self.username}"
    
    def save(self, *args, **kwargs):
        if self.pk:
            try:
                original = User.objects.get(pk=self.pk)
                if original.username != self.username:
                    raise ValidationError("Username cannot be changed after creation")
            except User.DoesNotExist:
                # Happens during createsuperuser & some admin operations
                pass

        if self.username:
            self.username = self.username.lower()

        super().save(*args, **kwargs)

    
    def clean(self):
        super().clean()
        if self.username:
            
            reserved_usernames = {
                'admin', 'root', 'api', 'settings', 'help', 
                'support', 'about', 'privacy', 'terms', 'login',
                'signup', 'logout', 'profile', 'home', 'search'
            }
            if self.username.lower() in reserved_usernames:
                raise ValidationError({'username': 'This username is reserved'})
class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        to_field='username'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        to_field='username',  
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following' )
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower} → {self.following}"