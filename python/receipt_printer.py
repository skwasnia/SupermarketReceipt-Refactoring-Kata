from model_objects import ProductUnit

class ReceiptPrinter:

    def __init__(self, columns=40):
        self.columns = columns

    def print_receipt(self, receipt):
        return self._print_receipt_items(receipt) \
            + self._print_discounts(receipt) \
            + "\n" \
            + self._present_total(receipt)

    def _print_discounts(self, receipt):
        result = ""

        for discount in receipt.discounts:
            discount_presentation = self._print_discount(discount)
            result += discount_presentation

        return result

    def _print_receipt_items(self, receipt):
        result = ""

        for item in receipt.items:
            receipt_item = self._print_receipt_item(item)
            result += receipt_item

        return result

    def _print_receipt_item(self, item):
        total_price_printed = self._print_price(item.total_price)
        name = item.product.name
        line = self._format_line_with_whitespace(name, total_price_printed)
        if item.quantity != 1:
            line += f"  {self._print_price(item.price)} * {self._print_quantity(item)}\n"
        return line

    def _format_line_with_whitespace(self, name, value):
        line = name
        whitespace_size = self.columns - len(name) - len(value)
        for i in range(whitespace_size):
            line += " "
        line += value
        line += "\n"
        return line

    def _print_price(self, price):
        return "%.2f" % price

    def _print_quantity(self, item):
        if ProductUnit.EACH == item.product.unit:
            return str(item.quantity)
        else:
            return '%.3f' % item.quantity

    def _print_discount(self, discount):
        name = f"{discount.description} ({discount.product.name})"
        value = self._print_price(discount.discount_amount)
        return self._format_line_with_whitespace(name, value)

    def _present_total(self, receipt):
        name = "Total: "
        value = self._print_price(receipt.total_price())
        return self._format_line_with_whitespace(name, value)
