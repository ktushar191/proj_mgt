from django.db import models

import uuid
from django.conf import settings

class SessionLog(models.Model):
    class Meta:
        db_table = 'auth_session_log'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_column='user_id',on_delete=models.CASCADE)
    logged_in_datetime = models.DateTimeField(auto_now_add=True)
    logged_out_datetime = models.DateTimeField(blank=True, null=True, default=None)
    source = models.CharField(max_length=30)
    auth_type = models.CharField(max_length=100,blank=True, null=True, default=None)
    fcm_id = models.CharField(max_length=1000, blank=True, null=True, default=None)

    def __str__(self):
        data = dict(id=self.id, user=self.user, client=self.client, logged_in_datetime=self.logged_in_datetime,
                    logged_out_datetime=self.logged_out_datetime, source=self.source ,  auth_type=self.auth_type,
                    fcm_id=self.fcm_id)
        return "{}".format(data)