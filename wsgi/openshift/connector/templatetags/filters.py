from django import template
from connector import permissions

register = template.Library()

@register.filter
def can_edit_profile(user, member):
    return permissions.can_user_edit_profile(user, member)

@register.filter
def can_edit_skill(user, skill):
    return permissions.can_user_edit_skill(user, skill)

@register.filter
def can_edit_offer(user, offer):
    return permissions.can_user_edit_offer(user, offer)
   
@register.inclusion_tag('skills/skill_badge.html')
def skill_badge(skill):
    return {'skill': skill}

@register.inclusion_tag('offers/offer_badge.html')
def offer_badge(offer):
    return {'offer': offer}

@register.inclusion_tag('offers/offer_minibadge.html')
def offer_minibadge(offer):
    return {'offer': offer}

@register.inclusion_tag('skills/skill_minibadge.html')
def skill_minibadge(skill):
    return {'skill': skill}

@register.filter
def joinby(value, arg):
    return arg.join([str(x) for x in value])