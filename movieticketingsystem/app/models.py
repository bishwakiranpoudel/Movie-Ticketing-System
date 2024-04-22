from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Theatre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

class Admin(models.Model):
    adminid = models.AutoField(primary_key=True)
    password = models.CharField(max_length=100)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)

class Customer(models.Model):
    username= models.CharField(max_length=100)
    cid = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    actors = models.TextField()
    director = models.CharField(max_length=100)
    poster = models.ImageField(upload_to='movie_posters/')
    description = models.TextField()

    def __str__(self):
        return self.title

class Show(models.Model):
    id = models.AutoField(primary_key=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    language = models.CharField(max_length=50)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)  # Add this line

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('not_booked', 'Not Booked'),
    ]
    id = models.AutoField(primary_key=True)
    hall_no = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seat_no = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_booked')
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)

@receiver(post_save, sender=Show)
def create_default_tickets(sender, instance, created, **kwargs):
    if created:
        for i in range(1, 41):  # Create 40 tickets for each show
            Ticket.objects.create(
                hall_no=instance.theatre.name,
                price=str(100),
                seat_no=str(i),
                status='not_booked',
                show=instance
            )