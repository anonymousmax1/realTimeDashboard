from dashboard.models import *

class DataDomain():
    def get_all():
        return Data.objects.all()
    
    def add_or_update(label, value) -> bool:
        try:
            obj = Data.objects.get(label=label)
            obj.value = value
            obj.save()
            return True
        except Data.DoesNotExist:
            obj = Data(label=label, value=value)
            obj.save()
            return True
        except:
            return False