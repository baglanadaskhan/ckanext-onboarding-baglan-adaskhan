import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.onboarding_baglan_adaskhan.views.home import home
from ckanext.onboarding_baglan_adaskhan.views.admin import admin
from ckanext.onboarding_baglan_adaskhan.views.user import user
from ckanext.onboarding_baglan_adaskhan.views.dataset import dataset
from ckanext.onboarding_baglan_adaskhan.lib.helpers import get_helpers

log = logging.getLogger(__name__)

# import ckanext.onboarding_baglan_adaskhan.cli as cli
# import ckanext.onboarding_baglan_adaskhan.helpers as helpers
# import ckanext.onboarding_baglan_adaskhan.views as views
from ckan.lib.plugins import DefaultTranslation
from ckanext.onboarding_baglan_adaskhan.logic import (
    action, auth
)


class OnboardingBaglanAdaskhanPlugin(plugins.SingletonPlugin, DefaultTranslation, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IDatasetForm, inherit=False)
    # plugins.implements(plugins.IClick)
    plugins.implements(plugins.ITemplateHelpers)
    # plugins.implements(plugins.IValidators)
    

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "onboarding_baglan_adaskhan")
        log.debug("Hello World")

    
    # IAuthFunctions

    def get_auth_functions(self):
        return {
            "dataset_review": auth.dataset_review,
            "package_update": auth.package_update
        }

    # IActions

    def get_actions(self):
        return {
            "hello_world": action.hello_world,
            "package_search": action.package_search,
            "dataset_review": action.dataset_review,
        }

    # IBlueprint

    def get_blueprint(self):
        return [home, admin, user, dataset]

    # IClick

    # def get_commands(self):
    #     return cli.get_commands()

    # ITemplateHelpers

    def get_helpers(self):
        return get_helpers()

    # IValidators

    # def get_validators(self):
    #     return validators.get_validators()
    

    # IDatasetForm

    def is_fallback(self):
        return True

    def package_types(self):
        return []

    def _modify_package_schema(self, schema):
        schema.update(
            {
                "review_status": [
                    toolkit.get_validator("ignore_missing"),
                    toolkit.get_converter("convert_to_extras"),
                ]
            }
        )
        return schema

    def create_package_schema(self):
        schema = super(OnboardingBaglanAdaskhanPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(OnboardingBaglanAdaskhanPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(OnboardingBaglanAdaskhanPlugin, self).show_package_schema()
        schema.update({"review_status": [toolkit.get_converter("convert_from_extras")]})
        return schema

    def setup_template_variables(self, context, data_dict):
        return super(OnboardingBaglanAdaskhanPlugin, self).setup_template_variables(
            context, data_dict
        )

    def new_template(self):
        return super(OnboardingBaglanAdaskhanPlugin, self).new_template()

    def read_template(self):
        return super(OnboardingBaglanAdaskhanPlugin, self).read_template()

    def edit_template(self):
        return super(OnboardingBaglanAdaskhanPlugin, self).edit_template()

    def search_template(self):
        return super(OnboardingBaglanAdaskhanPlugin, self).search_template()

    def history_template(self):
        return super(OnboardingBaglanAdaskhanPlugin, self).history_template()

    def package_form(self):
        return super(OnboardingBaglanAdaskhanPlugin, self).package_form()
