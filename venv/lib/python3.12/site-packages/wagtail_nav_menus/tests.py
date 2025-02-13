from django.test import TestCase
from rest_framework.test import APIRequestFactory
from wagtail.models import Site, Page
from .viewsets import NavMenuViewSet
from .models import NavMenu
import json
import wagtail


class NavMenuTestCase(TestCase):
    def setUp(self):
        self.json_menu = [
            {
                "type": "external_link",
                "value": {
                    "open_in_new_tab": True,
                    "link": "http://www.google.com",
                    "override_title": "TITLE",
                },
            },
            {
                "type": "page_link",
                "value": {"open_in_new_tab": False, "page": 2, "override_title": ""},
            },
            {"type": "image", "value": 1},
            {"type": "html", "value": "<div> html is here </div>"},
            {
                "type": "nav_category",
                "value": {
                    "title": "a nav cat",
                    "sub_nav": [
                        {
                            "type": "page_link",
                            "value": {
                                "open_in_new_tab": False,
                                "page": 1,
                                "override_title": "",
                            },
                        },
                    ],
                },
            },
        ]
        self.maxDiff = None

    def json_after_create_menu(self, json_for_create):
        menu = NavMenu.objects.create(name="top", menu=json.dumps([json_for_create]))
        output_json = menu.to_json()
        return json.loads(output_json)[0]

    def test_external_link(self):
        source = {
            "type": "external_link",
            "value": {
                "open_in_new_tab": True,
                "link": "http://www.google.com",
                "override_title": "TITLE",
            },
        }
        expected = source
        result = self.json_after_create_menu(source)
        self.assertDictEqual(result, expected)

    def test_image(self):
        source = {"type": "image", "value": 1}
        expected = {"type": "image", "value": None}
        result = self.json_after_create_menu(source)
        self.assertDictEqual(result, expected)

    def test_html(self):
        source = {"type": "html", "value": "<div> html is here </div>"}
        expected = {"type": "html", "value": "<div> html is here </div>"}
        result = self.json_after_create_menu(source)
        self.assertDictEqual(result, expected)

    def test_page_link(self):
        source = {
            "type": "page_link",
            "value": {"open_in_new_tab": False, "page": 2, "override_title": ""},
        }
        expected = {
            "type": "page_link",
            "value": {
                "page": {
                    "slug": "home",
                    "live": True,
                    "content_type": 1,
                    "pk": 2,
                    "first_published_at": None,
                    "search_description": "",
                    "numchild": 0,
                    "latest_revision_created_at": None,
                    "locked": False,
                    "expire_at": None,
                    "url": "/",
                    "show_in_menus": False,
                    "title": "Welcome to your new Wagtail site!",
                    "seo_title": "",
                    "url_path": "/home/",
                    "depth": 2,
                    "owner": None,
                    "path": "00010001",
                    "has_unpublished_changes": False,
                    "draft_title": "Welcome to your new Wagtail site!",
                    "expired": False,
                    "go_live_at": None,
                    "last_published_at": None,
                    "live_revision": None,
                },
                "open_in_new_tab": False,
                "override_title": "",
            },
        }
        result = self.json_after_create_menu(source)
        self.assertEqual(result["type"], expected["type"])
        self.assertEqual(
            result["value"]["open_in_new_tab"], expected["value"]["open_in_new_tab"]
        )
        self.assertEqual(
            result["value"]["override_title"], expected["value"]["override_title"]
        )
        self.assertEqual(
            result["value"]["page"]["slug"], expected["value"]["page"]["slug"]
        )

    def test_nav_category(self):
        source = {
            "type": "nav_category",
            "value": {
                "title": "a nav cat",
                "sub_nav": [
                    {
                        "type": "page_link",
                        "value": {
                            "open_in_new_tab": False,
                            "page": 1,
                            "override_title": "",
                        },
                    }
                ],
            },
        }
        expected = {
            "type": "nav_category",
            "value": {
                "title": "a nav cat",
                "sub_nav": [
                    {
                        "type": "page_link",
                        "value": {
                            "page": {
                                "slug": "root",
                                "live": True,
                                "content_type": 1,
                                "pk": 1,
                                "first_published_at": None,
                                "search_description": "",
                                "numchild": 1,
                                "latest_revision_created_at": None,
                                "locked": False,
                                "expire_at": None,
                                "show_in_menus": False,
                                "title": "Root",
                                "seo_title": "",
                                "url_path": "/",
                                "depth": 1,
                                "owner": None,
                                "path": "0001",
                                "has_unpublished_changes": False,
                                "draft_title": "Root",
                                "url": None,
                                "expired": False,
                                "go_live_at": None,
                                "last_published_at": None,
                                "live_revision": None,
                            },
                            "open_in_new_tab": False,
                            "override_title": "",
                        },
                    }
                ],
            },
        }
        # Page schema added a few fields in Wagtail 2.8
        if wagtail.VERSION[0] == 2 and wagtail.VERSION[1] >= 8:
            expected["value"]["sub_nav"][0]["value"]["page"]["locked_at"] = None
            expected["value"]["sub_nav"][0]["value"]["page"]["locked_by"] = None
        result = self.json_after_create_menu(source)
        self.assertEqual(result["type"], expected["type"])
        self.assertEqual(result["value"]["title"], expected["value"]["title"])
        self.assertEqual(
            result["value"]["sub_nav"][0]["type"],
            expected["value"]["sub_nav"][0]["type"],
        )
        self.assertEqual(
            result["value"]["sub_nav"][0]["value"]["open_in_new_tab"],
            expected["value"]["sub_nav"][0]["value"]["open_in_new_tab"],
        )
        self.assertEqual(
            result["value"]["sub_nav"][0]["value"]["page"]["slug"],
            expected["value"]["sub_nav"][0]["value"]["page"]["slug"],
        )

    def test_menu_json(self):
        """Test serializing and deserializing the menu json"""
        menu = NavMenu.objects.create(name="top", menu=json.dumps(self.json_menu))

        output_json = menu.to_json()
        output = json.loads(output_json)

        self.assertEqual(output[0]["type"], "external_link")
        self.assertEqual(output[0]["value"]["link"], "http://www.google.com")

    def test_render_menu(self):
        json_menu = json.dumps(self.json_menu)
        NavMenu.objects.create(name="top", menu=json_menu)
        NavMenu.objects.create(name="bottom", menu=json_menu)
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)


class NavMenuViewSetTestCase(TestCase):
    def test_nav_menu_viewset(self):
        request = APIRequestFactory().get("")
        nav_detail = NavMenuViewSet.as_view({"get": "retrieve"})
        nav = NavMenu.objects.create(name="top")
        response = nav_detail(request, pk=nav.pk)
        self.assertContains(response, nav.name)

    def test_nav_menu_viewset_site(self):
        """
        Nav API should support Wagtail Sites and return only sites as specific
        """
        page = Page.objects.all().last()
        default_site = Site.objects.all().first()
        other_site = Site.objects.create(
            hostname="example.com", port=80, root_page=page
        )
        rdata = {
            "SERVER_NAME": other_site.hostname,
        }
        rfactory = APIRequestFactory(**rdata)
        request = rfactory.get("")
        nav_detail = NavMenuViewSet.as_view({"get": "list"})
        nav_default_site = NavMenu.objects.create(name="default", site=default_site)
        nav_other_site = NavMenu.objects.create(name="other", site=other_site)
        response = nav_detail(request)
        self.assertContains(response, nav_other_site.name)
        self.assertNotContains(response, nav_default_site.name)

    def test_nav_menu_viewset_site_filter(self):
        """
        Nav API should allow site filter override
        """
        page = Page.objects.all().last()
        default_site = Site.objects.all().first()
        other_site = Site.objects.create(
            hostname="example.com", port=80, root_page=page
        )
        rdata = {
            "SERVER_NAME": other_site.hostname,
        }
        rfactory = APIRequestFactory(**rdata)
        request = rfactory.get("?site=2")
        nav_detail = NavMenuViewSet.as_view({"get": "list"})
        nav_default_site = NavMenu.objects.create(name="default", site=default_site)
        nav_other_site = NavMenu.objects.create(name="other", site=other_site)
        response = nav_detail(request)
        self.assertContains(response, nav_other_site.name)
        self.assertNotContains(response, nav_default_site.name)
