from django.urls import path
from kanbans import views

app_name = "kanbans"

urlpatterns =[
    path("columns", views.ColumnView.as_view()),
    path("columns/<int:col_id>/", views.ColumnDetailsView.as_view()),
    path("columns/order", views.ReorderColumnsView.as_view()),
]