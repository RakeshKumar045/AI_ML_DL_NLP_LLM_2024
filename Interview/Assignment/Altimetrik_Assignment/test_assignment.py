
import unittest

class Item:
    def __init__(self, name, price, quantity):
        # Initialize an Item object with a name, price, and quantity.
        self.name = name  # The name of the item
        self.price = price  # The price of the item
        self.quantity = quantity  # The quantity of the item in stock

class Cart:
    def __init__(self):
        # Initialize a shopping cart with an empty list of items and a total price of 0.
        self.items = []
        self.total_price = 0

    def add_item(self, item):
        # Add an item to the shopping cart if it's in stock, and update the total price.
        if item.quantity > 0:
            self.items.append(item)
            self.total_price += item.price * item.quantity
        else:
            # If the item is out of stock, print a message.
            print("Item out of stock.")

    def remove_item(self, item):
        # Remove an item from the shopping cart if it's present and update the total price.
        if item in self.items:
            self.items.remove(item)
            self.total_price -= item.price * item.quantity
        else:
            # If the item is not in the cart, print a message.
            print("Item not in cart.")

    def checkout(self):
        # Calculate and print the total amount to pay in a specific format.
        print("Total amount to pay: ${:.2f}".format(self.total_price))

    def view_all_items(self):
        # Display the names, quantities, and prices of all items in the shopping cart.
        print("Items in cart:")
        for item in self.items:
            print("{} - {} x ${:.2f}".format(item.name, item.quantity, item.price))

def main():
    # Create a Cart instance.
    cart = Cart()

    # Add items to the cart.
    cart.add_item(Item("Orange", 3, 2))
    cart.add_item(Item("Banana", 2, 1))
    cart.add_item(Item("Watermelon", 5, 1))

    # Remove an item from the cart.
    cart.remove_item(Item("Banana", 2, 1))

    # View all items in the cart.
    cart.view_all_items()

    # Proceed to checkout.
    cart.checkout()

# if __name__ == "__main__":
#     main()

class TestCart(unittest.TestCase):

    def test_add_item(self):
        # Create a cart object.
        cart = Cart()

        # Add an item to the cart.
        cart.add_item(Item("Orange", 3, 2))

        # Check that the item was added to the cart.
        self.assertIn(Item("Orange", 3, 2), cart.items)

    def test_remove_item(self):
        # Create a cart object.
        cart = Cart()

        # Add an item to the cart.
        cart.add_item(Item("Banana", 2, 1))

        # Remove the item from the cart.
        cart.remove_item(Item("Banana", 2, 1))

        # Check that the item was removed from the cart.
        self.assertNotIn(Item("Banana", 2, 1), cart.items)

    def test_checkout(self):
        # Create a cart object.
        cart = Cart()

        # Add items to the cart.
        cart.add_item(Item("Orange", 3, 2))
        cart.add_item(Item("Banana", 2, 1))
        cart.add_item(Item("Watermelon", 5, 1))

        # Checkout.
        cart.checkout()

        # Check that the total price is correct.
        self.assertEqual(cart.total_price, 16.0)

if __name__ == "__main__":
    unittest.main()

