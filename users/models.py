from django.db import models
from django.contrib.auth.models import User

# # class UserModel(models.Model):
# #     user = models.OneToOneField(User, on_delete=models.CASCADE)
# #     name = models.CharField(max_length=12) 
# #     email = models.EmailField(max_length=48)

# #     class Meta:
# #         unique_together = [['user', 'name']]
    
# #     def __str__(self) -> str:
# #         return f" {'user': self.name}"


# class ProfileUser(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     tickers = models.CharField(max_length=8, null=True)
#     key_words = models.CharField(max_length=18, null=True)

#     def __str__(self) -> str:
#         return f"{self.user}"
