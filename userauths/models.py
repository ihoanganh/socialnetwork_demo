from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from shortuuid.django_fields import ShortUUIDField
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.utils.html import mark_safe
import shortuuid

GENDER = (
    ("male","Male"),
    ("female","Female")
)

RELATIONSHIP = (
    ("single","Single"),
    ("married","Married"),
    ("inlove","In Love"),
)

def user_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (instance.user.id, ext)
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class User(AbstractUser):
    full_name = models.CharField(max_length=200, null=True, blank=True) 
    username = models.TextField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    gender =  models.CharField(max_length=100, choices=GENDER, null=True, blank=True)
    
    otp = models.CharField(max_length=10, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return str(self.username)
    
    
    
class Profile(models.Model):
    pid = ShortUUIDField(length=7, max_length=25, alphabet='abcdefghijklmnopqrstuvwxyz')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True, default="default.jpg")
    cover_image = models.ImageField(upload_to=user_directory_path,null=True, blank=True , default="cover.jpg")
    full_name = models.CharField(max_length=200, null=True, blank=True) 
    phone = models.CharField(max_length=200, null=True, blank=True)
    gender =  models.CharField(max_length=100, choices=GENDER, default='male')
    relationship =  models.CharField(max_length=100, choices=RELATIONSHIP, default='single')
    bio = models.CharField(max_length=200, null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    working_at = models.CharField(max_length=200, null=True, blank=True)
    instagram = models.CharField(max_length=200, null=True, blank=True)
    whatsapp = models.CharField(max_length=200, null=True, blank=True)
    verified = models.BooleanField(default=False)
    followers = models.ManyToManyField(User, blank=True, related_name="followers")
    following = models.ManyToManyField(User, blank=True, related_name="following")
    friends = models.ManyToManyField(User, blank=True, related_name="friends")
    blocked = models.ManyToManyField(User, blank=True, related_name="blocked")
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    # def __str__(self):
    #     # if self.full_name != "" or self.full_name != None:
    #     #     return self.full_name
    #     return self.user.username
        
    # def save(self, *args, **kwargs):
    #     if self.slug == ""  or self.slug == None:
    #         uuid_key = shortuuid.uuid()
    #         uniqueid = uuid_key[:2]
    #         self.slug = slugify(self.full_name) + '-' + str(uniqueid.lower())
    #     super(Profile, self).save(*args, **kwargs)
     
    class Meta:
        ordering = ["-date"]

    def __str__(self):
        if self.full_name:
            return str(self.full_name)
        else:
            return str(self.user.username)   
        
    def thumbnail(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 30px;" />' % (self.image))

    
def create_user_profile(sender, instance, created, **Kwargs):
    if created:
        Profile.objects.create(user=instance)
        
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
 
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)



