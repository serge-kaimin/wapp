
from django.views.generic import TemplateView


# Serve react app from /app/public folder
class HomePageView(TemplateView):
    template_name = "index.html"