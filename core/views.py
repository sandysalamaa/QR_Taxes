from rest_framework import viewsets, permissions
from .models import Item, Receipt, Category
from .serializers import ItemSerializer, ReceiptSerializer, CategorySerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from django.db.models import Sum
from rest_framework.response import Response


class ReceiptViewSet(viewsets.ModelViewSet):
    serializer_class = ReceiptSerializer
    # authentication_classes = [FirebaseAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Receipt.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail = False , methods = ['get'])
    def category_total(self, request):
        """
        Returns aggregated spending by category for the authenticated user
        """
        totals = (
            Item.objects
            .filter(invoice__user=request.user)
            .values('category__name')
            .annotate(total=Sum('total_price'))
            .order_by('-total')
        )
        
        return Response({
            'results': list(totals),
            'grand_total': sum(item['total'] for item in totals if item['total'])
        })


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # authentication_classes = [FirebaseAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        return serializer.save()
    
class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Item.objects.filter(invoice__user = self.request.user)
    
    def perform_create(self, serializer):
        receipt = serializer.validated_data['invoice']
        if receipt.user != self.request.user:
            raise PermissionDenied("You don't own this receipt")
        serializer.save()