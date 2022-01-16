from django.urls import path
from .views import *

urlpatterns = [
    path('owner/create', OwnerCreate.as_view()),
    path('owner/list', OwnerList.as_view()),
    path('signup', OwnerCreateView.as_view()),
    path('login', OwnerLoginView.as_view()),
    path('perish/create', PerishableCreate.as_view()),
    path('perish/list', PerishableList.as_view()),
    path('perish_create', PerishableCreateView.as_view()),
    path('perish_update', PerishableUpdateView.as_view()),
    path('perish_delete', PerishableDeleteView.as_view()),
    path('get_user_perish', GetUsersPerishableByUsername.as_view()),
    path('get_code_perish', GetUsersPerishableByCode.as_view()),
    path('utilis/retrieve_username', retrieve_username.as_view()),
    path('perish_create_test', PerishableCreateTestView.as_view()),
    path('recommend_recipe', GetRecipeRecommendation.as_view()),
    path('utilis/sessions', logged_in_sessions.as_view()),
    path('logout', remove_session.as_view()),

    # path('owner/destroy', OwnerDestroy.as_view()),
]
