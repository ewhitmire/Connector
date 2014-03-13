from connector.models import *

def can_user_edit_profile(user, member):
	return user.member == member

def can_user_edit_skill(user, skill):
	return user.member == skill.member

def can_user_edit_offer(user, offer):
	return user.member == offer.member