from django import template

register = template.Library()

@register.filter
def sort_by_amount(bids):
    return sorted(bids, key=lambda bid: bid.amount, reverse=True)