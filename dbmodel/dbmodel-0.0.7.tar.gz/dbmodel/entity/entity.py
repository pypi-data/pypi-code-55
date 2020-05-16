# -*- coding: utf-8 -*-

__private_methods__ = ["toJSON", "toDB"]

from dbmodel.entity.datatype import *
from dbmodel.entity.status import EntityStatus
from dbmodel.utils.inflector import Inflector, Portugues


class Entity(object):

    def __init__(self, context=None, **kw):
        try:
            self.__context__ = context
            self.__commit__ = []
            self.__status__ = EntityStatus.created
            self.__table__ = Inflector(Portugues).tableize(
                self.__class__.__name__)
            filled = False
            for item in self.__dir__():
                if not item.startswith("__") and item not in __private_methods__:
                    self.__dict__["__%s" % item] = self.__getattribute__(item)
                    if self.__dict__["__%s" % item].name and not self.__dict__["__%s" % item].type:
                        self.__dict__["__%s" % item].type = getattr(__import__('model.{0}'.format(self.__dict__["__%s" % item].name.lower(
                        )), fromlist=[self.__dict__["__%s" % item].name]), self.__dict__["__%s" % item].name)
                    self.__dict__[item] = None if self.__dict__["__%s" % item].__class__.__name__ != "ObjectList" and self.__dict__["__%s" % item].__class__.__name__ != "ObjectManyList" else ListType(
                        context=self, type=self.__dict__["__%s" % item].type)
                    if item in kw:
                        filled = True
                        self.__setattr__(item, kw[item])
                        del kw[item]
                    elif "%s.%s" % (self.__table__, item) in kw:
                        filled = True
                        self.__setattr__(
                            item, kw["%s.%s" % (self.__table__, item)])
                        del kw["%s.%s" % (self.__table__, item)]
            if len(kw) > 0:
                filled = True
                self.__setrelattr__(**kw)

            # TEST IF CONTEXT IS DATABASE
            __DB_CONTEXT = self.__context__
            if __DB_CONTEXT and filled:
                while __DB_CONTEXT:
                    if __DB_CONTEXT.__class__.__name__ == "Connection" and filled:
                        self.__status__ = EntityStatus.filled
                    __DB_CONTEXT = __DB_CONTEXT.__context__ if '__context__' in  __DB_CONTEXT.__dict__ else None
        except Exception as e:
            raise e

    def __setrelattr__(self, **kw):
        rel_kw = {item.split(".")[0] : { } for item in kw if "." in item and not "%s." % self.__table__ in item}
        if len(rel_kw)>0:
            for _table in rel_kw:
                _data = {key.split(".")[1] : value for key, value in kw.items() if key.startswith("{}.".format(_table))}
                if len(_data) > 0:
                    field = self.__getattribute__("__%s" % _table)

                    if field.__class__.__name__ == "Object":
                        self.__dict__[_table] = field.type(context=self, **_data)

                    if field.__class__.__name__ == "ObjectList":
                        object = field.type(context=self, **_data)
                        object_exists = [obj for obj in self.__dict__[_table] if all([getattr(
                            obj, key) == object.__dict__[key] for key in object.__primary_key__])]
                        if len(object_exists) == 0:
                            self.__dict__[_table].append(object)

                    if field.__class__.__name__ == "ObjectManyList":
                        object = field.type(context=self, **_data)
                        object_exists = [obj for obj in self.__dict__[_table] if all([getattr(
                            obj, key) == object.__dict__[key] for key in object.__primary_key__])]
                        if len(object_exists) == 0:
                            self.__dict__[_table].append(object)

    def __append_commit__(self, field):
        # APPEND TO COMMIT
        if field.type and field.value:
            object_exists = [
                obj for obj in self.__commit__ if obj == field.value]
            if len(object_exists) == 0:
                self.__commit__.append(field.value)
            else:
                object_exists[0] = field.value
            # SET FOREIGN KEY
            #if field.__class__.__name__ is "Object" and self.__dict__[field.reference] != field.value.__dict__[field.key]:
            #    self.__setattr__(field.reference, field.value.__dict__[field.key])

    def __setattr__(self, item, value):
        try:
            if not item.startswith("__"):
                if hasattr(self, "__%s" % item):
                    self.__status__ = EntityStatus.modified
                    field = self.__getattribute__("__%s" % item)
                    if field.type and (field.__class__.__name__ is "ObjectList" or field.__class__.__name__ is "ObjectManyList") and isinstance(value, list):
                        for item_list in value:

                            if isinstance(item_list, dict):
                                self.__dict__[item].append(
                                    field.type(context=self, **item_list))

                            if isinstance(item_list, field.type):
                                item_list.__context__ = self
                                self.__dict__[item].append(item_list)
                    else:
                        if field.type and isinstance(value, dict):
                            field.value = field.type(context=self, **value)
                        elif field.type and value.__class__.__name__ is "Object":
                            value.__context__ = self
                            field.value = value
                        else:
                            field.value = value

                        self.__append_commit__(field)

                        self.__dict__[item] = field.value

                    if self.__context__:
                        object_exists = [
                            obj for obj in self.__context__.__commit__ if obj == self]

                        if len(object_exists) == 0:
                            self.__context__.__commit__.append(self)
                        else:
                            object_exists[0] = self
                else:
                    raise Exception("%s field does not exist" % item)
            else:
                super().__setattr__(item, value)
        except Exception as e:
            raise e

    def __eq__(self, other):
        if self.__class__.__name__ != other.__class__.__name__:
            return False
        return all([getattr(other, pk) == self.__dict__[pk] for pk in self.__primary_key__])

    def toJSON(self):
        try:
            return {k: v if not hasattr(v, "toJSON") else v.toJSON() for k, v in self.__dict__.items() if not k.startswith("__") and v is not None and (v.__class__.__name__ != "ListType" or len(v)>0)}
        except Exception as e:
            raise e

    def toDB(self):
        try:
            return {k: v for k, v in self.__dict__.items() if not k.startswith("__") and v is not None and not hasattr(v, "toJSON")}
        except Exception as e:
            raise e
