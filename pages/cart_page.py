import logging
from playwright.async_api import Page
from aria.base_page import BasePage

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    """
    Page Object for automationexercise.com/view_cart page.
    Handles cart verification, quantity checks, and item removal.
    """

    # --- Selectors ---
    # CART_TABLE = "table#cart_info_table"
    # CART_ITEMS = "tr.cart_product"              # Each row in cart = one product
    # CART_PRODUCT_NAMES = "td.cart_description h4 a"  # Product name in cart row
    # CART_QUANTITY = "td.cart_quantity button"   # Quantity shown in cart
    # CART_PRICE = "td.cart_price p"              # Price per item
    # CART_TOTAL = "td.cart_total p"              # Total price per row
    # REMOVE_BUTTON = "a.cart_quantity_delete"    # × button to remove item
    # EMPTY_CART_MSG = "b:has-text('Cart is empty!')"
    # PROCEED_TO_CHECKOUT = "a:has-text('Proceed To Checkout')"
    CART_TABLE = "table#cart_info_table"
    CART_ITEMS = "table#cart_info_table tbody tr"
    CART_PRODUCT_NAMES = "td.cart_description h4 a"
    CART_QUANTITY = "td.cart_quantity button"
    CART_PRICE = "td.cart_price p"
    CART_TOTAL = "td.cart_total p"
    REMOVE_BUTTON = "td.cart_delete a"
    EMPTY_CART_MSG = "span#empty_cart"
    PROCEED_TO_CHECKOUT = "a:has-text('Proceed To Checkout')"

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://automationexercise.com/view_cart"

    async def open(self) -> "CartPage":
        """Navigate directly to cart page."""
        await self.navigate(self.url)
        return self

    async def get_cart_item_count(self) -> int:
        """Return number of distinct products in the cart."""
        items = self.page.locator(self.CART_ITEMS)
        count = await items.count()
        logger.info(f"Cart contains {count} item(s)")
        return count

    async def get_all_cart_product_names(self) -> list[str]:
        """Return list of all product names currently in the cart."""
        name_locators = self.page.locator(self.CART_PRODUCT_NAMES)
        count = await name_locators.count()
        names = []
        for i in range(count):
            name = await name_locators.nth(i).inner_text()
            names.append(name.strip())
        logger.info(f"Cart products: {names}")
        return names

    async def is_product_in_cart(self, product_name: str) -> bool:
        """
        Check if a specific product name exists in the cart.
        Case-insensitive partial match — more robust than exact match.
        """
        names = await self.get_all_cart_product_names()
        for name in names:
            if product_name.lower() in name.lower():
                logger.info(f"Found '{product_name}' in cart")
                return True
        logger.warning(f"'{product_name}' NOT found in cart. Cart has: {names}")
        return False

    async def is_cart_empty(self) -> bool:
        """Returns True if cart is empty."""
        return await self.is_visible(self.EMPTY_CART_MSG)

    async def remove_first_item(self) -> None:
        """Click the × button on the first cart item to remove it."""
        first_remove = self.page.locator(self.REMOVE_BUTTON).first
        await first_remove.click()
        # Wait for cart to update after removal
        await self.page.wait_for_timeout(1000)
        logger.info("Removed first item from cart")

    async def get_item_quantity(self, index: int = 0) -> int:
        """Get quantity of item at given index (0 = first item)."""
        qty_text = await self.page.locator(
            self.CART_QUANTITY
        ).nth(index).inner_text()
        return int(qty_text.strip())