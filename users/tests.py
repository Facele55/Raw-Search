from django.test import TestCase


class DBTestCase(TestCase):
    databases = {'search_db'} # {'__all__'} shold work too

    def setUp(self):
        ContentSearchIndex.objects.using('search_db').create(url="https://www.starwars.com/", title="Star Wars", description="star Wars Site", site_lang="en", site_content="About Star Wars", keywords="star wars")
        ContentSearchIndex.objects.using('search_db').create(url="https://www.google.com/", title="Google", description="Google Site", site_lang="en", site_content="Google search engine", keywords="google search")

    def test_star_can_wars(self):
        """Star Wars correctly identified"""
        star_wars1 = ContentSearchIndex.objects.using('search_db').get(url="https://www.starwars.com/")
        self.assertEqual(star_wars1.url, "https://www.starwars.com/")
        self.assertEqual(star_wars1.title, "Star Wars")
        self.assertEqual(star_wars1.description, "star Wars Site")
        self.assertEqual(star_wars1.site_lang, "en")
        self.assertEqual(star_wars1.site_content, "About Star Wars")
        self.assertEqual(star_wars1.keywords, "star wars")

    def test_google(self):
        """Google correctly identified"""
        google = ContentSearchIndex.objects.using('search_db').get(url="https://www.google.com/")
        self.assertEqual(google.url, "https://www.google.com/")
        self.assertEqual(google.title, "Google")
        self.assertEqual(google.description, "Google Site")
        self.assertEqual(google.site_lang, "ee")
        self.assertEqual(google.site_content, "Google search engine")
        self.assertEqual(google.keywords, "google search")
