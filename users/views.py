from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.services import (
    create_stripe_price,
    create_stripe_product,
    create_stripe_session,
)


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment_user = serializer.save(user=self.request.user)

        product = create_stripe_product(payment_user.course)
        price = create_stripe_price(payment_user.price)
        session_id, payment_link = create_stripe_session(price)

        payment_user.product_id = product.id
        payment_user.session_id = session_id
        payment_user.link = payment_link
        payment_user.save()
