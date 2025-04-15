from playwright.sync_api import Page, expect


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
