from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View
from django.forms.models import model_to_dict
from .forms import ClassCreationForm, TypeToggle
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin



class ClassAdd(LoginRequiredMixin, View):
    def get(self, request):
        form = ClassCreationForm()
        return render(request, 'classes/class_add.html', context={'form':form})
    
    def post(self, request): # !!!
        inputdata = request.POST.copy()
        inputdata['creator'] = request.user.id
        form = ClassCreationForm(inputdata)
        if form.is_valid():
            class_ = form.save()
            class_.GenerateInviteLink()
            return redirect('home')
        else:
            return render(request, 'classes/class_add.html', context={'form':form})
        
class ViewClass(LoginRequiredMixin, View):
    def get(self, request, id):
        class_ = get_object_or_404(Class, id=id, creator__id=request.user.id)

        invite_link = request.build_absolute_uri(class_.InviteLink())
        form = TypeToggle(instance=class_)
        tests = class_.Tests()
        wr = class_.WaitingRoom()
        members = class_.Members()
        return render(request, 'classes/class.html', context={'class':class_, 'form':form, 'invite':invite_link, 'waitingRoom': {'objs': wr, 'count': len(wr)}, 'members':{'objs': members, 'count': len(members)}, 'tests':{'objs': tests, 'count': len(tests)}})
    def post(self, request, id):
        class_ = get_object_or_404(Class, id=id, creator__id=request.user.id)
        form = TypeToggle(request.POST, instance=class_)
        if form.is_valid():
            form.save()
        return redirect('class', id=id)

class ViewInvite(LoginRequiredMixin, View): # !!!
    def get(self, request, code): # !!!
        inv_link = get_object_or_404(InviteLink, code=code)
        class_ = inv_link.current_class
        info = self.Check(request, class_)
        if not info:
            return render(request, 'classes/invite.html', context={'class':class_})
        else:
            return render(request, 'classes/info.html', context={'info': info})
        
    def post(self, request, code):
        inv_link = get_object_or_404(InviteLink, code=code)
        class_ = inv_link.current_class
        info = self.Check(request, class_)
        if not info: 
            w = WaitingRoom(current_class=class_, user=request.user)
            w.save()
            info = 'Запрос на вступление отправлен'
            if class_.type.id == 1:
                class_.JoinUser(request.user.id)
                info = f'Вы присоединились к классу "{class_.name}"'
    
        return render(request, 'classes/info.html', context={'info': info})
        
    
    def Check(self, request, class_):
        info = None
        if request.user.id == class_.creator.id:
            info = 'The teacher cannot join his own class'
            info = 'Преподаватель не может вступить в собственный класс'
        elif class_.UserExistsInMembers(request.user.id):
            info = 'You are already in class'
            info = 'Вы уже в классе'
        elif class_.UserExistsInWaitingRoom(request.user.id):
            info = 'Class application already submitted'
            info = 'Запрос на вступление уже отправлен'
        elif class_.type.id == 3:
            info = 'Class closed'
            info = 'Класс закрыт'
        return info
        
class ViewJoin(LoginRequiredMixin, View):
    def get(self,request, class_id, user_id):
        class_ = get_object_or_404(Class, id=class_id, creator__id=request.user.id)
        class_.JoinUser(user_id)
        return redirect('class', id=class_.id)

class ViewReject(LoginRequiredMixin, View):
    def get(self,request, class_id, user_id):
        class_ = get_object_or_404(Class, id=class_id, creator__id=request.user.id)
        class_.RejectUser(user_id)
        return redirect('class', id=class_.id)
        
class DeleteCLass(LoginRequiredMixin, View): 
    def get(self, request, class_id):
        class_ = get_object_or_404(Class, id=class_id, creator__id=request.user.id)
        class_.delete()
        return redirect('home')

class ExceptMember(LoginRequiredMixin, View):
    def get(self, request, class_id, user_id):
        class_ = get_object_or_404(Class, id=class_id, creator__id=request.user.id)
        class_.ExeceptMember(user_id)
        return redirect('class', id=class_id)
    
class RefreshInvite(LoginRequiredMixin, View):
    def get(self, request, id):
        class_ = get_object_or_404(Class, id=id, creator__id=request.user.id)
        class_.ChangeInviteLink()
        return redirect('class', id=class_.id)

class ClassLeave(LoginRequiredMixin, View):
    def get(self, request, id):
        class_ = get_object_or_404(Class, id=id)
        class_.ExeceptMember(request.user.id)
        return redirect('home')
    