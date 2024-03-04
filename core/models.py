from django.contrib.auth.models import User

from django.db import models
from geopy.geocoders import Nominatim

class Location(models.Model):
    DISTRICT_CHOICES = [
        ('Balaka', 'Balaka'),
        ('Blantyre', 'Blantyre'),
        ('Chikwawa', 'Chikwawa'),
        ('Chiradzulu', 'Chiradzulu'),
        ('Chitipa', 'Chitipa'),
        ('Dedza', 'Dedza'),
        ('Dowa', 'Dowa'),
        ('Karonga', 'Karonga'),
        ('Kasungu', 'Kasungu'),
        ('Likoma', 'Likoma'),
        ('Lilongwe', 'Lilongwe'),
        ('Machinga', 'Machinga'),
        ('Mangochi', 'Mangochi'),
        ('Mchinji', 'Mchinji'),
        ('Mulanje', 'Mulanje'),
        ('Mwanza', 'Mwanza'),
        ('Mzimba', 'Mzimba'),
        ('Nkhata Bay', 'Nkhata Bay'),
        ('Nkhotakota', 'Nkhotakota'),
        ('Nsanje', 'Nsanje'),
        ('Ntcheu', 'Ntcheu'),
        ('Ntchisi', 'Ntchisi'),
        ('Phalombe', 'Phalombe'),
        ('Rumphi', 'Rumphi'),
        ('Salima', 'Salima'),
        ('Thyolo', 'Thyolo'),
        ('Zomba', 'Zomba'),
    ]

    name = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.latitude or not self.longitude:
           
            geolocator = Nominatim(user_agent="core")
            location = geolocator.geocode(self.name + ", Malawi")

            if location:
                self.latitude = location.latitude
                self.longitude = location.longitude

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


def get_precautionary_measures(destruction_percentage):
    if destruction_percentage < 40:
        return "Low risk: Take basic precautions."
    elif 40 <= destruction_percentage < 70:
        return "Moderate risk: Evacuate if necessary, follow local authorities' instructions."
    else:
        return "High risk: Immediate action required. Evacuate and follow emergency procedures."


class AffectedArea(models.Model):
    name = models.CharField(max_length=100)
    district = models.CharField(max_length=100, choices=Location.DISTRICT_CHOICES)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    destruction_percentage = models.FloatField()
    precautionary_measures = models.TextField()

    def save(self, *args, **kwargs):
       
        location_name = f"{self.name}, {self.district}, Malawi"
        geolocator = Nominatim(user_agent="core")
        location = geolocator.geocode(location_name)

        if location:
            self.latitude = location.latitude
            self.longitude = location.longitude

      
        self.precautionary_measures = get_precautionary_measures(self.destruction_percentage)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.district}"

class Disaster(models.Model):
    DISASTER_CHOICES = [
        ('Floods', 'Floods'),
        ('Drought', 'Drought'),
        ('Fire', 'Fire'),
        ('Cyclone', 'Cyclone'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100, choices=DISASTER_CHOICES)
    banner_image = models.ImageField(upload_to='banner_image', null=True, blank=True)
    image = models.ImageField(upload_to='data_images/', null=True, blank=True)
    image_one = models.ImageField(upload_to='data_images/', null=True, blank=True)
    image_two = models.ImageField(upload_to='data_images/', null=True, blank=True)
    image_three = models.ImageField(upload_to='data_images/', null=True, blank=True)

    displaced = models.IntegerField()
    dead = models.IntegerField()
    date = models.DateField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    description = models.TextField()
    affected_areas = models.ManyToManyField(AffectedArea)  
    def location_info(self):
        return {
            'name': self.location.name,
            'latitude': self.location.latitude,
            'longitude': self.location.longitude,
        }


    def calculate_total_relief_aid_percentage(self):
     
        if self.affected_areas.exists():
           
            total_destruction_percentage = sum(area.destruction_percentage for area in self.affected_areas.all())

           
            average_destruction_percentage = total_destruction_percentage / self.affected_areas.count()

            
            if average_destruction_percentage < 40:
                return 20 
            elif 40 <= average_destruction_percentage < 70:
                return 50  
            else:
                return 80 
        else:
            return 0 

    def __str__(self):
        return f"{self.name}, {self.location}"


class Prediction(models.Model):
    disaster = models.ForeignKey(Disaster, on_delete=models.CASCADE)
    predicted_date = models.DateField()
    confidence = models.FloatField()

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=500)
    lastname = models.CharField(max_length=500)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        if not self.pk:  # If the instance is being created, set the user
            self.user = self.user or getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
        super(Profile, self).save(*args, **kwargs)

    
class Updates(models.Model):
    messagez = models.CharField(max_length=500)
    def __str__(self):
        return self.messagez
    
class CommunityFeedback(models.Model):
    message = models.TextField()

    def __str__(self):
        return f"{self.name}"


# models.py


class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"

class Thread(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.title}"

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.thread}"