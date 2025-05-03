import asyncio
import random
from typing import Union

def ask_scroll_input() -> Union[int, None]:
    """
    Asks the user if they want to input a custom scroll range.

    Returns:
        int: The amount to scroll if the user inputs a valid number.
        None: If the user does not want to input a custom scroll range.
    """
    scroll_ask = input("Do you want to input a custom page scroll range (translates to amount of jobs scraped)? Y/N: ").strip().lower()
    if scroll_ask == "y":
        # Ensures the input is valid and continues asking until a valid input is given.
        while True:
            scroll_amount = input("Enter amount to scroll - 500 equals approximately 50 more jobs (approximately 96 jobs by default), limit is 21000: ")
            try:
                scroll_amount = int(scroll_amount)
                if scroll_amount <= 0:
                    print("Please enter a positive number.")
                    continue
                elif scroll_amount > 21000:
                    print("Maximum scroll limit reached (21000). Setting to maximum value.")
                    return 21000
                else:
                    return scroll_amount
            except ValueError:
                print("Invalid input! Please enter a valid number.")
    else:
        return None

async def custom_scroll(page, scroll_amount: Union[int, None]) -> None:
    """
    Simulates real-life user scrolling by dividing the scroll range into smaller intervals.

    Args:
        page: The page object (from a browser automation library like Zendriver).
        scroll_amount: The total number of pixels to scroll. If None, no scrolling occurs.

    Returns:
        None
    """
    if scroll_amount is None:
        return

    max_amount = 21000
    if scroll_amount > max_amount:
        print(f"Limit reached, defaulting to maximum amount of {max_amount} pixels.")
        scroll_amount = max_amount
    
    # Define the divider for the scroll amount based on the total scroll amount.
    if scroll_amount >= 15000:
        divider = 30
    elif scroll_amount >= 10000:
        divider = 20
    elif scroll_amount >= 5000:
        divider = 10
    else:
        divider = 7

    divided_amount = scroll_amount / divider

    # Perform the scroll action at divided intervals
    for _ in range(divider):
        await page.scroll_down(divided_amount)  # Scroll down the page by the divided amount
        interval = random.uniform(1, 3)  # Random interval between scroll actions
        await asyncio.sleep(interval)
