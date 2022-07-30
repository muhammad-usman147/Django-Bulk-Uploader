from django.urls import path
from .views import get_churn_image, list_of_data_view, result_api_view, result_cga_api_view, result_churn_api_view

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'dataset', list_of_data_view, basename='dataset')


urlpatterns = [
    path('result', result_api_view, name='result'),
    path('result_cga', result_cga_api_view, name='result_cga'),
    path('result_churn', result_churn_api_view, name='result_churn'),
    path('churn_image', get_churn_image, name='churn_image')
]

urlpatterns += router.urls