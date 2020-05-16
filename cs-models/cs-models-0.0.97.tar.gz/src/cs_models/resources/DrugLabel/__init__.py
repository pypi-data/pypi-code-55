from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from marshmallow import ValidationError

from cs_models.utils.utils import update_model
from ...database import db_session
from ...resources.DrugLabel.models import DrugLabelModel
from .schemas import (
    DrugLabelPatchSchema,
    DrugLabelQueryParamsSchema,
    DrugLabelResourceSchema,
)


schema_resource = DrugLabelResourceSchema()
schema_params = DrugLabelQueryParamsSchema()
schema_patch = DrugLabelPatchSchema()


class DrugLabel(object):
    @staticmethod
    def create(params):
        """
        Args:
            params: dict(DrugLabelResourceSchema)

        Returns: DrugLabelResourceSchema

        Raises:
            ValidationError
            SQLAlchemyError
        """
        data, errors = schema_resource.load(params)
        if errors:
            raise ValidationError(errors)
        response = _helper_create(data)
        return response

    @staticmethod
    def read(params):
        """
        Args:
            params: dict(DrugLabelQueryParamsSchema)

        Returns: List<DrugLabelResourceSchema>

        Raises:
            ValidationError
        """
        data, errors = schema_params.load(params)
        if errors:
            raise ValidationError(errors)
        drug_label_query = _build_query(params=data)
        response = schema_resource.dump(drug_label_query, many=True).data
        return response

    @staticmethod
    def one(params):
        """
        Args:
            params: dict(DrugLabelQueryParamsSchema)

        Returns: DrugLabelResourceSchema

        Raises:
            ValidationError
        """
        data, errors = schema_params.load(params)
        if errors:
            raise ValidationError(errors)
        drug_label_query = _build_query(params=data).one()
        response = schema_resource.dump(drug_label_query).data
        return response

    @staticmethod
    def update(id, params):
        """

        Args:
            id: int
            params: DrugLabelPatchSchema

        Returns:
            DrugLabelResourceSchema

        Raises:
            sqlalchemy.orm.exc.NoResultFound
            sqlalchemy.orm.exc.MultipleResultsFound
            ValidationError
        """
        drug_label_query = db_session.query(DrugLabel).filter_by(id=id).one()
        data, errors = schema_patch.load(params)
        if errors:
            raise ValidationError(errors)

        response = _helper_update(data, drug_label_query)
        return response

    @staticmethod
    def upsert(params):
        """
        Args:
            params: DrugLabelResourceSchema

        Returns:
            DrugLabelResourceSchema

        Raises:
            ValidationError
        """
        data, errors = schema_resource.load(params)
        if errors:
            raise ValidationError(errors)

        try:
            query_params = {
                "spl_id": params["spl_id"],
                "set_id": params["set_id"],
            }
            drug_label_query = _build_query(query_params).one()
            response = _helper_update(data, drug_label_query)
        except NoResultFound:
            response = _helper_create(data)
        return response

    @staticmethod
    def delete(id):
        """
        Args:
            id: int

        Returns: string

        Raises:
            sqlalchemy.orm.exc.NoResultFound
            sqlalchemy.orm.exc.MultipleResultsFound
            SQLAlchemyError
        """
        drug_label_query = (
            db_session.query(DrugLabelModel).filter_by(id=id).one()
        )
        try:
            db_session.delete(drug_label_query)
            db_session.commit()
            db_session.close()
            return "Successfully deleted"
        except SQLAlchemyError:
            db_session.rollback()
            db_session.close()
            raise


def _helper_create(data):
    new_drug_label = DrugLabelModel(**data)
    try:
        db_session.add(new_drug_label)
        db_session.commit()
        drug_label_query = db_session.query(DrugLabelModel).get(
            new_drug_label.id
        )
        response = schema_resource.dump(drug_label_query).data
        db_session.close()
        return response
    except SQLAlchemyError:
        db_session.rollback()
        db_session.close()
        raise


def _helper_update(data, drug_label_query):
    data["id"] = drug_label_query.id
    try:
        update_model(data, drug_label_query)
        db_session.commit()
        response = schema_resource.dump(drug_label_query).data
        return response
    except SQLAlchemyError:
        db_session.rollback()
        raise


def _build_query(params):
    q = db_session.query(DrugLabelModel)
    if params.get("id"):
        q = q.filter_by(id=params.get("id"))
    if params.get("spl_id"):
        q = q.filter_by(spl_id=params.get("spl_id"))
    if params.get("set_id"):
        q = q.filter_by(set_id=params.get("set_id"))
    return q
