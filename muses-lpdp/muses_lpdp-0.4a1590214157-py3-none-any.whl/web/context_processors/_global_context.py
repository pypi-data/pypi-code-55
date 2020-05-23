from datetime import datetime, date

from db.models import SiteParam
from web.forms import ThemeSelectorForm


def global_context(request):
    l_site_params = {}
    site_params = SiteParam.objects.all()

    for item in site_params:
        l_site_params[item.key] = item.value

    temp = {
        'site_number_of_days_since_creation': (datetime.now() - datetime(year=2000, month=3, day=7)).days,
        'site_number_of_days_until_birthday':
            (date(year=(datetime.now().year + 1), month=3, day=7) -
             date(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)).days,
    }

    context = {**l_site_params, **temp}

    if request.user.is_authenticated:
        f = ThemeSelectorForm()
        f.fields['theme'].initial = request.user.theme
        context.update(
            {'theme_selector_form': f}
        )
        context.update(
            {'selected_theme': f"web/css/{request.user.theme}.css"}
        )

    return context
