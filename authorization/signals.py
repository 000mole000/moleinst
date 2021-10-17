from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver

from authorization.models import UserProfile


@receiver(user_signed_up)
def create_profile(user, sociallogin=None, **kwargs):

    if sociallogin:
        if sociallogin.account.provider == 'github':
            print('soc', sociallogin.account.extra_data['avatar_url'])
            user.save()
            profile = UserProfile(user=user, avatar_url=sociallogin.account.extra_data['avatar_url'])
            profile.save()
        if sociallogin.account.provider == 'discord':
            print('soc', sociallogin.account.extra_data['avatar'])
            user.save()
            if sociallogin.account.extra_data['avatar']:
                profile = UserProfile(user=user, avatar_url='https://cdn.discordapp.com/avatars/'+sociallogin.account.extra_data['id']+'/'+sociallogin.account.extra_data['avatar']+'.png')
                profile.save()
            else:
                profile = UserProfile(user=user)
                profile.save()

    else:
        user.save()
        profile = UserProfile(user=user)
        profile.save()
