from django.contrib import admin
from django.urls import path, include
from calculators.views import sitemap_xml, robots_txt

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # SEO files at root level - MUST be before the include
    path('sitemap.xml', sitemap_xml, name='sitemap_xml'),
    path('robots.txt', robots_txt, name='robots_txt'),
    
    # Include all other calculator URLs
    path('', include('calculators.urls')),
]