import logging
from playwright.async_api import Page
from aria.base_page import BasePage

logger = logging.getLogger(__name__)


class ProductsPage(BasePage):
    """
    Page Object for automationexercise.com/products page.
    Handles product search, listing, and adding items to cart.
    """

    # --- Selectors ---
    SEARCH_INPUT = "input#search_product"
    SEARCH_BUTTON = "button#submit_search"
    PRODUCT_LIST = "div.productinfo"
    PRODUCT_NAMES = "div.productinfo p"
    CONTINUE_SHOPPING = "button:has-text('Continue Shopping')"
    # VIEW_CART = "p:has-text('View Cart')"
    VIEW_CART = "role=link[name='View Cart']"
    NO_RESULTS = "p:has-text('no products found')"

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://automationexercise.com/products"

    async def open(self) -> "ProductsPage":
        """Navigate to products page."""
        await self.navigate(self.url)
        logger.info("Products page opened")
        return self

    async def search(self, keyword: str) -> "ProductsPage":
        """Search for a product by keyword."""
        logger.info(f"Searching for: '{keyword}'")
        await self.fill(self.SEARCH_INPUT, keyword)
        await self.click(self.SEARCH_BUTTON)
        await self.page.wait_for_load_state("domcontentloaded")
        return self

    async def get_product_count(self) -> int:
        """Return how many products are currently visible."""
        count = await self.page.locator(self.PRODUCT_LIST).count()
        logger.info(f"Found {count} products on page")
        return count

    async def get_all_product_names(self) -> list[str]:
        """Return list of all visible product names."""
        name_locators = self.page.locator(self.PRODUCT_NAMES)
        count = await name_locators.count()
        names = []
        for i in range(count):
            name = await name_locators.nth(i).inner_text()
            names.append(name.strip())
        return names

    async def add_first_product_to_cart(self) -> str:
        """
        Hover over the first product and click Add to Cart.
        Uses .first on the button to avoid strict mode violation
        when two overlapping buttons exist in the DOM.
        Returns the product name for cart verification.
        """
        # Get product name before clicking
        first_product_name = await self.page.locator(
            self.PRODUCT_NAMES
        ).first.inner_text()

        # Hover to reveal the Add to Cart button
        first_card = self.page.locator("div.product-image-wrapper").first
        await first_card.hover()

        # Wait for hover animation
        await self.page.wait_for_timeout(500)

        # .first resolves the strict mode violation (two buttons in DOM)
        first_add_btn = self.page.locator(
            "div.product-image-wrapper"
        ).first.locator("a.add-to-cart").first

        await first_add_btn.click()

        logger.info(f"Added to cart: '{first_product_name.strip()}'")
        return first_product_name.strip()

    async def continue_shopping(self) -> None:
        """Click Continue Shopping on the modal after adding to cart."""
        await self.click(self.CONTINUE_SHOPPING)

    # async def go_to_cart(self) -> None:
    #     """Click View Cart on the modal after adding to cart."""
    #     await self.click(self.VIEW_CART)
    # async def go_to_cart(self) -> None:
    #     """Click View Cart on the modal after adding to cart."""
    #     await self.page.get_by_role("link", name="View Cart").click()
    #     await self.page.wait_for_url("**/view_cart**", timeout=8000)
    # logger.info("Navigated to cart page")
    
    async def go_to_cart(self) -> None:
        """
    Click View Cart specifically inside the modal dialog.
    We scope the click to div.modal-content to avoid hitting
    the navbar's View Cart link which is also on the page.
    """
    # Scope the click to ONLY inside the modal — ignores navbar link
        await self.page.locator("div.modal-content").get_by_text("View Cart").click()
        await self.page.wait_for_url("**/view_cart**", timeout=8000)
    logger.info("Navigated to cart page via modal")

    async def is_no_results_shown(self) -> bool:
        """Returns True if no products found message is visible."""
        return await self.is_visible(self.NO_RESULTS)