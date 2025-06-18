import pytest
import ckan.plugins as plugins


@pytest.mark.ckan_config("ckan.plugins", "onboarding_baglan_adaskhan")
@pytest.mark.usefixtures("with_plugins")
def test_plugin():
    assert plugins.plugin_loaded("onboarding_baglan_adaskhan")
