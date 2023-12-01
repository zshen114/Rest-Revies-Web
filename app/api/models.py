from django.contrib.auth import get_user_model
from django.db import models
from api.helpers import generate_code

User = get_user_model()

CATEGORY_CHOICES = (('Asian', 'Asian'), ('Italian', 'Italian'),
                    ('Swiss', 'Swiss'), ('Greek', 'Greek'),)

RATING_CHOICES = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))


class UserProfile(models.Model):
    user = models.OneToOneField(
        verbose_name='user',
        to=User,
        on_delete=models.CASCADE,
        related_name='user_profile'
    )
    location = models.CharField(null=True, blank=True, max_length=30)
    phone = models.CharField(null=True, blank=True, max_length=30)
    bio = models.CharField(max_length=300, blank=True)
    interests = models.CharField(null=True, blank=True, max_length=30)
    profile_pic = models.ImageField(null=True, blank=True)
    member_since = models.DateTimeField(auto_now=True)
    code = models.CharField(
        verbose_name='code',
        max_length=255,
        default=generate_code,
    )

    def generate_new_code(self):
        self.code = generate_code()
        self.save()
        return self.code

    def __str__(self):
        return self.user.username


class Restaurant(models.Model):

    name = models.CharField(blank=False, null=False, max_length=15)
    category = models.CharField(
        blank=False, null=False,
        max_length=15,
        choices=CATEGORY_CHOICES
    )
    country = models.CharField(blank=False, null=False, max_length=30)
    street = models.CharField(blank=False, null=False, max_length=30)
    city = models.CharField(blank=False, null=False, max_length=30)
    zip = models.CharField(null=True, blank=True, max_length=30)
    website = models.CharField(null=True, blank=True, max_length=30)
    phone = models.CharField(null=True, blank=True, max_length=30)
    email = models.CharField(null=True, blank=True, max_length=30)
    opening_hours = models.CharField(null=True, blank=True, max_length=30)
    price_level = models.IntegerField(null=True, blank=True)
    restaurant_pic = models.ImageField(null=True, blank=True, max_length=30)
    restaurant_owner = models.ForeignKey(
        verbose_name='restaurant_owner',
        related_name='owned_restaurants',
        to=User,
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Comment(models.Model):

    author = models.ForeignKey(
        to=User,
        verbose_name='User',
        on_delete=models.CASCADE,
        related_name='authors'
    )
    restaurant = models.ForeignKey(
        to=Restaurant,
        verbose_name='Restaurant',
        on_delete=models.CASCADE,
        related_name='restaurants'
    )
    body = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True, blank=True)
    rating = models.IntegerField(
        verbose_name='rating',
        default=0,
        choices=RATING_CHOICES
    )

    def __str__(self):
        return f"{str(self.author).upper()} Commented for {str(self.restaurant).upper()}"


class Reaction(models.Model):
    class Meta:
        unique_together = (('user_reacted', 'comment'),)

    user_reacted = models.ForeignKey(
        to=User,
        verbose_name='User',
        on_delete=models.CASCADE,
        related_name='users_reacted')
    comment = models.ForeignKey(
        to=Comment,
        verbose_name='Comment',
        on_delete=models.CASCADE,
        related_name='comments')

    def __str__(self):
        return f"{str(self.user_reacted).upper()} Liked: {self.comment}"

