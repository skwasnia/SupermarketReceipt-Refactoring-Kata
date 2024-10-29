import math
import csv

from model_objects import ProductQuantity, SpecialOfferType, Discount


class ShoppingCart:
    def __init__(self, cart_file=None, catalog=None):
        self._items = []
        self._product_quantities = {}

        if not cart_file:
            return

        if not catalog:
            return

        with open(cart_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['name']
                quantity = float(row['quantity'])
                product = catalog.products[name]
                self.add_item_quantity(product, quantity)

    @property
    def items(self):
        return self._items

    def add_item(self, product):
        self.add_item_quantity(product, 1.0)

    @property
    def product_quantities(self):
        return self._product_quantities

    def add_item_quantity(self, product, quantity):
        self._items.append(ProductQuantity(product, quantity))
        if product in self._product_quantities.keys():
            self._product_quantities[product] = self._product_quantities[product] + quantity
        else:
            self._product_quantities[product] = quantity

    def _get_offers_factor(self, p, quantity, offer, unit_price, quantity_as_int):
        x = 1
        discount = None

        if offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
            x = 3

        elif offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
            x = 2
            if quantity_as_int >= 2:
                total = offer.argument * (quantity_as_int / x) + quantity_as_int % 2 * unit_price
                discount_n = unit_price * quantity - total
                discount = Discount(p, "2 for " + str(offer.argument), -discount_n)
        elif offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
            x = 5

        return (x, discount)

    def handle_offers(self, receipt, offers, catalog):
        for p in self._product_quantities.keys(): # For each item
            quantity = self._product_quantities[p]
            if p in offers.keys(): # If item in the offer
                offer = offers[p]
                unit_price = catalog.unit_price(p)
                quantity_as_int = int(quantity)

                x, discount = self._get_offers_factor(p, quantity, offer, unit_price, quantity_as_int)

                if offer.offer_type == SpecialOfferType.THREE_FOR_TWO and quantity_as_int > 2:
                    discount_amount = quantity * unit_price - (
                                (math.floor(quantity_as_int / 3) * 2 * unit_price) + quantity_as_int % 3 * unit_price)
                    discount = Discount(p, "3 for 2", -discount_amount)

                if offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
                    discount = Discount(p, str(offer.argument) + "% off",
                                        -quantity * unit_price * offer.argument / 100.0)

                if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT and quantity_as_int >= 5:
                    discount_total = unit_price * quantity - (
                                offer.argument * math.floor(quantity_as_int / 5) + quantity_as_int % 5 * unit_price)
                    discount = Discount(p, str(x) + " for " + str(offer.argument), -discount_total)

                if discount:
                    receipt.add_discount(discount)
