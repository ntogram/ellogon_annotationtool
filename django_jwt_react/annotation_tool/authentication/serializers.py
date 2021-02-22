from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import CustomUser, Project, Collection, Document
from .send_email import EmailAlert

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):


        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['fav_color'] = user.fav_color
        return token

# ...
class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(
        required=True
    )
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)  # as long as the fields are the same, we can just use this
        if password is not None:
            instance.set_password(password)
        instance.is_active=False
        instance.save()
        #Send confirmation mail

        #activation_alert=EmailAlert(instance.email,instance.username)
        #activation_alert.send_activation_email()
        return instance

    class ProjectSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Project
            fields = '__all__'

    class CollectionSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Collection
            fields = '__all__'

    class DocumentSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Document
            fields = '__all__'