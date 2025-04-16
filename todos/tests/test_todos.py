from playwright.sync_api import Page, expect
import pytest
from todos.models import TodoItem


def test_display_empty_list_on_first_load(live_index_url, page: Page):
    page.goto(live_index_url)
    expect(page.locator("#todo_items_empty")).not_to_be_empty()


def test_create_todo_item_shows_new_item(page_create_todo):
    title = "My Custom Todo"
    page = page_create_todo(title=title)
    page.wait_for_selector(f"text={title}")


def test_no_empty_text_when_todo_list_not_empty(page_create_todo):
    page = page_create_todo()
    expect(page.locator("#todo_items_empty")).to_be_empty()


def test_form_clears_after_submission(page_create_todo):
    page = page_create_todo()
    expect(page.get_by_role("textbox", name="Title*")).to_be_empty()
    expect(page.get_by_role("textbox", name="Description*")).to_be_empty()


def test_display_one_item_on_first_load(live_index_url, create_todo, page: Page):
    todo = create_todo()
    page.goto(live_index_url)
    page.wait_for_selector(f"text={todo.title}")
    expect(page.locator("#todo_items_empty")).to_be_empty()


def test_checkbox(create_todo, live_index_url, page: Page):
    items = [create_todo(title=f"Test item {i}") for i in range(3)]
    page.goto(live_index_url)

    middle_item = items[1]
    middle_id = f"toggle_item_{middle_item.id}"
    page.get_by_test_id(middle_id).check()
    expect(page.get_by_test_id(middle_id)).to_be_checked()

    middle_item.refresh_from_db()
    assert middle_item.completed is True

    items[0].refresh_from_db()
    assert items[0].completed is False

    items[2].refresh_from_db()
    assert items[2].completed is False


def test_checkbox_loads_correctly(create_todo, live_index_url, page: Page):
    item = create_todo(title="Test item", completed=True)
    page.goto(live_index_url)
    checkbox_id = f"toggle_item_{item.id}"
    expect(page.get_by_test_id(checkbox_id)).to_be_checked()


def test_completed_item_has_strikethrough_on_load(create_todo, live_index_url, page: Page):
    item = create_todo(title="Test item", completed=True)
    page.goto(live_index_url)
    checkbox_id = f"toggle_item_{item.id}"
    expect(page.get_by_test_id(checkbox_id)).to_be_checked()
    expect(page.locator(f"#checkbox-label-{item.id}")).to_have_class("font-semibold text-gray-900 line-through")


def test_item_has_strikethrough_added_when_completed(create_todo, live_index_url, page: Page):
    item = create_todo(title="Test item")
    page.goto(live_index_url)
    checkbox_id = f"toggle_item_{item.id}"
    expect(page.get_by_test_id(checkbox_id)).not_to_be_checked()
    expect(page.locator(f"#checkbox-label-{item.id}")).to_have_class("font-semibold text-gray-900")
    page.get_by_test_id(checkbox_id).click()
    expect(page.get_by_test_id(checkbox_id)).to_be_checked()
    expect(page.locator(f"#checkbox-label-{item.id}")).to_have_class("font-semibold text-gray-900 line-through")


def test_delete_item(create_todo, live_index_url, page: Page):
    item = create_todo(title="Test item", completed=True)
    page.goto(live_index_url)

    delete_id = f"delete_item_{item.id}"
    page.get_by_test_id(delete_id).click()

    expect(page.locator("#todo_items_empty")).not_to_contain_text("Test item")

    with pytest.raises(TodoItem.DoesNotExist):
        TodoItem.objects.get(id=item.id)


def test_delete_last_item_shows_nothing_to_see(create_todo, live_index_url, page: Page):
    item = create_todo(title="Test item", completed=True)
    page.goto(live_index_url)

    delete_id = f"delete_item_{item.id}"
    page.get_by_test_id(delete_id).click()

    page.wait_for_selector("text=Nothing to see")
