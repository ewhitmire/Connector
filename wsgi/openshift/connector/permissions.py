from connector.models import *

def can_user_edit_profile(user, member):
	if not hasattr(user, 'member'): 
		return False
	return user.member == member

def can_user_edit_skill(user, skill):	
	if not hasattr(user, 'member'):
		return False
	return user.member == skill.member

def can_user_edit_offer(user, offer):	
	if not hasattr(user, 'member'):
		return False
	return user.member == offer.member