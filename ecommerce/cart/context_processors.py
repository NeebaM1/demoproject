from cart.models import Cart


def cart_count(requset):
    u=requset.user
    count=0
    if u.is_authenticated:
        try:
            item=Cart.objects.filter(user=u)
            count=item.count()
        except:
            pass
    return {'count':count}
