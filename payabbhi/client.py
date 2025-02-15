from types import ModuleType
import requests

from . import resources, utility

# dict of resource classes which contian underscore 
resource_name_with_underscore_dict =	{
  "payment_link": "Payment_Link",
  "virtual_account": "Virtual_Account",
}
def capitalize_camel_case(string):
    if string in resource_name_with_underscore_dict.keys():
        return  resource_name_with_underscore_dict[string]
    else:
        return "".join(map(str.capitalize, string.split('_')))

# Create a dict of resource classes
RESOURCE_CLASSES = {}

for resource_name, resource_module in resources.__dict__.items():
    if isinstance(resource_module, ModuleType) and capitalize_camel_case(resource_name) in resource_module.__dict__:
        # this if is required so that classes contian underscore in the name could be left intect
        if resource_name in resource_name_with_underscore_dict.keys():
            RESOURCE_CLASSES[resource_name] = resource_module.__dict__[capitalize_camel_case(resource_name)]
        else:
            RESOURCE_CLASSES[resource_name.replace("_","")] = resource_module.__dict__[capitalize_camel_case(resource_name)]

UTILITY_CLASSES = {}
for utility_name, utility_module in utility.__dict__.items():
    if isinstance(utility_module, ModuleType) and utility_name.capitalize() in utility_module.__dict__:
        UTILITY_CLASSES[utility_name] = utility_module.__dict__[utility_name.capitalize()]


class Client(object):

    VERSION = '1.0.3'

    def __init__(self, access_id="", secret_key=""):
        self.session = requests.Session()
        self.access_id = access_id
        self.secret_key = secret_key

        self.cert_path = False
        self.app_info = {}

        # intializes each resource
        # injecting this client object into the constructor
        for resource_class_name, resource_klass in RESOURCE_CLASSES.items():
            setattr(self, resource_class_name, resource_klass(self))

        for utility_class_name, utility_klass in UTILITY_CLASSES.items():
            setattr(self, utility_class_name, utility_klass(self))

    def set_app_info(self, app_name, app_version="", app_url=""):
        self.app_info = {
            'name': app_name,
            'version': app_version,
            'url': app_url,
        }

    def get_app_info(self):
        return self.app_info
