# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals, print_function

import datetime
import hashlib
import json
import time

from six import iteritems, string_types
from werkzeug.exceptions import NotFound, Forbidden

import frappe
from frappe import _, msgprint
from frappe.model import default_fields, display_fieldtypes
from frappe.model import optional_fields, table_fields
from frappe.model.base_document import BaseDocument, get_controller
from frappe.model.naming import set_new_name
from frappe.utils import cint, flt, cstr, now, get_datetime_str, file_lock, date_diff,getdate,get_datetime,to_timedelta
from frappe.utils.background_jobs import enqueue

max_positive_value = {
    'smallint': 2 ** 15,
    'int': 2 ** 31,
    'bigint': 2 ** 63
}


# once_only validation
# methods

def get_doc(*args, **kwargs):
    """returns a frappe.model.Document object.

    :param arg1: Document dict or DocType name.
    :param arg2: [optional] document name.

    There are multiple ways to call `get_doc`

        # will fetch the latest user object (with child table) from the database
        user = get_doc("User", "test@example.com")

        # create a new object
        user = get_doc({
            "doctype":"User"
            "email_id": "test@example.com",
            "roles: [
                {"role": "System Manager"}
            ]
        })

        # create new object with keyword arguments
        user = get_doc(doctype='User', email_id='test@example.com')
    """
    if args:
        if isinstance(args[0], BaseDocument):
            # already a document
            return args[0]
        elif isinstance(args[0], string_types):
            doctype = args[0]

        elif isinstance(args[0], dict):
            # passed a dict
            kwargs = args[0]

        else:
            raise ValueError('First non keyword argument must be a string or dict')

    if kwargs:
        if 'doctype' in kwargs:
            doctype = kwargs['doctype']
        else:
            raise ValueError('"doctype" is a required key')

    controller = get_controller(doctype)
    if controller:
        return controller(*args, **kwargs)

    raise ImportError(doctype)


class Document(BaseDocument):
    """All controllers inherit from `Document`."""

    def __init__(self, *args, **kwargs):
        """Constructor.

        :param arg1: DocType name as string or document **dict**
        :param arg2: Document name, if `arg1` is DocType name.

        If DocType name and document name are passed, the object will load
        all values (including child documents) from the database.
        """
        self.doctype = self.name = None
        self._default_new_docs = {}
        self.flags = frappe._dict()

        if args and args[0] and isinstance(args[0], string_types):
            # first arugment is doctype
            if len(args) == 1:
                # single
                self.doctype = self.name = args[0]
            else:
                self.doctype = args[0]
                if isinstance(args[1], dict):
                    # filter
                    self.name = frappe.db.get_value(args[0], args[1], "name")
                    if self.name is None:
                        frappe.throw(_("{0} {1} not found").format(_(args[0]), args[1]),
                                     frappe.DoesNotExistError)
                else:
                    self.name = args[1]

            self.load_from_db()
            return

        if args and args[0] and isinstance(args[0], dict):
            # first argument is a dict
            kwargs = args[0]

        if kwargs:
            # init base document
            super(Document, self).__init__(kwargs)
            self.init_valid_columns()

        else:
            # incorrect arguments. let's not proceed.
            raise ValueError('Illegal arguments')

    @staticmethod
    def whitelist(f):
        """Decorator: Whitelist method to be called remotely via REST API."""
        f.whitelisted = True
        return f

    def reload(self):
        """Reload document from database"""
        self.load_from_db()

    def load_from_db(self):
        """Load document and children from database and create properties
        from fields"""
        if not getattr(self, "_metaclass", False) and self.meta.issingle:
            single_doc = frappe.db.get_singles_dict(self.doctype)
            if not single_doc:
                single_doc = frappe.new_doc(self.doctype).as_dict()
                single_doc["name"] = self.doctype
                del single_doc["__islocal"]

            super(Document, self).__init__(single_doc)
            self.init_valid_columns()
            self._fix_numeric_types()

        else:
            d = frappe.db.get_value(self.doctype, self.name, "*", as_dict=1)
            if not d:
                frappe.throw(_("{0} {1} not found").format(_(self.doctype), self.name), frappe.DoesNotExistError)

            super(Document, self).__init__(d)

        if self.name == "DocType" and self.doctype == "DocType":
            from frappe.model.meta import doctype_table_fields
            table_fields = doctype_table_fields
        else:
            table_fields = self.meta.get_table_fields()

        for df in table_fields:
            children = frappe.db.get_values(df.options,
                                            {"parent": self.name, "parenttype": self.doctype,
                                             "parentfield": df.fieldname},
                                            "*", as_dict=True, order_by="idx asc")
            if children:
                self.set(df.fieldname, children)
            else:
                self.set(df.fieldname, [])

        # sometimes __setup__ can depend on child values, hence calling again at the end
        if hasattr(self, "__setup__"):
            self.__setup__()

    def get_latest(self):
        if not getattr(self, "latest", None):
            self.latest = frappe.get_doc(self.doctype, self.name)
        return self.latest

    def check_permission(self, permtype='read', permlevel=None):
        """Raise `frappe.PermissionError` if not permitted"""
        if not self.has_permission(permtype):
            self.raise_no_permission_to(permlevel or permtype)

    def has_permission(self, permtype="read", verbose=False):
        """Call `frappe.has_permission` if `self.flags.ignore_permissions`
        is not set.

        :param permtype: one of `read`, `write`, `submit`, `cancel`, `delete`"""
        if self.flags.ignore_permissions:
            return True
        return frappe.has_permission(self.doctype, permtype, self, verbose=verbose)

    def raise_no_permission_to(self, perm_type):
        """Raise `frappe.PermissionError`."""
        frappe.flags.error_message = _('Insufficient Permission for {0}').format(self.doctype)
        raise frappe.PermissionError

    def insert(self, ignore_permissions=None, ignore_links=None, ignore_if_duplicate=False, ignore_mandatory=None):
        """Insert the document in the database (as a new document).
        This will check for user permissions and execute `before_insert`,
        `validate`, `on_update`, `after_insert` methods if they are written.

        :param ignore_permissions: Do not check permissions if True."""
        if self.flags.in_print:
            return

        self.flags.notifications_executed = []

        if ignore_permissions != None:
            self.flags.ignore_permissions = ignore_permissions

        if ignore_links != None:
            self.flags.ignore_links = ignore_links

        if ignore_mandatory != None:
            self.flags.ignore_mandatory = ignore_mandatory

        self.set("__islocal", True)

        self.check_permission("create")
        self._set_defaults()
        self.set_user_and_timestamp()
        self.set_docstatus()
        self.check_if_latest()
        self.run_method("before_insert")
        self._validate_links()
        self.set_new_name()
        self.set_parent_in_children()
        self.validate_higher_perm_levels()

        self.flags.in_insert = True
        self.run_before_save_methods()
        self._validate()
        self.set_docstatus()
        self.flags.in_insert = False

        # follow document on document creation

        # run validate, on update etc.

        # parent
        if getattr(self.meta, "issingle", 0):
            self.update_single(self.get_valid_dict())
        else:
            try:
                self.db_insert()
            except frappe.DuplicateEntryError as e:
                if not ignore_if_duplicate:
                    raise e

        # children
        for d in self.get_all_children():
            d.db_insert()

        self.run_method("after_insert")
        self.flags.in_insert = True

        if self.get("amended_from"):
            self.copy_attachments_from_amended_from()

        self.run_post_save_methods()
        self.flags.in_insert = False

        # delete __islocal
        if hasattr(self, "__islocal"):
            delattr(self, "__islocal")

        # if not (frappe.flags.in_migrate or frappe.local.flags.in_install):
        #     follow_document(self.doctype, self.name, frappe.session.user)
        return self

    def save(self, *args, **kwargs):
        """Wrapper for _save"""
        return self._save(*args, **kwargs)

    def _save(self, ignore_permissions=None, ignore_version=None):
        """Save the current document in the database in the **DocType**'s table or
        `tabSingles` (for single types).

        This will check for user permissions and execute
        `validate` before updating, `on_update` after updating triggers.

        :param ignore_permissions: Do not check permissions if True.
        :param ignore_version: Do not save version if True."""
        if self.flags.in_print:
            return

        self.flags.notifications_executed = []

        if ignore_permissions != None:
            self.flags.ignore_permissions = ignore_permissions

        if ignore_version != None:
            self.flags.ignore_version = ignore_version

        if self.get("__islocal") or not self.get("name"):
            self.insert()
            return

        self.check_permission("write", "save")

        self.set_user_and_timestamp()
        self.set_docstatus()
        self.check_if_latest()
        self.set_parent_in_children()
        self.set_name_in_children()

        self.validate_higher_perm_levels()
        self._validate_links()
        self.run_before_save_methods()

        if self._action != "cancel":
            self._validate()

        if self._action == "update_after_submit":
            self.validate_update_after_submit()

        self.set_docstatus()

        # parent
        if self.meta.issingle:
            self.update_single(self.get_valid_dict())
        else:
            self.db_update()

        self.update_children()
        self.run_post_save_methods()

        return self

    def copy_attachments_from_amended_from(self):
        '''Copy attachments from `amended_from`'''
        pass

    def update_children(self):
        '''update child tables'''
        for df in self.meta.get_table_fields():
            self.update_child_table(df.fieldname, df)

    def update_child_table(self, fieldname, df=None):
        '''sync child table for given fieldname'''
        rows = []
        if not df:
            df = self.meta.get_field(fieldname)

        for d in self.get(df.fieldname):
            d.db_update()
            rows.append(d.name)

        if df.options in (self.flags.ignore_children_type or []):
            # do not delete rows for this because of flags
            # hack for docperm :(
            return

        if rows:
            # select rows that do not match the ones in the document
            deleted_rows = frappe.db.sql("""select name from `tab{0}` where parent=%s
				and parenttype=%s and parentfield=%s
				and name not in ({1})""".format(df.options, ','.join(['%s'] * len(rows))),
                                         [self.name, self.doctype, fieldname] + rows)
            if len(deleted_rows) > 0:
                # delete rows that do not match the ones in the document
                frappe.db.sql("""delete from `tab{0}` where name in ({1})""".format(df.options,
                                                                                    ','.join(
                                                                                        ['%s'] * len(deleted_rows))),
                              tuple(row[0] for row in deleted_rows))

        else:
            # no rows found, delete all rows
            frappe.db.sql("""delete from `tab{0}` where parent=%s
				and parenttype=%s and parentfield=%s""".format(df.options),
                          (self.name, self.doctype, fieldname))

    def get_doc_before_save(self):
        return getattr(self, '_doc_before_save', None)

    def set_new_name(self, force=False):
        """Calls `frappe.naming.se_new_name` for parent and child docs."""
        if self.flags.name_set and not force:
            return

        set_new_name(self)
        # set name for children
        for d in self.get_all_children():
            set_new_name(d)

        self.flags.name_set = True

    def get_title(self):
        '''Get the document title based on title_field or `title` or `name`'''
        return self.get(self.meta.get_title_field())

    def set_title_field(self):
        """Set title field based on template"""

        def get_values():
            values = self.as_dict()
            # format values
            for key, value in iteritems(values):
                if value == None:
                    values[key] = ""
            return values

        if self.meta.get("title_field") == "title":
            df = self.meta.get_field(self.meta.title_field)

            if df.options:
                self.set(df.fieldname, df.options.format(**get_values()))
            elif self.is_new() and not self.get(df.fieldname) and df.default:
                # set default title for new transactions (if default)
                self.set(df.fieldname, df.default.format(**get_values()))

    def update_single(self, d):
        """Updates values for Single type Document in `tabSingles`."""
        frappe.db.sql("""delete from `tabSingles` where doctype=%s""", self.doctype)
        for field, value in iteritems(d):
            if field != "doctype":
                frappe.db.sql("""insert into `tabSingles` (doctype, field, value)
					values (%s, %s, %s)""", (self.doctype, field, value))

        if self.doctype in frappe.db.value_cache:
            del frappe.db.value_cache[self.doctype]

    def set_user_and_timestamp(self):
        self._original_modified = self.modified
        self.modified = now()
        self.modified_by = frappe.session.user
        if not self.creation:
            self.creation = self.modified
        if not self.owner:
            self.owner = self.modified_by

        for d in self.get_all_children():
            d.modified = self.modified
            d.modified_by = self.modified_by
            if not d.owner:
                d.owner = self.owner
            if not d.creation:
                d.creation = self.creation

        frappe.flags.currently_saving.append((self.doctype, self.name))

    def set_docstatus(self):
        if self.docstatus == None:
            self.docstatus = 0

        for d in self.get_all_children():
            d.docstatus = self.docstatus

    def _validate(self):
        self._validate_mandatory()
        self._validate_selects()
        self._validate_length()
        self._extract_images_from_text_editor()
        self._sanitize_content()
        self._save_passwords()
        self.validate_workflow()

        children = self.get_all_children()
        for d in children:
            d._validate_selects()
            d._validate_length()
            d._extract_images_from_text_editor()
            d._sanitize_content()
            d._save_passwords()
        if self.is_new():
            # don't set fields like _assign, _comments for new doc
            for fieldname in optional_fields:
                self.set(fieldname, None)
        else:
            self.validate_set_only_once()

    def validate_workflow(self):
        '''Validate if the workflow transition is valid'''
        if frappe.flags.in_install == 'frappe': return

    def validate_set_only_once(self):
        '''Validate that fields are not changed if not in insert'''
        set_only_once_fields = self.meta.get_set_only_once_fields()

        if set_only_once_fields and self._doc_before_save:
            # document exists before saving
            for field in set_only_once_fields:
                fail = False
                value = self.get(field.fieldname)
                original_value = self._doc_before_save.get(field.fieldname)

                if field.fieldtype in table_fields:
                    fail = not self.is_child_table_same(field.fieldname)
                elif field.fieldtype in ('Date', 'Datetime', 'Time'):
                    fail = str(value) != str(original_value)
                else:
                    fail = value != original_value

                if fail:
                    frappe.throw(_("Value cannot be changed for {0}").format(self.meta.get_label(field.fieldname)),
                                 frappe.CannotChangeConstantError)

        return False

    def is_child_table_same(self, fieldname):
        '''Validate child table is same as original table before saving'''
        value = self.get(fieldname)
        original_value = self._doc_before_save.get(fieldname)
        same = True

        if len(original_value) != len(value):
            same = False
        else:
            # check all child entries
            for i, d in enumerate(original_value):
                new_child = value[i].as_dict(convert_dates_to_str=True)
                original_child = d.as_dict(convert_dates_to_str=True)

                # all fields must be same other than modified and modified_by
                for key in ('modified', 'modified_by', 'creation'):
                    del new_child[key]
                    del original_child[key]

                if original_child != new_child:
                    same = False
                    break

        return same

    def apply_fieldlevel_read_permissions(self):
        '''Remove values the user is not allowed to read (called when loading in desk)'''
        has_higher_permlevel = False
        for p in self.get_permissions():
            if p.permlevel > 0:
                has_higher_permlevel = True
                break

        if not has_higher_permlevel:
            return

        has_access_to = self.get_permlevel_access('read')

        for df in self.meta.fields:
            if df.permlevel and not df.permlevel in has_access_to:
                self.set(df.fieldname, None)

        for table_field in self.meta.get_table_fields():
            for df in frappe.get_meta(table_field.options).fields or []:
                if df.permlevel and not df.permlevel in has_access_to:
                    for child in self.get(table_field.fieldname) or []:
                        child.set(df.fieldname, None)

    def validate_higher_perm_levels(self):
        """If the user does not have permissions at permlevel > 0, then reset the values to original / default"""
        if self.flags.ignore_permissions or frappe.flags.in_install:
            return

        has_access_to = self.get_permlevel_access()
        high_permlevel_fields = self.meta.get_high_permlevel_fields()

        if high_permlevel_fields:
            self.reset_values_if_no_permlevel_access(has_access_to, high_permlevel_fields)

        # check for child tables
        for df in self.meta.get_table_fields():
            high_permlevel_fields = frappe.get_meta(df.options).meta.get_high_permlevel_fields()
            if high_permlevel_fields:
                for d in self.get(df.fieldname):
                    d.reset_values_if_no_permlevel_access(has_access_to, high_permlevel_fields)

    def get_permlevel_access(self, permission_type='write'):
        if not hasattr(self, "_has_access_to"):
            roles = frappe.get_roles()
            self._has_access_to = []
            for perm in self.get_permissions():
                if perm.role in roles and perm.permlevel > 0 and perm.get(permission_type):
                    if perm.permlevel not in self._has_access_to:
                        self._has_access_to.append(perm.permlevel)

        return self._has_access_to

    def has_permlevel_access_to(self, fieldname, df=None, permission_type='read'):
        if not df:
            df = self.meta.get_field(fieldname)

        return df.permlevel in self.get_permlevel_access(permission_type)

    def get_permissions(self):
        if self.meta.istable:
            # use parent permissions
            permissions = frappe.get_meta(self.parenttype).permissions
        else:
            permissions = self.meta.permissions

        return permissions

    def _set_defaults(self):
        if frappe.flags.in_import:
            return

        new_doc = frappe.new_doc(self.doctype, as_dict=True)
        self.update_if_missing(new_doc)

        # children
        for df in self.meta.get_table_fields():
            new_doc = frappe.new_doc(df.options, as_dict=True)
            value = self.get(df.fieldname)
            if isinstance(value, list):
                for d in value:
                    d.update_if_missing(new_doc)

    def check_if_latest(self):
        """Checks if `modified` timestamp provided by document being updated is same as the
        `modified` timestamp in the database. If there is a different, the document has been
        updated in the database after the current copy was read. Will throw an error if
        timestamps don't match.

        Will also validate document transitions (Save > Submit > Cancel) calling
        `self.check_docstatus_transition`."""
        conflict = False
        self._action = "save"
        if not self.get('__islocal'):
            if self.meta.issingle:
                modified = frappe.db.sql('''select value from tabSingles
					where doctype=%s and field='modified' for update''', self.doctype)
                modified = modified and modified[0][0]
                if modified and modified != cstr(self._original_modified):
                    conflict = True
            else:
                tmp = frappe.db.sql("""select modified, docstatus from `tab{0}`
					where name = %s for update""".format(self.doctype), self.name, as_dict=True)

                if not tmp:
                    frappe.throw(_("Record does not exist"))
                else:
                    tmp = tmp[0]

                modified = cstr(tmp.modified)

                if modified and modified != cstr(self._original_modified):
                    conflict = True

                self.check_docstatus_transition(tmp.docstatus)

            if conflict:
                frappe.msgprint(_("Error: Document has been modified after you have opened it") \
                                + (" (%s, %s). " % (modified, self.modified)) \
                                + _("Please refresh to get the latest document."),
                                raise_exception=frappe.TimestampMismatchError)
        else:
            self.check_docstatus_transition(0)

    def check_docstatus_transition(self, docstatus):
        """Ensures valid `docstatus` transition.
        Valid transitions are (number in brackets is `docstatus`):

        - Save (0) > Save (0)
        - Save (0) > Submit (1)
        - Submit (1) > Submit (1)
        - Submit (1) > Cancel (2)

        """
        if not self.docstatus:
            self.docstatus = 0
        if docstatus == 0:
            if self.docstatus == 0:
                self._action = "save"
            elif self.docstatus == 1:
                self._action = "submit"
                self.check_permission("submit")
            else:
                raise frappe.DocstatusTransitionError(_("Cannot change docstatus from 0 to 2"))

        elif docstatus == 1:
            if self.docstatus == 1:
                self._action = "update_after_submit"
                self.check_permission("submit")
            elif self.docstatus == 2:
                self._action = "cancel"
                self.check_permission("cancel")
            else:
                raise frappe.DocstatusTransitionError(_("Cannot change docstatus from 1 to 0"))

        elif docstatus == 2:
            raise frappe.ValidationError(_("Cannot edit cancelled document"))

    def set_parent_in_children(self):
        """Updates `parent` and `parenttype` property in all children."""
        for d in self.get_all_children():
            d.parent = self.name
            d.parenttype = self.doctype

    def set_name_in_children(self):
        # Set name for any new children
        for d in self.get_all_children():
            if not d.name:
                set_new_name(d)

    def validate_update_after_submit(self):
        if self.flags.ignore_validate_update_after_submit:
            return

        self._validate_update_after_submit()
        for d in self.get_all_children():
            if d.is_new() and self.meta.get_field(d.parentfield).allow_on_submit:
                # in case of a new row, don't validate allow on submit, if table is allow on submit
                continue

            d._validate_update_after_submit()

    # TODO check only allowed values are updated

    def _validate_mandatory(self):
        if self.flags.ignore_mandatory:
            return

        missing = self._get_missing_mandatory_fields()
        for d in self.get_all_children():
            missing.extend(d._get_missing_mandatory_fields())

        if not missing:
            return

        for fieldname, msg in missing:
            msgprint(msg)

        if frappe.flags.print_messages:
            print(self.as_json().encode("utf-8"))

        raise frappe.MandatoryError('[{doctype}, {name}]: {fields}'.format(
            fields=", ".join((each[0] for each in missing)),
            doctype=self.doctype,
            name=self.name))

    def _validate_links(self):
        if self.flags.ignore_links or self._action == "cancel":
            return

        invalid_links, cancelled_links = self.get_invalid_links()

        for d in self.get_all_children():
            result = d.get_invalid_links(is_submittable=self.meta.is_submittable)
            invalid_links.extend(result[0])
            cancelled_links.extend(result[1])

        if invalid_links:
            msg = ", ".join((each[2] for each in invalid_links))
            frappe.throw(_("Could not find {0}").format(msg),
                         frappe.LinkValidationError)

        if cancelled_links:
            msg = ", ".join((each[2] for each in cancelled_links))
            frappe.throw(_("Cannot link cancelled document: {0}").format(msg),
                         frappe.CancelledLinkError)

    def get_all_children(self, parenttype=None):
        """Returns all children documents from **Table** type field in a list."""
        ret = []
        for df in self.meta.get("fields", {"fieldtype": ['in', table_fields]}):
            if parenttype:
                if df.options == parenttype:
                    return self.get(df.fieldname)
            value = self.get(df.fieldname)
            if isinstance(value, list):
                ret.extend(value)
        return ret

    def run_method(self, method, *args, **kwargs):
        """run standard triggers, plus those in hooks"""
        if "flags" in kwargs:
            del kwargs["flags"]

        if hasattr(self, method) and hasattr(getattr(self, method), "__call__"):
            fn = lambda self, *args, **kwargs: getattr(self, method)(*args, **kwargs)
        else:
            # hack! to run hooks even if method does not exist
            fn = lambda self, *args, **kwargs: None

        fn.__name__ = str(method)
        out = Document.hook(fn)(self, *args, **kwargs)

        return out

    def run_trigger(self, method, *args, **kwargs):
        return self.run_method(method, *args, **kwargs)

    def _submit(self):
        """Submit the document. Sets `docstatus` = 1, then saves."""
        self.docstatus = 1
        self.save()

    def _cancel(self):
        """Cancel the document. Sets `docstatus` = 2, then saves."""
        self.docstatus = 2
        self.save()

    def submit(self):
        """Submit the document. Sets `docstatus` = 1, then saves."""
        self._submit()

    def cancel(self):
        """Cancel the document. Sets `docstatus` = 2, then saves."""
        self._cancel()

    def delete(self):
        """Delete document."""
        frappe.delete_doc(self.doctype, self.name, flags=self.flags)

    def run_before_save_methods(self):
        """Run standard methods before  `INSERT` or `UPDATE`. Standard Methods are:

        - `validate`, `before_save` for **Save**.
        - `validate`, `before_submit` for **Submit**.
        - `before_cancel` for **Cancel**
        - `before_update_after_submit` for **Update after Submit**

        Will also update title_field if set"""

        self.load_doc_before_save()
        self.reset_seen()

        if self.flags.ignore_validate:
            return

        if self._action == "save":
            self.run_method("before_validate")
            self.run_method("validate")
            self.run_method("before_save")
        elif self._action == "submit":
            self.run_method("before_validate")
            self.run_method("validate")
            self.run_method("before_submit")
        elif self._action == "cancel":
            self.run_method("before_cancel")
        elif self._action == "update_after_submit":
            self.run_method("before_update_after_submit")

        self.set_title_field()

    def load_doc_before_save(self):
        '''Save load document from db before saving'''
        self._doc_before_save = None
        if not self.is_new():
            try:
                self._doc_before_save = frappe.get_doc(self.doctype, self.name)
            except frappe.DoesNotExistError:
                self._doc_before_save = None
                frappe.clear_last_message()

    def run_post_save_methods(self):
        pass

    def clear_cache(self):
        pass

    def reset_seen(self):
        pass

    def notify_update(self):
        pass

    def db_set(self, fieldname, value=None, update_modified=True, notify=False, commit=False):
        '''Set a value in the document object, update the timestamp and update the database.

        WARNING: This method does not trigger controller validations and should
        be used very carefully.

        :param fieldname: fieldname of the property to be updated, or a {"field":"value"} dictionary
        :param value: value of the property to be updated
        :param update_modified: default True. updates the `modified` and `modified_by` properties
        :param notify: default False. run doc.notify_updated() to send updates via socketio
        :param commit: default False. run frappe.db.commit()
        '''
        if isinstance(fieldname, dict):
            self.update(fieldname)
        else:
            self.set(fieldname, value)

        if update_modified and (self.doctype, self.name) not in frappe.flags.currently_saving:
            # don't update modified timestamp if called from post save methods
            # like on_update or on_submit
            self.set("modified", now())
            self.set("modified_by", frappe.session.user)

        self.load_doc_before_save()
        # to trigger notification on value change
        self.run_method('before_change')

        frappe.db.set_value(self.doctype, self.name, fieldname, value,
                            self.modified, self.modified_by, update_modified=update_modified)

        self.run_method('on_change')

        if notify:
            self.notify_update()

        self.clear_cache()
        if commit:
            frappe.db.commit()

    def db_get(self, fieldname):
        '''get database value for this fieldname'''
        return frappe.db.get_value(self.doctype, self.name, fieldname)

    def check_no_back_links_exist(self):
        """Check if document links to any active document before Cancel."""
        from frappe.model.delete_doc import check_if_doc_is_linked, check_if_doc_is_dynamically_linked
        if not self.flags.ignore_links:
            check_if_doc_is_linked(self, method="Cancel")
            check_if_doc_is_dynamically_linked(self, method="Cancel")

    def save_version(self):
        '''Save version info'''
        version = frappe.new_doc('Version')
        if version.set_diff(self._doc_before_save, self):
            version.insert(ignore_permissions=True)

    @staticmethod
    def hook(f):
        """Decorator: Make method `hookable` (i.e. extensible by another app).

        Note: If each hooked method returns a value (dict), then all returns are
        collated in one dict and returned. Ideally, don't return values in hookable
        methods, set properties in the document."""

        def add_to_return_value(self, new_return_value):
            if isinstance(new_return_value, dict):
                if not self.get("_return_value"):
                    self._return_value = {}
                self._return_value.update(new_return_value)
            else:
                self._return_value = new_return_value or self.get("_return_value")

        def compose(fn, *hooks):
            pass

        def composer(self, *args, **kwargs):
            pass

        return composer

    def is_whitelisted(self, method):
        fn = getattr(self, method, None)
        if not fn:
            raise NotFound("Method {0} not found".format(method))
        elif not getattr(fn, "whitelisted", False):
            raise Forbidden("Method {0} not whitelisted".format(method))

    def validate_value(self, fieldname, condition, val2, doc=None, raise_exception=None):
        """Check that value of fieldname should be 'condition' val2
            else throw Exception."""
        error_condition_map = {
            "in": _("one of"),
            "not in": _("none of"),
            "^": _("beginning with"),
        }

        if not doc:
            doc = self

        val1 = doc.get_value(fieldname)

        df = doc.meta.get_field(fieldname)
        val2 = doc.cast(val2, df)

        if not frappe.compare(val1, condition, val2):
            label = doc.meta.get_label(fieldname)
            condition_str = error_condition_map.get(condition, condition)
            if doc.parentfield:
                msg = _("Incorrect value in row {0}: {1} must be {2} {3}".format(doc.idx, label, condition_str, val2))
            else:
                msg = _("Incorrect value: {0} must be {1} {2}".format(label, condition_str, val2))

            # raise passed exception or True
            msgprint(msg, raise_exception=raise_exception or True)

    def validate_table_has_rows(self, parentfield, raise_exception=None):
        """Raise exception if Table field is empty."""
        if not (isinstance(self.get(parentfield), list) and len(self.get(parentfield)) > 0):
            label = self.meta.get_label(parentfield)
            frappe.throw(_("Table {0} cannot be empty").format(label), raise_exception or frappe.EmptyTableError)

    def round_floats_in(self, doc, fieldnames=None):
        """Round floats for all `Currency`, `Float`, `Percent` fields for the given doc.

        :param doc: Document whose numeric properties are to be rounded.
        :param fieldnames: [Optional] List of fields to be rounded."""
        if not fieldnames:
            fieldnames = (df.fieldname for df in
                          doc.meta.get("fields", {"fieldtype": ["in", ["Currency", "Float", "Percent"]]}))

        for fieldname in fieldnames:
            doc.set(fieldname, flt(doc.get(fieldname), self.precision(fieldname, doc.parentfield)))

    def get_url(self):
        """Returns Desk URL for this document. `/desk#Form/{doctype}/{name}`"""
        return "/desk#Form/{doctype}/{name}".format(doctype=self.doctype, name=self.name)

    def add_comment(self, comment_type='Comment', text=None, comment_email=None, link_doctype=None, link_name=None,
                    comment_by=None):
        """Add a comment to this document.

        :param comment_type: e.g. `Comment`. See Communication for more info."""

        out = frappe.get_doc({
            "doctype": "Comment",
            'comment_type': comment_type,
            "comment_email": comment_email or frappe.session.user,
            "comment_by": comment_by,
            "reference_doctype": self.doctype,
            "reference_name": self.name,
            "content": text or comment_type,
            "link_doctype": link_doctype,
            "link_name": link_name
        }).insert(ignore_permissions=True)
        return out

    def add_seen(self, user=None):
        '''add the given/current user to list of users who have seen this document (_seen)'''
        if not user:
            user = frappe.session.user

        if self.meta.track_seen:
            _seen = self.get('_seen') or []
            _seen = frappe.parse_json(_seen)

            if user not in _seen:
                _seen.append(user)
                frappe.db.set_value(self.doctype, self.name, '_seen', json.dumps(_seen), update_modified=False)
                frappe.local.flags.commit = True

    def add_viewed(self, user=None):
        '''add log to communication when a user views a document'''
        if not user:
            user = frappe.session.user

        if hasattr(self.meta, 'track_views') and self.meta.track_views:
            frappe.get_doc({
                "doctype": "View Log",
                "viewed_by": frappe.session.user,
                "reference_doctype": self.doctype,
                "reference_name": self.name,
            }).insert(ignore_permissions=True)
            frappe.local.flags.commit = True

    def get_signature(self):
        """Returns signature (hash) for private URL."""
        return hashlib.sha224(get_datetime_str(self.creation).encode()).hexdigest()

    def get_liked_by(self):
        liked_by = getattr(self, "_liked_by", None)
        if liked_by:
            return json.loads(liked_by)
        else:
            return []

    def set_onload(self, key, value):
        if not self.get("__onload"):
            self.set("__onload", frappe._dict())
        self.get("__onload")[key] = value

    def get_onload(self, key=None):
        if not key:
            return self.get("__onload", frappe._dict())

        return self.get('__onload')[key]

    def queue_action(self, action, **kwargs):
        '''Run an action in background. If the action has an inner function,
        like _submit for submit, it will call that instead'''
        # call _submit instead of submit, so you can override submit to call
        # run_delayed based on some action
        # See: Stock Reconciliation
        if hasattr(self, '_' + action):
            action = '_' + action

        if file_lock.lock_exists(self.get_signature()):
            frappe.throw(_('This document is currently queued for execution. Please try again'),
                         title=_('Document Queued'))

        self.lock()
        enqueue('frappe.model.document.execute_action', doctype=self.doctype, name=self.name,
                action=action, **kwargs)

    def lock(self, timeout=None):
        '''Creates a lock file for the given document. If timeout is set,
        it will retry every 1 second for acquiring the lock again

        :param timeout: Timeout in seconds, default 0'''
        signature = self.get_signature()
        if file_lock.lock_exists(signature):
            lock_exists = True
            if timeout:
                for i in range(timeout):
                    time.sleep(1)
                    if not file_lock.lock_exists(signature):
                        lock_exists = False
                        break
            if lock_exists:
                raise frappe.DocumentLockedError
        file_lock.create_lock(signature)

    def unlock(self):
        '''Delete the lock file for this document'''
        file_lock.delete_lock(self.get_signature())

    # validation helpers
    def validate_from_to_dates(self, from_date_field, to_date_field):
        '''
        Generic validation to verify date sequence
        '''
        if date_diff(self.get(to_date_field), self.get(from_date_field)) < 0:
            frappe.throw(_('{0} must be after {1}').format(
                frappe.bold(self.meta.get_label(to_date_field)),
                frappe.bold(self.meta.get_label(from_date_field)),
            ), frappe.InvalidDates)


def execute_action(doctype, name, action, **kwargs):
    '''Execute an action on a document (called by background worker)'''
    doc = frappe.get_doc(doctype, name)
    doc.unlock()
    try:
        getattr(doc, action)(**kwargs)
    except Exception:
        frappe.db.rollback()

        # add a comment (?)
        if frappe.local.message_log:
            msg = json.loads(frappe.local.message_log[-1]).get('message')
        else:
            msg = '<pre><code>' + frappe.get_traceback() + '</pre></code>'

        doc.add_comment('Comment', _('Action Failed') + '<br><br>' + msg)
        doc.notify_update()


class BaseDocument(object):
    ignore_in_getter = ("doctype", "_meta", "meta", "_table_fields", "_valid_columns")

    def __init__(self, d):
        self.update(d)
        self.dont_update_if_missing = []

        if hasattr(self, "__setup__"):
            self.__setup__()

    @property
    def meta(self):
        if not hasattr(self, "_meta"):
            self._meta = frappe.get_meta(self.doctype)

        return self._meta

    def update(self, d):
        if "doctype" in d:
            self.set("doctype", d.get("doctype"))

        # first set default field values of base document
        from frappe.model import default_fields
        for key in default_fields:
            if key in d:
                self.set(key, d.get(key))

        for key, value in iteritems(d):
            self.set(key, value)

        return self

    def update_if_missing(self, d):
        if isinstance(d, BaseDocument):
            d = d.get_valid_dict()

        if "doctype" in d:
            self.set("doctype", d.get("doctype"))
        for key, value in iteritems(d):
            # dont_update_if_missing is a list of fieldnames, for which, you don't want to set default value
            if (self.get(key) is None) and (value is not None) and (key not in self.dont_update_if_missing):
                self.set(key, value)

    def get_db_value(self, key):
        return frappe.db.get_value(self.doctype, self.name, key)

    def get(self, key=None, filters=None, limit=None, default=None):
        if key:
            if isinstance(key, dict):
                return _filter(self.get_all_children(), key, limit=limit)
            if filters:
                if isinstance(filters, dict):
                    value = _filter(self.__dict__.get(key, []), filters, limit=limit)
                else:
                    default = filters
                    filters = None
                    value = self.__dict__.get(key, default)
            else:
                value = self.__dict__.get(key, default)

            if value is None and key not in self.ignore_in_getter \
                    and key in (d.fieldname for d in self.meta.get_table_fields()):
                self.set(key, [])
                value = self.__dict__.get(key)

            return value
        else:
            return self.__dict__

    def getone(self, key, filters=None):
        return self.get(key, filters=filters, limit=1)[0]

    def set(self, key, value, as_value=False):
        if isinstance(value, list) and not as_value:
            self.__dict__[key] = []
            self.extend(key, value)
        else:
            self.__dict__[key] = value

    def delete_key(self, key):
        if key in self.__dict__:
            del self.__dict__[key]

    def append(self, key, value=None):
        if value == None:
            value = {}
        if isinstance(value, (dict, BaseDocument)):
            if not self.__dict__.get(key):
                self.__dict__[key] = []
            value = self._init_child(value, key)
            self.__dict__[key].append(value)

            # reference parent document
            value.parent_doc = self

            return value
        else:

            # metaclasses may have arbitrary lists
            # which we can ignore
            if (getattr(self, '_metaclass', None)
                    or self.__class__.__name__ in ('Meta', 'FormMeta', 'DocField')):
                return value

            raise ValueError(
                'Document for field "{0}" attached to child table of "{1}" must be a dict or BaseDocument, not {2} ({3})'.format(
                    key,
                    self.name, str(type(value))[1:-1], value)
            )

    def extend(self, key, value):
        if isinstance(value, list):
            for v in value:
                self.append(key, v)
        else:
            raise ValueError

    def remove(self, doc):
        self.get(doc.parentfield).remove(doc)

    def _init_child(self, value, key):
        if not self.doctype:
            return value
        if not isinstance(value, BaseDocument):
            if "doctype" not in value or value['doctype'] is None:
                value["doctype"] = self.get_table_field_doctype(key)
                if not value["doctype"]:
                    raise AttributeError(key)

            value = get_controller(value["doctype"])(value)
            value.init_valid_columns()

        value.parent = self.name
        value.parenttype = self.doctype
        value.parentfield = key

        if value.docstatus is None:
            value.docstatus = 0

        if not getattr(value, "idx", None):
            value.idx = len(self.get(key) or []) + 1

        if not getattr(value, "name", None):
            value.__dict__['__islocal'] = 1

        return value

    def get_valid_dict(self, sanitize=True, convert_dates_to_str=False, ignore_nulls=False):
        d = frappe._dict()
        for fieldname in self.meta.get_valid_columns():
            d[fieldname] = self.get(fieldname)

            # if no need for sanitization and value is None, continue
            if not sanitize and d[fieldname] is None:
                continue

            df = self.meta.get_field(fieldname)
            if df:
                if df.fieldtype == "Check":
                    d[fieldname] = 1 if cint(d[fieldname]) else 0

                elif df.fieldtype == "Int" and not isinstance(d[fieldname], int):
                    d[fieldname] = cint(d[fieldname])

                elif df.fieldtype in ("Currency", "Float", "Percent") and not isinstance(d[fieldname], float):
                    d[fieldname] = flt(d[fieldname])

                elif df.fieldtype in ("Datetime", "Date", "Time") and d[fieldname] == "":
                    d[fieldname] = None

                elif df.get("unique") and cstr(d[fieldname]).strip() == "":
                    # unique empty field should be set to None
                    d[fieldname] = None

                if isinstance(d[fieldname], list) and df.fieldtype not in table_fields:
                    frappe.throw(_('Value for {0} cannot be a list').format(_(df.label)))

                if convert_dates_to_str and isinstance(d[fieldname],
                                                       (datetime.datetime, datetime.time, datetime.timedelta)):
                    d[fieldname] = str(d[fieldname])

            if d[fieldname] == None and ignore_nulls:
                del d[fieldname]

        return d

    def init_valid_columns(self):

        for key in default_fields:
            if key not in self.__dict__:
                self.__dict__[key] = None

            if key in ("idx", "docstatus") and self.__dict__[key] is None:
                self.__dict__[key] = 0

        for key in self.get_valid_columns():
            if key not in self.__dict__:
                self.__dict__[key] = None

    def get_valid_columns(self):
        if self.doctype not in frappe.local.valid_columns:
            if self.doctype in ("DocField", "DocPerm") and self.parent in ("DocType", "DocField", "DocPerm"):
                from frappe.model.meta import get_table_columns
                valid = get_table_columns(self.doctype)
            else:
                valid = self.meta.get_valid_columns()

            frappe.local.valid_columns[self.doctype] = valid

        return frappe.local.valid_columns[self.doctype]

    def is_new(self):
        return self.get("__islocal")

    def as_dict(self, no_nulls=False, no_default_fields=False, convert_dates_to_str=False):
        doc = self.get_valid_dict(convert_dates_to_str=convert_dates_to_str)
        doc["doctype"] = self.doctype
        for df in self.meta.get_table_fields():
            children = self.get(df.fieldname) or []
            doc[df.fieldname] = [d.as_dict(no_nulls=no_nulls) for d in children]

        if no_nulls:
            for k in list(doc):
                if doc[k] is None:
                    del doc[k]

        if no_default_fields:
            for k in list(doc):
                if k in default_fields:
                    del doc[k]

        for key in ("_user_tags", "__islocal", "__onload", "_liked_by", "__run_link_triggers"):
            if self.get(key):
                doc[key] = self.get(key)

        return doc

    def as_json(self):
        return frappe.as_json(self.as_dict())

    def get_table_field_doctype(self, fieldname):
        return self.meta.get_field(fieldname).options

    def get_parentfield_of_doctype(self, doctype):
        fieldname = [df.fieldname for df in self.meta.get_table_fields() if df.options == doctype]
        return fieldname[0] if fieldname else None

    def db_insert(self):
        """INSERT the document (with valid columns) in the database."""
        if not self.name:
            # name will be set by document class in most cases
            set_new_name(self)

        if not self.creation:
            self.creation = self.modified = now()
            self.created_by = self.modified_by = frappe.session.user

        # if doctype is "DocType", don't insert null values as we don't know who is valid yet
        d = self.get_valid_dict(convert_dates_to_str=True,
                                ignore_nulls=self.doctype in ('DocType', 'DocField', 'DocPerm'))

        columns = list(d)
        try:
            frappe.db.sql("""INSERT INTO `tab{doctype}` ({columns})
					VALUES ({values})""".format(
                doctype=self.doctype,
                columns=", ".join(["`" + c + "`" for c in columns]),
                values=", ".join(["%s"] * len(columns))
            ), list(d.values()))
        except Exception as e:
            if frappe.db.is_primary_key_violation(e):
                if self.meta.autoname == "hash":
                    # hash collision? try again
                    self.name = None
                    self.db_insert()
                    return

                frappe.msgprint(_("Duplicate name {0} {1}").format(self.doctype, self.name))
                raise frappe.DuplicateEntryError(self.doctype, self.name, e)

            elif frappe.db.is_unique_key_violation(e):
                # unique constraint
                self.show_unique_validation_message(e)

            else:
                raise

        self.set("__islocal", False)

    def db_update(self):
        if self.get("__islocal") or not self.name:
            self.db_insert()
            return

        d = self.get_valid_dict(convert_dates_to_str=True,
                                ignore_nulls=self.doctype in ('DocType', 'DocField', 'DocPerm'))

        # don't update name, as case might've been changed
        name = d['name']
        del d['name']

        columns = list(d)

        try:
            frappe.db.sql("""UPDATE `tab{doctype}`
				SET {values} WHERE `name`=%s""".format(
                doctype=self.doctype,
                values=", ".join(["`" + c + "`=%s" for c in columns])
            ), list(d.values()) + [name])
        except Exception as e:
            if frappe.db.is_unique_key_violation(e):
                self.show_unique_validation_message(e)
            else:
                raise

    def show_unique_validation_message(self, e):
        # TODO: Find a better way to extract fieldname
        if frappe.db.db_type != 'postgres':
            fieldname = str(e).split("'")[-2]
            label = None

            # unique_first_fieldname_second_fieldname is the constraint name
            # created using frappe.db.add_unique
            if "unique_" in fieldname:
                fieldname = fieldname.split("_", 1)[1]

            df = self.meta.get_field(fieldname)
            if df:
                label = df.label

            frappe.msgprint(_("{0} must be unique".format(label or fieldname)))

        # this is used to preserve traceback
        raise frappe.UniqueValidationError(self.doctype, self.name, e)

    def update_modified(self):
        '''Update modified timestamp'''
        self.set("modified", now())
        frappe.db.set_value(self.doctype, self.name, 'modified', self.modified, update_modified=False)

    def _fix_numeric_types(self):
        for df in self.meta.get("fields"):
            if df.fieldtype == "Check":
                self.set(df.fieldname, cint(self.get(df.fieldname)))

            elif self.get(df.fieldname) is not None:
                if df.fieldtype == "Int":
                    self.set(df.fieldname, cint(self.get(df.fieldname)))

                elif df.fieldtype in ("Float", "Currency", "Percent"):
                    self.set(df.fieldname, flt(self.get(df.fieldname)))

        if self.docstatus is not None:
            self.docstatus = cint(self.docstatus)

    def _get_missing_mandatory_fields(self):
        """Get mandatory fields that do not have any values"""

        def get_msg(df):
            if df.fieldtype in table_fields:
                return "{}: {}: {}".format(_("Error"), _("Data missing in table"), _(df.label))

            elif self.parentfield:
                return "{}: {} {} #{}: {}: {}".format(_("Error"), frappe.bold(_(self.doctype)),
                                                      _("Row"), self.idx, _("Value missing for"), _(df.label))

            else:
                return _("Error: Value missing for {0}: {1}").format(_(df.parent), _(df.label))

        missing = []

        for df in self.meta.get("fields", {"reqd": ('=', 1)}):
            if self.get(df.fieldname) in (None, []):
                missing.append((df.fieldname, get_msg(df)))

        # check for missing parent and parenttype
        if self.meta.istable:
            for fieldname in ("parent", "parenttype"):
                if not self.get(fieldname):
                    missing.append((fieldname, get_msg(frappe._dict(label=fieldname))))

        return missing

    def get_invalid_links(self, is_submittable=False):
        '''Returns list of invalid links and also updates fetch values if not set'''

        def get_msg(df, docname):
            if self.parentfield:
                return "{} #{}: {}: {}".format(_("Row"), self.idx, _(df.label), docname)
            else:
                return "{}: {}".format(_(df.label), docname)

        invalid_links = []
        cancelled_links = []

        for df in (self.meta.get_link_fields()
                   + self.meta.get("fields", {"fieldtype": ('=', "Dynamic Link")})):
            docname = self.get(df.fieldname)

            if docname:
                if df.fieldtype == "Link":
                    doctype = df.options
                    if not doctype:
                        frappe.throw(_("Options not set for link field {0}").format(df.fieldname))
                else:
                    doctype = self.get(df.options)
                    if not doctype:
                        frappe.throw(_("{0} must be set first").format(self.meta.get_label(df.options)))

                # MySQL is case insensitive. Preserve case of the original docname in the Link Field.

                # get a map of values ot fetch along with this link query
                # that are mapped as link_fieldname.source_fieldname in Options of
                # Readonly or Data or Text type fields

                fields_to_fetch = [
                    _df for _df in self.meta.get_fields_to_fetch(df.fieldname)
                    if
                    not _df.get('fetch_if_empty')
                    or (_df.get('fetch_if_empty') and not self.get(_df.fieldname))
                ]

                if not fields_to_fetch:
                    # cache a single value type
                    values = frappe._dict(name=frappe.db.get_value(doctype, docname,
                                                                   'name', cache=True))
                else:
                    values_to_fetch = ['name'] + [_df.fetch_from.split('.')[-1]
                                                  for _df in fields_to_fetch]

                    # don't cache if fetching other values too
                    values = frappe.db.get_value(doctype, docname,
                                                 values_to_fetch, as_dict=True)

                if frappe.get_meta(doctype).issingle:
                    values.name = doctype

                if values:
                    setattr(self, df.fieldname, values.name)

                    for _df in fields_to_fetch:
                        if self.is_new() or self.docstatus != 1 or _df.allow_on_submit:
                            setattr(self, _df.fieldname, values[_df.fetch_from.split('.')[-1]])

                    if not values.name:
                        invalid_links.append((df.fieldname, docname, get_msg(df, docname)))

                    elif (df.fieldname != "amended_from"
                          and (is_submittable or self.meta.is_submittable) and frappe.get_meta(doctype).is_submittable
                          and cint(frappe.db.get_value(doctype, docname, "docstatus")) == 2):

                        cancelled_links.append((df.fieldname, docname, get_msg(df, docname)))

        return invalid_links, cancelled_links

    def _validate_selects(self):
        if frappe.flags.in_import:
            return

        for df in self.meta.get_select_fields():
            if df.fieldname == "naming_series" or not (self.get(df.fieldname) and df.options):
                continue

            options = (df.options or "").split("\n")

            # if only empty options
            if not filter(None, options):
                continue

            # strip and set
            self.set(df.fieldname, cstr(self.get(df.fieldname)).strip())
            value = self.get(df.fieldname)

            if value not in options and not (frappe.flags.in_test and value.startswith("_T-")):
                # show an elaborate message
                prefix = _("Row #{0}:").format(self.idx) if self.get("parentfield") else ""
                label = _(self.meta.get_label(df.fieldname))
                comma_options = '", "'.join(_(each) for each in options)

                frappe.throw(_('{0} {1} cannot be "{2}". It should be one of "{3}"').format(prefix, label,
                                                                                            value, comma_options))

    def _validate_constants(self):
        if frappe.flags.in_import or self.is_new() or self.flags.ignore_validate_constants:
            return

        constants = [d.fieldname for d in self.meta.get("fields", {"set_only_once": ('=', 1)})]
        if constants:
            values = frappe.db.get_value(self.doctype, self.name, constants, as_dict=True)

        for fieldname in constants:
            df = self.meta.get_field(fieldname)

            # This conversion to string only when fieldtype is Date
            if df.fieldtype == 'Date' or df.fieldtype == 'Datetime':
                value = str(values.get(fieldname))

            else:
                value = values.get(fieldname)

            if self.get(fieldname) != value:
                frappe.throw(_("Value cannot be changed for {0}").format(self.meta.get_label(fieldname)),
                             frappe.CannotChangeConstantError)

    def _validate_length(self):
        if frappe.flags.in_install:
            return

        if self.meta.issingle:
            # single doctype value type is mediumtext
            return

        type_map = frappe.db.type_map

        for fieldname, value in iteritems(self.get_valid_dict()):
            df = self.meta.get_field(fieldname)

            if not df or df.fieldtype == 'Check':
                # skip standard fields and Check fields
                continue

            column_type = type_map[df.fieldtype][0] or None

            if column_type == 'varchar':
                default_column_max_length = type_map[df.fieldtype][1] or None
                max_length = cint(df.get("length")) or cint(default_column_max_length)

                if len(cstr(value)) > max_length:
                    self.throw_length_exceeded_error(df, max_length, value)

            elif column_type in ('int', 'bigint', 'smallint'):
                max_length = max_positive_value[column_type]

                if abs(cint(value)) > max_length:
                    self.throw_length_exceeded_error(df, max_length, value)

    def throw_length_exceeded_error(self, df, max_length, value):
        if self.parentfield and self.idx:
            reference = _("{0}, Row {1}").format(_(self.doctype), self.idx)

        else:
            reference = "{0} {1}".format(_(self.doctype), self.name)

        frappe.throw(_("{0}: '{1}' ({3}) will get truncated, as max characters allowed is {2}") \
                     .format(reference, _(df.label), max_length, value), frappe.CharacterLengthExceededError,
                     title=_('Value too big'))

    def _validate_update_after_submit(self):
        # get the full doc with children
        db_values = frappe.get_doc(self.doctype, self.name).as_dict()

        for key in self.as_dict():
            df = self.meta.get_field(key)
            db_value = db_values.get(key)

            if df and not df.allow_on_submit and (self.get(key) or db_value):
                if df.fieldtype in table_fields:
                    # just check if the table size has changed
                    # individual fields will be checked in the loop for children
                    self_value = len(self.get(key))
                    db_value = len(db_value)

                else:
                    self_value = self.get_value(key)

                if self_value != db_value:
                    frappe.throw(_("Not allowed to change {0} after submission").format(df.label),
                                 frappe.UpdateAfterSubmitError)

    def _sanitize_content(self):
        """Sanitize HTML and Email in field values. Used to prevent XSS.

            - Ignore if 'Ignore XSS Filter' is checked or fieldtype is 'Code'
        """
        if frappe.flags.in_install:
            return

        for fieldname, value in self.get_valid_dict().items():
            if not value or not isinstance(value, string_types):
                continue

            value = frappe.as_unicode(value)

            if (u"<" not in value and u">" not in value):
                # doesn't look like html so no need
                continue

            elif "<!-- markdown -->" in value and not ("<script" in value or "javascript:" in value):
                # should be handled separately via the markdown converter function
                continue

            df = self.meta.get_field(fieldname)
            sanitized_value = value

            if df and df.get("fieldtype") in ("Data", "Code", "Small Text") and df.get("options") == "Email":
                sanitized_value = value

            elif df and (df.get("ignore_xss_filter")
                         or (df.get("fieldtype") == "Code" and df.get("options") != "Email")
                         or df.get("fieldtype") in ("Attach", "Attach Image", "Barcode")

                         # cancelled and submit but not update after submit should be ignored
                         or self.docstatus == 2
                         or (self.docstatus == 1 and not df.get("allow_on_submit"))):
                continue

            else:
                sanitized_value = value

            self.set(fieldname, sanitized_value)

    def _save_passwords(self):
        '''Save password field values in __Auth table'''
        if self.flags.ignore_save_passwords is True:
            return

        for df in self.meta.get('fields', {'fieldtype': ('=', 'Password')}):
            if self.flags.ignore_save_passwords and df.fieldname in self.flags.ignore_save_passwords: continue
            new_password = self.get(df.fieldname)
            if new_password and not self.is_dummy_password(new_password):
                # set dummy password like '*****'
                self.set(df.fieldname, '*' * len(new_password))

    def get_password(self, fieldname='password', raise_exception=True):
        if self.get(fieldname) and not self.is_dummy_password(self.get(fieldname)):
            return self.get(fieldname)

        return "frappe"

    def is_dummy_password(self, pwd):
        return ''.join(set(pwd)) == '*'

    def precision(self, fieldname, parentfield=None):
        """Returns float precision for a particular field (or get global default).

        :param fieldname: Fieldname for which precision is required.
        :param parentfield: If fieldname is in child table."""
        from frappe.model.meta import get_field_precision

        if parentfield and not isinstance(parentfield, string_types):
            parentfield = parentfield.parentfield

        cache_key = parentfield or "main"

        if not hasattr(self, "_precision"):
            self._precision = frappe._dict()

        if cache_key not in self._precision:
            self._precision[cache_key] = frappe._dict()

        if fieldname not in self._precision[cache_key]:
            self._precision[cache_key][fieldname] = None

            doctype = self.meta.get_field(parentfield).options if parentfield else self.doctype
            df = frappe.get_meta(doctype).get_field(fieldname)

            if df.fieldtype in ("Currency", "Float", "Percent"):
                self._precision[cache_key][fieldname] = get_field_precision(df, self)

        return self._precision[cache_key][fieldname]

    def get_formatted(self, fieldname, doc=None, currency=None, absolute_value=False, translated=False):
        from frappe.utils.formatters import format_value

        df = self.meta.get_field(fieldname)
        if not df and fieldname in default_fields:
            from frappe.model.meta import get_default_df
            df = get_default_df(fieldname)

        val = self.get(fieldname)

        if translated:
            val = _(val)

        if absolute_value and isinstance(val, (int, float)):
            val = abs(self.get(fieldname))

        if not doc:
            doc = getattr(self, "parent_doc", None) or self

        return format_value(val, df=df, doc=doc, currency=currency)

    def is_print_hide(self, fieldname, df=None, for_print=True):
        """Returns true if fieldname is to be hidden for print.

        Print Hide can be set via the Print Format Builder or in the controller as a list
        of hidden fields. Example

            class MyDoc(Document):
                def __setup__(self):
                    self.print_hide = ["field1", "field2"]

        :param fieldname: Fieldname to be checked if hidden.
        """
        meta_df = self.meta.get_field(fieldname)
        if meta_df and meta_df.get("__print_hide"):
            return True

        print_hide = 0

        if self.get(fieldname) == 0 and not self.meta.istable:
            print_hide = (df and df.print_hide_if_no_value) or (meta_df and meta_df.print_hide_if_no_value)

        if not print_hide:
            if df and df.print_hide is not None:
                print_hide = df.print_hide
            elif meta_df:
                print_hide = meta_df.print_hide

        return print_hide

    def in_format_data(self, fieldname):
        """Returns True if shown via Print Format::`format_data` property.
            Called from within standard print format."""
        doc = getattr(self, "parent_doc", self)

        if hasattr(doc, "format_data_map"):
            return fieldname in doc.format_data_map
        else:
            return True

    def reset_values_if_no_permlevel_access(self, has_access_to, high_permlevel_fields):
        """If the user does not have permissions at permlevel > 0, then reset the values to original / default"""
        to_reset = []

        for df in high_permlevel_fields:
            if df.permlevel not in has_access_to and df.fieldtype not in display_fieldtypes:
                to_reset.append(df)

        if to_reset:
            if self.is_new():
                # if new, set default value
                ref_doc = frappe.new_doc(self.doctype)
            else:
                # get values from old doc
                if self.get('parent_doc'):
                    self.parent_doc.get_latest()
                    ref_doc = [d for d in self.parent_doc.get(self.parentfield) if d.name == self.name][0]
                else:
                    ref_doc = self.get_latest()

            for df in to_reset:
                self.set(df.fieldname, ref_doc.get(df.fieldname))

    def get_value(self, fieldname):
        df = self.meta.get_field(fieldname)
        val = self.get(fieldname)

        return self.cast(val, df)

    def cast(self, value, df):
        return cast_fieldtype(df.fieldtype, value)

    def _extract_images_from_text_editor(self):
        pass


def cast_fieldtype(fieldtype, value):
    if fieldtype in ("Currency", "Float", "Percent"):
        value = flt(value)

    elif fieldtype in ("Int", "Check"):
        value = cint(value)

    elif fieldtype in ("Data", "Text", "Small Text", "Long Text",
                       "Text Editor", "Select", "Link", "Dynamic Link"):
        value = cstr(value)

    elif fieldtype == "Date":
        value = getdate(value)

    elif fieldtype == "Datetime":
        value = get_datetime(value)

    elif fieldtype == "Time":
        value = to_timedelta(value)

    return value

def _filter(data, filters, limit=None):
    """pass filters as:
        {"key": "val", "key": ["!=", "val"],
        "key": ["in", "val"], "key": ["not in", "val"], "key": "^val",
        "key" : True (exists), "key": False (does not exist) }"""

    out, _filters = [], {}

    if not data:
        return out

    # setup filters as tuples
    if filters:
        for f in filters:
            fval = filters[f]

            if not isinstance(fval, (tuple, list)):
                if fval is True:
                    fval = ("not None", fval)
                elif fval is False:
                    fval = ("None", fval)
                elif isinstance(fval, string_types) and fval.startswith("^"):
                    fval = ("^", fval[1:])
                else:
                    fval = ("=", fval)

            _filters[f] = fval

    for d in data:
        add = True
        for f, fval in iteritems(_filters):
            if not frappe.compare(getattr(d, f, None), fval[0], fval[1]):
                add = False
                break

        if add:
            out.append(d)
            if limit and (len(out) - 1) == limit:
                break

    return out
