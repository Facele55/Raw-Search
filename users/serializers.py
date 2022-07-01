from rest_framework import serializers

from core.models import Autocomplete
from users.models import CustomUser


class AutocompleteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Autocomplete
		fields = '__all__'
