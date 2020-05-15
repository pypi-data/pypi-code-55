# _*_ coding: utf-8 _*_
from plone.app.fhirfield import FhirResource
from plone.dexterity.content import Container
from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer


__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"


class IOrganization(model.Schema):
    """ """

    organization_resource = FhirResource(
        title=u"Fhir Organization Field",
        fhir_release="STU3",
        model="fhir.resources.STU3.organization.Organization",
    )


@implementer(IOrganization)
class Organization(Container):
    """ """


class IPatient(model.Schema):
    """ """

    patient_resource = FhirResource(
        title=u"Fhir Patient Field",
        fhir_release="STU3",
        model="fhir.resources.STU3.patient.Patient",
    )


@implementer(IPatient)
class Patient(Container):
    """ """


class IPractitioner(model.Schema):
    """ """

    practitioner_resource = FhirResource(
        title=u"Fhir Practitioner Field",
        fhir_release="STU3",
        model="fhir.resources.STU3.practitioner.Practitioner",
    )


@implementer(IPractitioner)
class Practitioner(Container):
    """ """


class IQuestionnaire(model.Schema):
    """ """

    questionnaire_resource = FhirResource(
        title=u"Fhir Questionnaire Field",
        fhir_release="STU3",
        model="fhir.resources.STU3.questionnaire.Questionnaire",
    )


@implementer(IQuestionnaire)
class Questionnaire(Container):
    """ """


class IQuestionnaireResponse(model.Schema):
    """ """

    questionnaireresponse_resource = FhirResource(
        title=u"Fhir QuestionnaireResponse Field",
        fhir_release="STU3",
        model="fhir.resources.STU3.questionnaireresponse.QuestionnaireResponse",
    )


@implementer(IQuestionnaireResponse)
class QuestionnaireResponse(Container):
    """ """


class ITask(model.Schema):
    """ """

    task_resource = FhirResource(
        title=u"Fhir Task Field",
        fhir_release="STU3",
        model="fhir.resources.STU3.task.Task",
    )


@implementer(ITask)
class Task(Item):
    """ """


class IProcedureRequest(model.Schema):
    """ """

    procedurerequest_resource = FhirResource(
        title=u"Fhir ProcedureRequest Field",
        fhir_release="STU3",
        model="fhir.resources.STU3.procedurerequest.ProcedureRequest",
    )


@implementer(IProcedureRequest)
class ProcedureRequest(Item):
    """ """


class IDevice(model.Schema):
    """ """

    device_resource = FhirResource(
        title=u"Fhir Device Field", fhir_release="STU3", resource_type="Device"
    )


@implementer(IDevice)
class Device(Item):
    """ """


class IDeviceRequest(model.Schema):
    """ """

    devicerequest_resource = FhirResource(
        title=u"Fhir DeviceRequest Field",
        fhir_release="STU3",
        resource_type="DeviceRequest",
    )


@implementer(IDeviceRequest)
class DeviceRequest(Item):
    """ """


class IValueSet(model.Schema):
    """ """

    valueset_resource = FhirResource(
        title=u"Fhir ValueSet Field", fhir_release="STU3", resource_type="ValueSet"
    )


@implementer(IValueSet)
class ValueSet(Item):
    """ """


class IChargeItem(model.Schema):
    """"""

    chargeitem_resource = FhirResource(
        title=u"Fhir ChargeItem Field", fhir_release="STU3", resource_type="ChargeItem"
    )


@implementer(IChargeItem)
class ChargeItem(Item):
    """ """


class IEncounter(model.Schema):
    """"""

    encounter_resource = FhirResource(
        title=u"Fhir FFEncounter Field", fhir_release="STU3", resource_type="Encounter"
    )


@implementer(IEncounter)
class Encounter(Item):
    """ """


class IMedicationRequest(model.Schema):
    """"""

    medicationrequest_resource = FhirResource(
        title=u"Fhir MedicationRequest Field",
        fhir_release="STU3",
        resource_type="MedicationRequest",
    )


@implementer(IMedicationRequest)
class MedicationRequest(Item):
    """ """


class IObservation(model.Schema):
    """"""

    observation_resource = FhirResource(
        title=u"Fhir Observation Field",
        fhir_release="STU3",
        resource_type="Observation",
    )


@implementer(IObservation)
class Observation(Item):
    """ """


class IMedia(model.Schema):
    """"""

    media_resource = FhirResource(
        title=u"Fhir Media Field", fhir_release="STU3", resource_type="Media"
    )


@implementer(IMedia)
class Media(Item):
    """ """
