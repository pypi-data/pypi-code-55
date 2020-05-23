import logging

from django.core.management import BaseCommand
from django.db import transaction, connection, IntegrityError
from tqdm import tqdm

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Тестирование"

    def handle(self, *args, **options):
        logger.info(self.help)

        with connection.cursor() as cursor:
            cursor.execute(f'''with a as (
                                select trim(value_str), attr_type_id, att.code, count(*)
                                from kd_document_attributes
                                join ckk_attr_type att on att.id = kd_document_attributes.attr_type_id
                                where value_str is not null
                                group by delete_dbl_spaces(value_str), attr_type_id, att.code
                                having count(*) > 1
                            )
                            
                            select count(*)
                            from a''')
            qty, = cursor.fetchone()
            pbar = tqdm(total=qty)
            deleted_cnt = 0
            not_deleted_cnt = 0

            # with transaction.atomic():
            cursor.execute(f'''with a as (
                                            select trim(value_str), attr_type_id, att.code, count(*)
                                            from kd_document_attributes
                                            join ckk_attr_type att on att.id = kd_document_attributes.attr_type_id
                                            where value_str is not null
                                            group by delete_dbl_spaces(value_str), attr_type_id, att.code
                                            having count(*) > 1
                                        )

                                        select *
                                        from a''')

            rows = cursor.fetchall()

            for row in rows:
                value_str, attr_type_id, code, count = row

                cursor.execute(f'''select id
                                    from kd_document_attributes
                                    where trim(value_str) = %s
                                      and attr_type_id = %s
                                    order by id''', [value_str.strip(), attr_type_id])
                rows1 = cursor.fetchall()
                for row1 in rows1:
                    id, = row1
                    try:
                        cursor.execute(f'''delete from kd_document_attributes where id=%s''', [id])
                        deleted_cnt += 1
                    except IntegrityError:
                        not_deleted_cnt += 1
                    # if step_first:
                    #     step_first = False
                    #     id_main = id
                    # else:
                    #     # res = Item.objects.filter(STMP_1_id=id).update(STMP_1=id_main)
                    #     # res = Item.objects.filter(STMP_2_id=id).update(STMP_2=id_main)
                    #     # res = Document_attr_cross.objects.filter(attribute_id=id).update(attribute_id=id_main)
                    #     cursor.execute(f'''delete from kd_document_attributes where id=%s''', [id])
                if pbar:
                    pbar.update(1)

        if pbar:
            pbar.close()
            print(f'Deleted: {deleted_cnt}')
            print(f'Not Deleted: {not_deleted_cnt}')
