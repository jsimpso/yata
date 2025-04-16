import pytest
from django.urls import reverse
from todos.models import TodoItem
from playwright.sync_api import Page


@pytest.fixture(scope="function")
def live_index_url(live_server):
    index_url = reverse("index")
    return f"{live_server.url}{index_url}"


@pytest.fixture(scope="function")
def create_todo():
    def _create_todo(title: str = "Test Title", description: str = "Created via Model", completed: bool = False):
        return TodoItem.objects.create(title=title, description=description, completed=completed)

    return _create_todo


@pytest.fixture(scope="function")
def page_create_todo(live_index_url, page: Page):
    def _create_todo(title: str = "Test Title", description: str = "Created via UI"):
        page.goto(live_index_url)
        page.get_by_role("textbox", name="Title*").click()
        page.get_by_role("textbox", name="Title*").fill(title)
        page.get_by_role("textbox", name="Description*").click()
        page.get_by_role("textbox", name="Description*").fill(description)
        page.get_by_role("button", name="Add").click()
        return page

    return _create_todo
