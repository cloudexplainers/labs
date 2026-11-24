from django.test import TestCase

from .models import Dish


class SignupTests(TestCase):
    def test_list_shows_dish(self):
        Dish.objects.create(name="Lasagna", person="Beth", kind="main")
        page = self.client.get("/signups/")
        self.assertContains(page, "Lasagna")

    def test_same_dish_twice_is_refused(self):
        Dish.objects.create(name="Lasagna", person="Beth", kind="main")
        page = self.client.post("/signups/new/", {"name": "Lasagna", "person": "Dave", "kind": "main"})
        self.assertContains(page, "already exists")
        self.assertEqual(Dish.objects.count(), 1)
