from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from authorization.models import UserProfile, Subscribe


class UserSerializer(UserDetailsSerializer):

    avatar_url = serializers.CharField(source="userprofile.avatar_url")
    avatar = serializers.ImageField(source="userprofile.avatar")
    subscribers_count = serializers.IntegerField(source="subscribers.all.count")
    subscribed = serializers.SerializerMethodField()

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('avatar_url', 'avatar', 'subscribers_count', 'subscribed')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', {})
        avatar_url = profile_data.get('avatar_url')
        avatar = profile_data.get('avatar')

        instance = super(UserSerializer, self).update(instance, validated_data)
        # get and update user profile
        profile = instance.userprofile
        if profile_data and avatar:
            profile.avatar = avatar
        elif profile_data and avatar_url:
            profile.avatar_url = avatar_url
        profile.save()
        return instance

    def get_subscribed(self, obj):
        print('conn', self.context['request'].user.id, obj.id, Subscribe.objects.filter(subscriber=self.context['request'].user.id, user=obj.id).exists())
        return Subscribe.objects.filter(subscriber=self.context['request'].user.id, user=obj.id).exists()
