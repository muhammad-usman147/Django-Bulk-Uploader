from django.shortcuts import render
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from rest_framework import views, permissions, authentication
from .serializers import SignupSerializer, LoginSerializer
import json
#-----------
from .models import Profile
USER = get_user_model()


@api_view(['POST'])
def signup_view(request):
    if request.method == 'POST':
        user_data = request.data.get('user')
        if user_data:
            username = USER.objects.filter(name=user_data.get('name'))
            email = USER.objects.filter(email=user_data.get('email'))

            if any([username, email]):
                return Response({
                    'msg': 'email and username already taken'
                })
            serializer = SignupSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'msg': 'user created'
                })
            return Response({
                'msg': serializer.errors
            })
        else:
            return Response({
                'msg': 'requested data is not valid'
            })


from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.utils.decorators import  method_decorator
from django.views import View

#rest api
@method_decorator(csrf_exempt,name = 'dispatch')
class CustomProfile(View):
    def post(self,request):
        if request.method == 'POST':
            user_data  = json.loads(request.body.decode("utf-8"))
            if True:
                print("="*10)
                print(user_data)
                #username = Profile.objects.all()

                if True:

                    output = []
                    
                    output.append(
                            {
                                "username":user_data
                            }
                        )
                    return JsonResponse({"output":output})
        else:
            return JsonResponse({"msg":"Error"})


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({'msg' : 'user login'})

class LogoutView(views.APIView):
    def post(self, request):
        logout(request)
        return Response({'msg' : 'user logout'})


'''
{
"username": "usama",
"email": "usamamashood@gmial.com",
"password": "12345566",
"company": "python",
"phone":"03116100813"
}

{
"user" : {
"username": "usama",
"email": "usamamashood@gmial.com",
"password": "12345566"
},
"company": "python",
"phone":"03116100813"
}
'''
