from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

class Categories(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name   

class Listing(models.Model):
    Owner = models.ForeignKey(User, on_delete=models.CASCADE)
    Image = models.ImageField(upload_to="listing_images/", blank=True, null=True)  # ✅ real file upload
    Name = models.CharField(max_length=64)
    Desc = models.TextField()  
    When = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Name
    
    def serialize(self):
        return {
            "id": self.id,
            "owner": self.Owner.username,   
            "image": self.Image.url if self.Image else None,
            "name": self.Name,
            "desc": self.Desc,
            "when": self.When.strftime("%Y-%m-%d %H:%M:%S")
        }  

class Messages(models.Model):
    Sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    Receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    Message = models.CharField(max_length=64)
    Attachment = models.FileField(upload_to="attachments/", blank=True, null=True)  
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)
    When = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.Sender} → {self.Receiver}: {self.Message[:20]}"
    
    def serialize(self):
        return {
            "id": self.id,
            "sender": self.Sender.username,     
            "receiver": self.Receiver.username, 
            "message": self.Message,
            "attachment": self.Attachment.url if self.Attachment else None,
            "item": self.item.Name if self.item else None,
            "when": self.When.strftime("%Y-%m-%d %H:%M:%S")
        }
