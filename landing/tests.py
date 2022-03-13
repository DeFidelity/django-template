from django.test import SimpleTestCase, Client
from django.urls import reverse, resolve
from landing.views import IndexView

class TestUrls(SimpleTestCase):
    
    def setUp(self):
        self.index_url = reverse('index')
        self.cient = Client()
    
    def test_index_url(self):
        response = resolve(self.index_url)
        
        self.assertEquals(response.func.view_class,IndexView)
        self.assertTemplateUsed('landing/index.html')
    
    def test_index_view(self):
        
        response = self.client.get(self.index_url)
        
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed('landing/index.html')
        
        
        