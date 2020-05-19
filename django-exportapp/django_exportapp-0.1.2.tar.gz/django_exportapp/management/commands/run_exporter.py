# import datetime

from django.core.management.base import BaseCommand

from django_exportapp.helper import exporter
from django.core import serializers
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
# from subprocess import call
from django.db import models


def dump_model_to_xml(target, data=None, mode='public'):
    if mode == 'public':
        dump_dir = settings.EXPORTAPP_PUBLIC_DIR
    if mode == 'private':
        dump_dir = settings.EXPORTAPP_PRIVATE_DIR
    #
    if data:
        print('{} [serializers]'.format(target))
        s = serializers.serialize(
            'xml',
            data,
            indent=4,
            use_natural_foreign_keys=False,
            use_natural_primary_keys=False,
        )
        out = open("{}/{}.xml".format(dump_dir, target), "w")
        out.write(s)
        out.close()
        print('{} [records {}]'.format(target, data.count()))
    return True


def run_dump(mode='public'):
    for i in ContentType.objects.all():
        if i.app_label == 'auth' and i.model == 'permission':
            continue
        if i.app_label == 'admin':
            continue
        if i.app_label == 'captcha':
            continue
        if i.app_label == 'contenttypes':
            continue
        if i.app_label == 'sessions':
            continue
        if i.app_label == 'hitcount':
            continue
        #
        try:
            dump_py_class = exporter.arr[i.model_class()]
        except Exception:
            try:
                # if application was remove, but stale in database
                data = i.model_class().objects.all()
            except Exception:
                print(
                    'Possibly application "{}" and model "{}" were remove, but exist stale contenttypes?'.format(
                        i.app_label, i.model
                    )
                )
            else:
                dump_model_to_xml('{}.{}'.format(i.app_label, i.model), data=data, mode=mode)
            pass
        else:
            if dump_py_class.export_status is True:
                if mode in dump_py_class.export_mode:
                    #
                    data = i.model_class().objects.all()
                    #
                    if mode == 'public':
                        for row in data:
                            for field in row._meta.get_fields(include_parents=False, include_hidden=False):
                                pass
                                if isinstance(field, models.CharField) or isinstance(field, models.EmailField) or isinstance(field, models.FloatField) or isinstance(field, models.IntegerField) or isinstance(field, models.TextField):
                                    # print(i.__dict__[f.name])
                                    # print(dir(i._meta.get_field(field.name)))
                                    # print(row.__dict__)
                                    value = row.__dict__[field.name]
                                    # print(field.name, '=', value)
                                    setattr(row, field.name, exporter.arr[i.model_class()].return_field_value(field.name, value))
                    if mode == 'private':
                        pass
                    #
                    dump_model_to_xml('{}.{}'.format(i.app_label, i.model), data=data, mode=mode)


# def run_tar(mode='public'):
#     ctime_format = "%Y%m%d_%H%M%S"
#     now = datetime.datetime.now()
#     fielname = now.strftime(ctime_format)
#     print(fielname)
#     call([
#         'tar',
#         '-czvf',
#         '{}/{}_{}_xml.tar.gz'.format(settings.EXPORTAPP_ARCH_DIR, settings.EXPORTAPP_PREFIX_NAME, fielname),
#         settings.EXPORTAPP_PRIVATE_DIR,
#     ])


class Command(BaseCommand):
    """Export models"""

    help = "export all models from _exportapp.py"

    def add_arguments(self, parser):
        parser.add_argument(
            '--mode',
            action='store',
            type=str,
            required=False,
            choices=('public', 'private'),
            help='public or private',
        )

        # parser.add_argument(
        #     '--tar',
        #     action='store_true',
        #     help='make tar',
        # )

    def handle(self, *args, **options):
        """The function that export data"""
        print('handle')
        print(options['mode'])

        if options['mode']:
            if options['mode'] == 'private':
                # print('privare')
                run_dump(mode='private')
                # run_tar()
            if options['mode'] == 'public':
                print('public')
                run_dump(mode='public')
        else:
            print('public')
            run_dump(mode='public')

        # if options['tar']:
        #     print('tar')
        #     if options['mode']:
        #         run_tar(mode=options['mode'])
        #     else:
        #         run_tar()

        self.stdout.write(
            self.style.SUCCESS(
                'Done'
            )
        )
