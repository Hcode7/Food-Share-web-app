from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class PremiumContentMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            if not request.user.subscription.is_active():
                if not 'premium' in request.path:
                    return redirect('subscription_page')
        else:
            if 'premium' in request.path:
                return redirect('login')
            
        return None