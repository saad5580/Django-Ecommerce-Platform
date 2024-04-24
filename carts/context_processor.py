from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    cart_count =  0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id = _cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user = request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart = cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0

    return dict(cart_count = cart_count)


# base_context_processors.py

# Context processor

# def session_expired(request):
#     session_is_expired = request.session.get("session_expired", False)  
#     return {"session_expired": session_is_expired}
