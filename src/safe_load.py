import asyncio


async def safe_load(
    page,
    initial_wait: int = 10,
    after_scroll_wait: int = 3,
    scroll_pixels: int = 300
) -> None:
    """
    Waits for a page to fully load, scrolls to trigger dynamic content, then minimizes the page.

    Args:
        page: A browser automation page object (e.g., from Playwright or Selenium).
        initial_wait: Seconds to wait after initial load to ensure all scripts settle.
        after_scroll_wait: Seconds to wait after scrolling for lazy-loaded elements.
        scroll_pixels: Vertical scroll distance to help trigger content loading.
    """
    # Ensure the DOM is fully loaded
    await page.wait_for_ready_state(until="complete")
    await asyncio.sleep(initial_wait)

    # Scroll slightly to trigger any dynamic/lazy content loading
    await page.scroll_down(scroll_pixels)
    await asyncio.sleep(after_scroll_wait)

    # Minimize the browser to ensure visibility of the upcoming input prompt
    await page.minimize()