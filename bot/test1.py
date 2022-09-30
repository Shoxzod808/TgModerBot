import config
from backend.models import Group
print(Group.objects.all()[0].user)