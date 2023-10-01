from django.db import models
from tests.models import TestForClass
from django.utils.crypto import get_random_string
import string
from django.urls import reverse

# Create your models here.

    
class ClassType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self) -> str:
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey("users.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.ForeignKey(ClassType, on_delete=models.DO_NOTHING, default=1)
    
    def __str__(self) -> str:
        return self.name
    
    
    def Generate_or_get_InviteLink(self):
        ex_code = self.CodeExists()
        if not ex_code:
            ex_code = self.GenerateInviteLink()
        return ex_code
        
    def ChangeInviteLink(self):
        invite_link = self.CodeExists()
        while True:
            try:
                invite_link.code = self.GenerateCode()
                return invite_link.save()
            except:pass
        
    def GenerateInviteLink(self):
        while True:
            try:
                code = self.GenerateCode()
                il = InviteLink(current_class=self, code=code)
                return il.save()
            except:pass
            
    def GenerateCode(self):
        return get_random_string(8, allowed_chars=string.ascii_uppercase + string.digits)
    
    def CodeExists(self):
        return self.ExistsIn(InviteLink, current_class__id=self.id)

    def InviteLink(self):
        code = self.CodeExists()
        return code.url()
    
    def Tests(self):
        return TestForClass.objects.filter(current_class=self.id)
    
    def Members(self):
        return Member.objects.filter(current_class=self.id)
    
    def WaitingRoom(self):
        return WaitingRoom.objects.filter(current_class=self.id)
    
    def ExistsIn(self, model, **kw):
        try:
            return model.objects.get(**kw)
        except:
            return None
    
    def UserExistsIn(self, model, user_id):
        
        # try:
        #     return model.objects.get(user__id=user_id, current_class__id=self.id)
        # except:
        #     return None
        return self.ExistsIn(model=model,user__id=user_id, current_class__id=self.id)
    
    def UserExistsInMembers(self, user_id):
        return self.UserExistsIn(Member, user_id)
        
    def UserExistsInWaitingRoom(self, user_id):
        return self.UserExistsIn(WaitingRoom, user_id)

    def JoinUser(self, user_id):
        wr_user = self.UserExistsInWaitingRoom(user_id)
        if wr_user:
            rejected_user = self.RejectUser(user_id)
            if rejected_user:
                m = Member(current_class=self, user=wr_user.user)
                return m.save()
        return False
        
    def RejectUser(self, user_id):
        wr_user = self.UserExistsInWaitingRoom(user_id)
        if wr_user:
            return wr_user.delete()
        else:
            return False
    
    def ExeceptMember(self, user_id):
        mb = self.UserExistsInMembers(user_id)
        mb.delete()

class Member(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    current_class = models.ForeignKey(Class, on_delete=models.CASCADE)

class WaitingRoom(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    current_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    

class InviteLink(models.Model):
    current_class = models.OneToOneField(Class, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def url(self):
        return reverse('invite', kwargs={'code': self.code})
