from django.urls import reverse
from playwright.sync_api import Page, expect


def test_display_empty_list_on_first_load(live_server, page: Page):
    url = reverse_url(live_server, "index")

    page.goto(url)
    page.wait_for_selector("text=Nothing to see")


def reverse_url(live_server, viewname, urlconf=None, args=None, kwargs=None, current_app=None):
    end = reverse(viewname, urlconf, args, kwargs, current_app)
    return f"{live_server.url}{end}"


def test_create_todo_item_shows_new_item(live_server, page: Page):
    url = reverse_url(live_server, "index")

    page.goto(url)
    page.get_by_role("textbox", name="Title*").click()
    page.get_by_role("textbox", name="Title*").fill("testing")
    page.get_by_role("textbox", name="Description*").click()
    page.get_by_role("textbox", name="Description*").fill("testing")
    page.get_by_role("button", name="Add").click()
    page.wait_for_selector("text=testing")


def test_no_empty_text_when_todo_list_not_empty(live_server, page: Page):
    url = reverse_url(live_server, "index")

    page.goto(url)
    page.get_by_role("textbox", name="Title*").click()
    page.get_by_role("textbox", name="Title*").fill("testing")
    page.get_by_role("textbot", name="Title*")
    page.get_by_role("textbox", name="Description*").click()
    page.get_by_role("textbox", name="Description*").fill("testing")
    page.get_by_role("button", name="Add").click()
    expect(page.get_by_text("Nothing to see here...")).not_to_be_visible()


def test_form_clears_after_submission(live_server, page: Page):
    url = reverse_url(live_server, "index")
    page.goto(url)
    page.get_by_role("textbox", name="Title*").click()
    page.get_by_role("textbox", name="Title*").fill("testing")
    page.get_by_role("textbox", name="Description*").click()
    page.get_by_role("textbox", name="Description*").fill("testing")
    page.get_by_role("button", name="Add").click()
    expect(page.get_by_role("textbox", name="Title*")).to_be_empty()
    expect(page.get_by_role("textbox", name="Description*")).to_be_empty()
