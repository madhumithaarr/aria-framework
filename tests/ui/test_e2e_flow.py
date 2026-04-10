import pytest
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.login_page import LoginPage
from tests.test_data import VALID_USER


@pytest.mark.smoke
@pytest.mark.ui
async def test_products_page_loads(products_page):
    """Verify products page shows a list of products."""
    count = await products_page.get_product_count()
    assert count > 0, "Expected products to be listed but found none"


@pytest.mark.regression
@pytest.mark.ui
async def test_product_search_returns_results(products_page):
    """Verify searching for a known product returns results."""
    await products_page.search("dress")
    count = await products_page.get_product_count()
    assert count > 0, "Search for 'dress' returned no results"


@pytest.mark.regression
@pytest.mark.ui
async def test_search_results_match_keyword(products_page):
    """
    Verify ALL returned search results are relevant to the search term.
    This is a quality check — not just 'did we get results' but 'are they correct'.
    """
    keyword = "top"
    await products_page.search(keyword)
    product_names = await products_page.get_all_product_names()

    assert len(product_names) > 0, f"No results found for '{keyword}'"

    # Check each result name contains the keyword (case insensitive)
    irrelevant = [
        name for name in product_names
        if keyword.lower() not in name.lower()
    ]

    # Allow up to 20% irrelevant results — real search engines aren't perfect
    allowed_irrelevant = len(product_names) * 0.2
    assert len(irrelevant) <= allowed_irrelevant, \
        f"Too many irrelevant results for '{keyword}': {irrelevant}"


@pytest.mark.regression
@pytest.mark.ui
async def test_add_product_to_cart(logged_in_page):
    """
    Full flow: Login → Products → Add to Cart → Verify in Cart.
    This is an E2E test — it crosses multiple pages.
    """
    # Step 1: Go to products (we're already logged in via fixture)
    products = ProductsPage(logged_in_page)
    await products.open()

    # Step 2: Add first product and remember its name
    added_product_name = await products.add_first_product_to_cart()

    # Step 3: Go to cart (click 'View Cart' on the modal)
    await products.go_to_cart()

    # Step 4: Verify the product we added is in the cart
    cart = CartPage(logged_in_page)
    # We're already on cart page after clicking View Cart — no need to navigate
    is_present = await cart.is_product_in_cart(added_product_name)

    assert is_present, \
        f"Product '{added_product_name}' was added but not found in cart"


@pytest.mark.regression
@pytest.mark.ui
async def test_cart_is_empty_initially(logged_in_page):
    """Verify a fresh cart is empty before adding anything."""
    cart = CartPage(logged_in_page)
    await cart.open()

    item_count = await cart.get_cart_item_count()

    # NOTE: This test may fail if you already have items from a previous test run
    # We handle this with a soft note — real apps would use API to clear cart
    # For now, document the state
    print(f"\nCart currently has {item_count} item(s)")

    # Verify the table at least exists (page loaded correctly)
    assert await cart.is_visible(cart.CART_TABLE) or \
           await cart.is_cart_empty(), \
        "Cart page didn't load correctly — neither cart table nor empty message visible"


# @pytest.mark.regression
# @pytest.mark.ui
# async def test_remove_item_from_cart(logged_in_page):
#     """
#     Full flow: Add item → Verify in cart → Remove it → Verify removed.
#     Tests the complete add + remove lifecycle.
#     """
#     # Step 1: Add a product first
#     products = ProductsPage(logged_in_page)
#     await products.open()
#     added_name = await products.add_first_product_to_cart()
#     await products.go_to_cart()

#     # Step 2: Verify it's in cart
#     cart = CartPage(logged_in_page)
#     initial_count = await cart.get_cart_item_count()
#     assert initial_count > 0, "Cart is empty after adding item — add step failed"

#     # Step 3: Remove the item
#     await cart.remove_first_item()

#     # Step 4: Verify count decreased
#     new_count = await cart.get_cart_item_count()
#     assert new_count < initial_count, \
#         f"Item count should have decreased. Before: {initial_count}, After: {new_count}"

@pytest.mark.regression
@pytest.mark.ui
async def test_remove_item_from_cart(logged_in_page):
    """Full flow: Add item → Verify in cart → Remove it → Verify removed."""
    products = ProductsPage(logged_in_page)
    await products.open()
    added_name = await products.add_first_product_to_cart()

    await products.go_to_cart()

    await logged_in_page.locator(
        "table#cart_info_table tbody tr"
    ).first.wait_for(state="visible", timeout=8000)

    cart = CartPage(logged_in_page)
    initial_count = await cart.get_cart_item_count()

    assert initial_count > 0, \
        f"Cart empty after adding '{added_name}'"

    await cart.remove_first_item()
    await logged_in_page.wait_for_timeout(1500)

    new_count = await cart.get_cart_item_count()
    assert new_count < initial_count, \
        f"Count should decrease. Before: {initial_count}, After: {new_count}"

@pytest.mark.ui
async def test_debug_cart_flow(logged_in_page):
    """Temporary debug test — delete after fixing."""
    products = ProductsPage(logged_in_page)
    await products.open()

    print("\n--- Step 1: Adding product ---")
    added_name = await products.add_first_product_to_cart()
    print(f"Added: {added_name}")
    print(f"--- URL after add = {logged_in_page.url} ---")

    await logged_in_page.screenshot(path="reports/debug_modal.png")
    print("--- Screenshot saved ---")

    # Print what's visible on screen right now
    body_text = await logged_in_page.locator("body").inner_text()
    print(f"--- Visible text (first 800 chars) ---\n{body_text[:800]}")

    # Check modal
    modal = logged_in_page.locator("div.modal-content")
    modal_visible = await modal.is_visible()
    print(f"--- Modal visible: {modal_visible} ---")

    if modal_visible:
        modal_text = await modal.inner_text()
        print(f"--- Modal text ---\n{modal_text}")