
from sqlalchemy.orm import sessionmaker
from ...view.basic_models import IndexInfo
from ...wrapper.mysql import BasicDatabaseConnector


def update_index_info_column():
    '''更新index_info中em_id列的值'''

    def modify_func(order_book_id: str) -> str:
        e = order_book_id.split('.')
        if len(e) < 2:
            return e

        if e[1] == 'XSHG':
            return e[0]+'.'+'SH'
        elif e[1] == 'XSHE':
            return e[0]+'.'+'SZ'
        else:
            return e

    Session = sessionmaker(BasicDatabaseConnector().get_engine())
    db_session = Session()
    for row in db_session.query(IndexInfo).filter(IndexInfo.tag_method.in_(['PE百分位', 'PB百分位', 'PS百分位'])).all():
        row.em_id = modify_func(row.order_book_id)
    db_session.commit()
    db_session.close()
