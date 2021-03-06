
from rest_framework.generics import (
	ListAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	DestroyAPIView,
	CreateAPIView,
)
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import *
from .permissions import *
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

class UserCreateAPIView(CreateAPIView):
	serializer_class = UserCreateSerializer

#------------------------------------------------------#Product

class ProductListView(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductListSerializer
	permission_classes = [AllowAny,]
	filter_backends = [SearchFilter, OrderingFilter,]
	search_fields = ['name', 'description',]



class ProductDetailView(RetrieveAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductDetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'product_id'
	permission_classes = [AllowAny,]

#------------------------------------------------------#Profile

class ProfileCreateAPIView(CreateAPIView):
	serializer_class = ProfileSerializer

class ProfileView(APIView):
	permission_classes = [IsAuthenticated, ]
	def get(self, request):
		profile = request.user.profile
		return Response(ProfileSerializer(profile).data)


class ProfileUpdateView(RetrieveUpdateAPIView):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'profile_id'
	permission_classes = [IsAuthenticated,IsUser ]


#------------------------------------------------------#Order


class OrderCreateView(APIView):
	permission_classes = [IsAuthenticated]
	def post(self, request):
		new_order=Order.objects.create(
			ordered_by =request.user,
			# ordered_on= datetime.now()
		)

		products=request.data["cart"]
		print(request.data)
		for product in products:
			the_product = Product.objects.get(id=product["id"])
			new_order_product=OrderProduct(product=the_product, quantity=product["quantity"])
			the_product.quantity-=int(new_order_product.quantity)
			print(the_product.quantity)
			the_product.save()
			new_order_product.order=new_order
			new_order_product.save()

		address=request.data["address"]
		the_address=Address.objects.get(id=int(address))
		total_price = request.data["totalPrice"]
		new_order.price = total_price
		new_order.address= the_address

		new_order.save()
		return Response(OrderSerializer(new_order).data)
		# serializer.save(user=self.request.user)

class OrderListView(ListAPIView):
	serializer_class = OrderListSerializer
	permission_classes = [IsAuthenticated,IsUser]
	def get_queryset(self):
		return Order.objects.filter(ordered_by=self.request.user)


class OrderDetailView(RetrieveAPIView):
	queryset = Order.objects.all()
	serializer_class = OrderDetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'order_id'
	permission_classes = [IsAuthenticated,IsUserOrder]

#------------------------------------------------------#Address


class AddressListView(ListAPIView):
	serializer_class = AddressSerializer
	permission_classes = [IsAuthenticated, IsUser]
	def get_queryset(self):
		return Address.objects.filter(user=self.request.user)

class AddressCreateView(CreateAPIView):
	serializer_class = AddressSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


class AddressUpdateView(RetrieveUpdateAPIView):
	queryset = Address.objects.all()
	serializer_class = AddressSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'address_id'
	permission_classes = [IsAuthenticated,IsUser ]

#------------------------------------------------------#

