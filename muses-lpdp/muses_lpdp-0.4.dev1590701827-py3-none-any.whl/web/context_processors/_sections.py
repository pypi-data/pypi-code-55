from db.models import Section


def sections(request):
    list_sections = Section.objects.all().order_by("order")
    return {'sections': list_sections}
