from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from chat.models import MessageModel
from rest_framework.serializers import ModelSerializer, CharField
from django.contrib import messages

from django.db.models.signals import post_save
from notifications.signals import notify
from chat.models import MessageModel


# def my_handler(sender, instance, created, **kwargs):
#     notify.send(instance, verb='was saved')


# post_save.connect(my_handler, sender=MessageModel)


class MessageModelSerializer(ModelSerializer):
    user = CharField(source='user.username', read_only=True)
    recipient = CharField(source='recipient.username')

    def create(self, validated_data):
        user = self.context['request'].user
        recipient = get_object_or_404(
            User, username=validated_data['recipient']['username'])
        msg = MessageModel(recipient=recipient,
                           body=validated_data['body'],
                           user=user)
        msg.save()
        # (user, recipient, msg)
        notify.send(user, recipient=recipient,
                    verb="sent you a new message", description=msg.body)
        # print("This message is saved in backend", user, recipient, msg)
        return msg

    class Meta:
        model = MessageModel
        fields = ('id', 'user', 'recipient', 'timestamp', 'body')


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
