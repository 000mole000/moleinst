# import redis
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# import json
#
# from blog.blog_serializers import PostAlertSerializer


# @receiver(post_save, sender="blog.Post")
# def create_post(sender, instance, created, **kwargs):
#     if created:
#         post = PostAlertSerializer(instance)
#         print('post', post.data)
#         pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
#         r = redis.Redis(connection_pool=pool)
#         r2 = r.publish('create_post', json.dumps(post.data))
