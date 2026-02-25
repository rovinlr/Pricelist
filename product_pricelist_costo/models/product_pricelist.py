from odoo import models


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    def _compute_price_rule(self, products_qty_partner, *args, **kwargs):
        prices = super()._compute_price_rule(products_qty_partner, *args, **kwargs)

        rule_ids = [rule_id for _price, rule_id in prices.values() if rule_id]
        rules = self.env["product.pricelist.item"].browse(rule_ids)
        cost_rules = {rule.id: rule for rule in rules if rule.compute_price == "costo"}

        if not cost_rules:
            return prices

        for product, _qty, _partner in products_qty_partner:
            if not product:
                continue
            product_data = prices.get(product.id)
            if not product_data:
                continue
            _price, rule_id = product_data
            cost_rule = cost_rules.get(rule_id)
            if cost_rule:
                prices[product.id] = (cost_rule._compute_costo_price(), rule_id)

        return prices
