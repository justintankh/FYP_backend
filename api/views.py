from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework import generics, status
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.sessions.models import Session

import json
# Google image search
from .utilies import gis_url, product_information_via_barcode, RecSys
import datetime

# Create your views here.


def get_all_logged_in_users():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    username_list = []
    session_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        username_list.append(data.get('username', None))
        session_list.append(session.session_key)

    # Delete expired sessions
    Session.objects.exclude(session_key__in=session_list).delete()
    users_in_session = Session.objects.all()
    users = []

    # API of all logged in users with session details
    for user, sessionValue in zip(users_in_session, users_in_session.values()):
        data = user.get_decoded()
        users.append(data)
        data.update(sessionValue)

    # users = Session.objects.all().values()

    # users = Session.objects.filter(expire_date__gte=timezone.now()).values()

    return users


class logged_in_sessions(APIView):
    def get(self, request, format=None):
        Owners = get_all_logged_in_users()
        return Response(Owners, status=status.HTTP_200_OK)


def remove_username_session(name):
    print(name)
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    sessionDeleted = False

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        if data.get('username', None) == name:
            sessionDeleted = True
            session.delete()
            print('entered')

    return sessionDeleted


class remove_session(APIView):
    lookup_url_kwarg = 'username'

    def get(self, request, format=None):
        name = request.GET.get(self.lookup_url_kwarg)
        if (name != None and remove_username_session(name)):
            data = {'Successful': '{} has been logged out.'.format(name)}
            return Response(data, status=status.HTTP_200_OK)
        return Response({'Failed': 'name "{}" is not logged in.'.format(name)}, status.HTTP_404_NOT_FOUND)


class OwnerCreate(generics.CreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = CreateOwnerSerializer


class OwnerList(generics.ListAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class OwnerCreateView(APIView):
    serializer_class = CreateOwnerSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if not self.request.session.exists(self.request.session.session_key):
                self.request.session.create()

            username = serializer.data.get('username')
            password = serializer.data.get('password')
            queryset = Owner.objects.filter(username=username)

            if len(username) < 5:
                return Response({'Bad request': 'Minimum 5 characters for Username.'}, status=status.HTTP_400_BAD_REQUEST)

            if queryset.exists():
                owner = queryset[0]
                self.request.session['username'] = owner.username
                self.request.session['code'] = owner.code
                return Response({'Bad request': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                owner = Owner(username=username, password=password)
                owner.save()
                self.request.session['username'] = owner.username
                owner = Owner.objects.filter(username=username)[0]
                self.request.session['code'] = owner.code
                return Response(OwnerSerializer(owner).data, status=status.HTTP_201_CREATED)
        return Response({'Bad request': 'Invalid entry'}, status=status.HTTP_400_BAD_REQUEST)


class OwnerLoginView(APIView):
    def post(self, request, format=None):
        data = json.loads(self.request.body)
        if data:
            username = data['username']
            password = data['password']
            queryset = Owner.objects.filter(username=username)
            # if not self.request.session.exists(self.request.session.session_key):
            self.request.session.delete()
            self.request.session.create()
            if queryset.exists():
                owner = queryset[0]
                if password != owner.password:
                    return Response({'Bad request': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
                self.request.session['username'] = owner.username
                self.request.session['code'] = owner.code
                return Response(OwnerSerializer(owner).data, status=status.HTTP_200_OK)
            else:
                return Response({'Bad request': 'Username not found'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Bad request': 'Invalid username'}, status=status.HTTP_400_BAD_REQUEST)


class PerishableCreate(generics.CreateAPIView):
    queryset = Perishable.objects.all()
    serializer_class = CreatePerishableSerializer


class PerishableList(generics.ListAPIView):
    queryset = Perishable.objects.all()
    serializer_class = PerishableSerializer


class PerishableCreateView(APIView):
    serializer_class = CreatePerishableSerializer

    def post(self, request, format=None):
        # if not self.request.session.exists(self.request.session.session_key):
        # return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Obtain product information
            b_code = 'EMPTY' if serializer.data.get(
                'b_code') is None else serializer.data.get('b_code')
            title, categories, categories_score = product_information_via_barcode(
                b_code, serializer.data.get('title'))
            if (title == False):
                title = serializer.data.get('title')
                categories = serializer.data.get('title')
                categories_score = serializer.data.get('title')
            img_url = gis_url(title)
            username = serializer.data.get('username')
            exp = serializer.data.get('exp')
            qty = 1 if serializer.data.get(
                'qty') is None else serializer.data.get('b_code')
            perishable = Perishable(
                username=username, title=title, img_url=img_url, exp=exp, qty=qty,
                b_code=b_code, categories=categories, categories_score=categories_score)
            perishable.save()
            return Response(PerishableSerializer(perishable).data, status=status.HTTP_201_CREATED)
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class PerishableCreateTestView(APIView):
    serializer_class = CreatePerishableTestSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            b_code = serializer.data.get('b_code')
            title, categories, categories_score = product_information_via_barcode(
                b_code)
            if (title == False):
                title = serializer.data.get('title')
            title = serializer.data.get('title')
            username = 'justintankh'
            img_url = gis_url(title)
            exp = '2021-12-26'
            qty = '1'
            perishable = Perishable(
                username=username, title=title, img_url=img_url, exp=exp, qty=qty,
                b_code=b_code, categories=categories, categories_score=categories_score)
            perishable.save()
            return Response(PerishableSerializer(perishable).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class GetUsersPerishableByUsername(APIView):
    lookup_url_kwarg = 'username'

    def get(self, request, format=None):
        # fetch("/api/get_user_perish" + "?username=" + this.username)
        # username = self.request.session['username']
        username = request.GET.get(self.lookup_url_kwarg)
        if username != None:
            perishables = Perishable.objects.filter(username=username)
            if len(perishables) > 0:
                data = perishables.values("username", "p_code",
                                          "title", "img_url", "qty", "rtr_date", "exp",)
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Perishables not found': 'Invalid username.'}, status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'Username parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)


def user_logged_in(name):
    print(name)
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    loggedIn = False

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        if data.get('username', None) == name:
            loggedIn = True
            print('entered')

    return loggedIn


class retrieve_username(APIView):
    def get(self, request, format=None):
        if 'username' not in self.request.session:
            return Response({'error': 'user session expired. Please login.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if user_logged_in(self.request.session['username']):
                return Response({'username': self.request.session['username']}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'user session expired. Please login.'}, status=status.HTTP_400_BAD_REQUEST)


def username_by_code(code):
    queryset = Owner.objects.filter(code=code)
    if queryset.exists():
        return queryset[0].username
    else:
        return False


class GetUsersPerishableByCode(APIView):
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):
        # fetch("/api/get_user_perish" + "?username=" + this.username)
        # username = self.request.session['username']
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            username = username_by_code(code)
            if username == False:
                return Response({'Username not found': 'Invalid code.'}, status.HTTP_404_NOT_FOUND)
            perishables = Perishable.objects.filter(username=username)
            if len(perishables) > 0:
                data = perishables.values("username", "p_code",
                                          "title", "img_url", "qty", "rtr_date", "exp",)
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Perishables not found': 'Empty database.'}, status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'Code parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)


class PerishableDeleteView(APIView):
    serializer_class = DeletePerishableSerializer

    def post(self, request, format=None):
        if request.data['p_code']:
            p_code = request.data['p_code']
            Perishables = Perishable.objects.filter(p_code=p_code)
            if len(Perishables) > 0:
                perishable = Perishables[0]
                perishable.delete()
                return Response({'Message': 'Successfully deleted'}, status=status.HTTP_200_OK)
        return Response({'Message': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class PerishableDeleteManyView(APIView):
    def post(self, request, format=None):
        data = json.loads(self.request.body)
        if data['p_code_array']:
            p_code_array = data['p_code_array']
            for p_code in p_code_array:
                Perishables = Perishable.objects.filter(p_code=p_code)
                if len(Perishables) > 0:
                    perishable = Perishables[0]
                    perishable.delete()
            return Response({'Message': 'Successfully deleted'}, status=status.HTTP_200_OK)
        return Response({'Message': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class PerishableUpdateView(APIView):
    serializer_class = UpdatePerishableSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            p_code = request.data['p_code']
            qty = request.data['qty']
            exp = request.data['exp']
            Perishables = Perishable.objects.filter(p_code=p_code)
            if len(Perishables) > 0:
                perishable = Perishables[0]
                perishable.qty = qty
                perishable.exp = exp
                perishable.save()
                return Response({'Message': 'Successfully updated'}, status=status.HTTP_200_OK)
        return Response({'Message': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class GetRecipeRecommendation(APIView):
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):
        # fetch("/api/recommend_recipe" + "?code=" + p_code+p_code2+p_code3)
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            perishables = []
            categories = []
            priority = []
            p_code_list = code.split(' ')  # + in kwargs is seen as whitespace
            print('code:', code)
            print('p_code_list:', p_code_list)
            for p_code in p_code_list:
                perishable = Perishable.objects.filter(p_code=p_code)
                if len(perishable) > 0:
                    perishable = perishable[0]
                    perishables.append(
                        {
                            'username': perishable.username,
                            'p_code': perishable.p_code,
                            'title': perishable.title,
                            'img_url': perishable.img_url,
                            'qty': perishable.qty,
                            'rtr_date': perishable.rtr_date,
                            'exp': perishable.exp,
                            'b_code': perishable.b_code,
                            'categories': perishable.categories,
                            'categories_score': perishable.categories_score
                        })
                    # if(perishable.categories == ''):
                    # TODO : Empty category items.
                    #  Currently handled by parsing item title as basis for category in utilies.py

                    categories_list = perishable.categories.split(',')
                    categories_score_list = [
                        float(x) for x in perishable.categories_score.split(',')]

                    days_left = (perishable.exp - datetime.date.today()).days
                    # Use all categories it has to represent the ingredient
                    if(days_left < 4 or len(categories_list) < 4):
                        categories += categories_list
                        priority.append({perishable.p_code: categories_list})

                    else:  # Use top 3 category to represent the ingredient
                        capture = []
                        for i in range(3):
                            high_score = categories_score_list[0]
                            for score in categories_score_list:
                                if high_score < score:
                                    high_score = score
                            index = categories_score_list.index(high_score)
                            categories_score_list.pop(index)
                            categories.append(categories_list[index])
                            capture.append(categories_list.pop(index))
                        priority.append({perishable.p_code: capture})

                else:
                    # One of the P_CODE is not valid
                    return Response({'Perishables not found': 'Invalid code.'}, status.HTTP_404_NOT_FOUND)

            ingredients = ' '.join(list(set(categories)))
            recs_DF, transform_results = RecSys(ingredients, 10)
            data = recs_DF.to_dict(orient='records')
            queryDetails = {'Product_Qty': len(perishables),
                            'Product': perishables,
                            'Ingredient_Qty': len(categories),
                            'Ingredient': ','.join(categories),
                            'Priority': priority}
            data.append(queryDetails)

            return Response(data, status=status.HTTP_200_OK)
        return Response({'Bad Request': 'Code parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)
