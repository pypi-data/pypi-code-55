import json
import traceback
from typing import Type, Dict, Any, List

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.db.models import Model, QuerySet
from django import forms
from django.http import HttpResponse, HttpRequest, JsonResponse


def reformat_model_dict(model_representation):
    return {'id': model_representation['pk'], **model_representation['fields']}


class ModelFriendlyJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuerySet):
            return [reformat_model_dict(md) for md in serializers.serialize('python', obj)]
        elif issubclass(type(obj), Model):
            return reformat_model_dict(serializers.serialize('python', [obj])[0])
        else:
            return super().default(obj)


def success_wrapper(output):
    return {'success': output}

def error_wrapper(output):
    return {'error': output}


class BaseEndpoint:
    request = None

    success_wrapper = success_wrapper
    error_wrapper = error_wrapper

    def __init__(self, *args, **kwargs):
        self.request: HttpRequest = kwargs.get('request', None)

    def as_response(self) -> HttpResponse:
        status_code = 200
        try:
            output = self.success_wrapper(self.get_http_method_handler()())
        except Exception as e:
            traceback.print_exc()

            try:
                message = json.loads(str(e))
            except json.JSONDecodeError:
                message = str(e)

            status_code = e.status_code if hasattr(e, 'status_code') else 500

            output = self.error_wrapper({'type': type(e).__name__,
                                         'message': message})

        return JsonResponse(data=output, encoder=ModelFriendlyJSONEncoder, status=status_code)


    def create(self):
        raise Exception("create is not implemented yet.")

    def delete(self):
        raise Exception("delete is not implemented yet.")

    def get(self):
        raise Exception("get is not implemented yet.")

    def update(self) :
        raise Exception("update is not implemented yet.")

    def partial_update(self):
        raise Exception("partial update is not implemented yet.")

    def get_request_body(self) -> Dict[str, Any]:
        return json.loads(self.request.body)

    def get_http_method_handler(self):

        if self.request.method == 'GET':
            return self.get
        elif self.request.method == 'POST':
            return self.create
        elif self.request.method == 'DELETE':
            return self.delete
        elif self.request.method == 'PUT':
            return self.update
        elif self.request.method == 'PATCH':
            return self.partial_update
        else:
            # TODO the rest of the HTTP MethodsS
            raise NotImplementedError(f"Handler for {self.request.method} is not implemented yet.")


class ModelEndpoint(BaseEndpoint):
    # General attributes
    model: Model = None  # use self.get_model() where possible
    queryset: QuerySet = None  # use self.get_queryset() where possible
    form = None  # usurped by create_form or update_form or partial_update_form if they're defined.

    # Creation specific attributes
    create_objects_key = 'objects'
    creation_form = None

    update_form = None

    partial_update_form = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'model' in kwargs:
            self.model = kwargs['model']
        if 'queryset' in kwargs:
            self.queryset = kwargs['queryset']

    @transaction.atomic
    def create(self):
        if self.create_objects_key in self.get_request_body():
            raw_object_representations = self.get_request_body()[self.create_objects_key]
            cleaned_object_representations = self.clean_creation_representations(raw_object_representations)
            instances = self.instantiate_creations(cleaned_object_representations)
            return self.get_model().objects.bulk_create(instances)
        else:
            raise BaseHttpException(f"Could not find objects attribute '{self.create_objects_key}'", status_code=422)

    def clean_creation_representations(self, object_representations: List[dict]) -> List[dict]:
        all_valid = True
        error_list = []
        cleaned_representations = []
        for object_representation in object_representations:
            valid, clean_data, errors = self.clean_creation_representation(object_representation)
            all_valid = valid and all_valid
            error_list.append(errors)
            cleaned_representations.append(clean_data)

        if not all_valid:
            raise BaseHttpException(json.dumps(error_list))
        return cleaned_representations

    def clean_creation_representation(self, object_representation: dict):
        result = self.get_creation_form()(object_representation, request=self.request)
        return (result.is_valid(),
                result.cleaned_data,
                result.errors.get_json_data())

    def instantiate_creations(self, object_representations: List[dict]):
        return [self.instantiate_creation(rep) for rep in object_representations]

    def instantiate_creation(self, object_representation: dict):
        return self.get_model()(**object_representation)

    def delete(self):
        return self.get_filtered_queryset().delete()

    def get(self):
        return self.get_filtered_queryset()

    def update(self):
        instance = self.get_queryset().get(**self.get_query_filters())
        form: RequestAwareModelForm = self.get_update_form()(self.get_request_body(), instance=instance)
        return form.save()

        queryset = self.get_filtered_queryset()

        found_count = queryset.count()
        if found_count < 1:
            raise BaseHttpException("No object could be found that matches your parameters.")
        elif found_count > 1:
            raise BaseHttpException("More than one object matches your parameters. Only one object can be fully updated at a time.")

        return queryset.update(**self.get_request_body())

    @transaction.atomic
    def partial_update(self):
        all_valid = True
        error_list = []
        forms = []
        for instance in self.get_filtered_queryset():
            valid, form, errors = self.check_partial_update_instance(update_data=self.get_request_body(),
                                                                    instance=instance)
            all_valid = valid and all_valid
            error_list.append(errors)
            forms.append(form)

        if not all_valid:
            raise BaseHttpException(json.dumps(error_list))

        return self.get_filtered_queryset().update(**self.get_request_body())

    def check_partial_update_instance(self, update_data, instance):
        result = self.get_partial_update_form()(update_data, instance=instance, request=self.request)
        return (result.is_valid(),
                result,
                result.errors.get_json_data())

    def get_creation_form(self):
        if self.creation_form:
            return self.creation_form
        elif self.form:
            return self.form
        else:
            raise BaseHttpException("No creation form has been specified")

    def get_update_form(self):
        if self.update_form:
            return self.update_form
        elif self.form:
            return self.form
        else:
            raise BaseHttpException("No update form has been specified")

    def get_partial_update_form(self):
        if self.partial_update_form:
            return self.partial_update_form
        elif self.form:
            return self.form
        else:
            raise BaseHttpException("No partial update form has been specified")

    def get_model(self) -> Type[Model]:
        if self.model is not None:
            return self.model
        # else:
        #     raise BaseHttpException("Model was not defined")

    def get_queryset(self) -> QuerySet:
        return self.queryset if self.queryset is not None else self.get_model().objects.all()

    def get_filtered_queryset(self) -> QuerySet:
        return self.get_queryset().filter(**self.get_query_filters())

    def get_query_filters(self):
        filter_params = dict()
        for key in self.request.GET.keys():
            values = self.request.GET.getlist(key)
            filter_key = f'{key}__in' if len(values) > 1 else key
            filter_params[filter_key] = values if len(values) > 1 else values[0]
        return filter_params


class BaseHttpException(Exception):
    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.status_code: int = status_code


# Identical to a ModelForm, but also accepts the request as a keyword param
class RequestAwareModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request: HttpRequest = kwargs.pop('request')
        super().__init__(*args, **kwargs)


