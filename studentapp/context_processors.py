from studentapp.models import Studentstbl
from wardenapp.models import Wardentbl
from adminapp.models import Admintbl,Hosteltbl

def user_context(request):
    user_info=None
    approval_status=None
    hostel_names=Hosteltbl.objects.all()

    if request.session.get('user_id'):
        user_info = Studentstbl.objects.get(id=request.session['user_id'])
        approval_status = user_info.sapproval
    elif request.session.get('admin_id'):
        user_info = Admintbl.objects.get(id=request.session['admin_id'])
    elif request.session.get('warden_id'):
        user_info = Wardentbl.objects.get(id=request.session['warden_id'])
        approval_status = user_info.wapproval

    return {
        'logged_in_user': user_info,
        'approval_status': approval_status,
        'hostel_names':hostel_names
    }


# Context Processors:
# Context processors are used in Django to add additional context data to all templates. -
# These data are automatically included without the need to pass them explicitly from each view.

# Benefits:
# Code Reusability: You don’t have to pass warden_obj manually in every view that needs it.
# Cleaner Views: Keeps your views cleaner by eliminating repetitive code.
# Consistent Context: Ensures that some essential data is consistently available across all templates without explicit handling.