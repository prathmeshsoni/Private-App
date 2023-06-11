from django.db import models
import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings


class PrivateModel(models.Model):
    date_name = models.DateField()
    private_description = models.TextField(null = True)
    # private_img = models.FileField(null =True ,upload_to = 'Private/PrivateImage')

    def __str__(self):
        return "%s" % (self.date_name)


class Private_SubModel(models.Model):
    private_id = models.ForeignKey(PrivateModel, on_delete = models.CASCADE,null=True)
    private_img = models.FileField(null =True ,upload_to = 'Private/PrivateImage')
    type = models.CharField(max_length = 50)
    def delete(self, *args, **kwargs):
        # Delete the image file when the product is deleted
        os.remove(self.private_img.path)
        super(Private_SubModel, self).delete(*args, **kwargs)

    def __str__(self):
        return "%s" % (self.private_id)

@receiver(pre_delete, sender=PrivateModel)
def delete_subcategory_images(sender, instance, **kwargs):
    subcategories = Private_SubModel.objects.filter(private_id=instance)

    # Delete subcategory images
    for subcategory in subcategories:
        image_path = os.path.join(settings.MEDIA_ROOT, str(subcategory.private_img))
        if os.path.exists(image_path):
            os.remove(image_path)
