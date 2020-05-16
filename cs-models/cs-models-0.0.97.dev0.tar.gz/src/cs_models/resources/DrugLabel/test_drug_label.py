import copy
from marshmallow import ValidationError
from sqlalchemy.orm.exc import (
    NoResultFound,
)
from parameterized import parameterized

from test.backendtestcase import TestCase
from test.utils import second_equals_first
from src.cs_models.resources.DrugLabel import DrugLabel


class DrugLabelResourceTestCase(TestCase):
    def setUp(self):
        super(DrugLabelResourceTestCase, self).setUp()
        self.inst = DrugLabel()

        self.label1 = self.inst.create({
            'spl_id': 'da403619-0631-4188-887a-e52b7bff07eb',
            'set_id': '7bf3e616-45e8-4469-a75d-4d824ce951ea',
            'indication_text': "INDICATIONS AND USAGE Zarontin is indicated for the control of absence (petit mal) epilepsy.",
        })

        self.label2 = self.inst.create({
            'spl_id': 'd82208ea-381b-4508-a3ac-638f8925b934',
            'set_id': '1d88fbe0-eb97-4964-8a78-88940064f8f0',
            'indication_text': "INDICATIONS AND USAGE TrophAmine® is indicated for the nutritional support of infants (including those of low birth weight) and young pediatric patients requiring TPN via either central or peripheral infusion routes.",
        })

        self.valid_data = {
            'spl_id': '8e3d9cc9-eb36-402e-aca4-18770713c652',
            'set_id': '2ac76334-e3c8-44e6-9eb5-2c4262e6e945',
            'indication_text': "1 INDICATIONS AND USAGE Zolpidem Tartrate Extended-Release Tablets are indicated for the treatment of insomnia characterized by difficulties with sleep onset and/or sleep maintenance (as measured by wake time after sleep onset). The clinical trials performed in support of efficacy were up to 3 weeks (using polysomnography measurement up to 2 weeks in both adult and elderly patients) and 24 weeks (using patient-reported assessment in adult patients only) in duration [see Clinical Studies (14)]. Zolpidem Tartrate Extended-Release Tablets, a gamma-aminobutyric acid (GABA) A receptor positive modulator, is indicated for the treatment of insomnia characterized by difficulties with sleep onset and/or sleep maintenance. (1)",
        }

    @parameterized.expand([
        ('spl_id',),
    ])
    def test_create_validation_error_missing_field(self, field_to_pop):
        base_data = copy.copy(self.valid_data)
        base_data.pop(field_to_pop)
        self.assertRaises(
            ValidationError,
            self.inst.create,
            base_data,
        )

    def test_create(self):
        resp = self.inst.create(self.valid_data)
        expected_data = {
            **self.valid_data,
        }
        second_equals_first(expected_data, resp)

    def test_read(self):
        resp = self.inst.read({})
        self.assertEqual(2, len(resp))

    @parameterized.expand([
        ('id', 'label1', 'id', 1),
        ('indication_text', 'label1', 'indication_text', 2),
    ])
    def test_read_w_params(
        self,
        field_name,
        attr,
        attr_field,
        expected_length,
    ):
        resp = self.inst.read({})
        self.assertEqual(2, len(resp))

        resp = self.inst.read({
            field_name: getattr(self, attr)[attr_field],
        })
        self.assertEqual(expected_length, len(resp))

    @parameterized.expand([
        ('id', 999, NoResultFound),
    ])
    def test_one_raises_exception(self, field_name, field_value, exception):
        self.assertRaises(
            exception,
            self.inst.one,
            {
                field_name: field_value,
            },
        )

    @parameterized.expand([
        ('id',),
        ('spl_id',),
    ])
    def test_one(self, field_name):
        resp = self.inst.one({
            field_name: self.label1[field_name],
        })
        second_equals_first(
            self.label1,
            resp,
        )

    def test_upsert_validation_error(self):
        self.assertRaises(
            ValidationError,
            self.inst.upsert,
            {
                'spl_id': self.valid_data['spl_id'],
            }
        )

    def test_upsert_creates_new_entry(self):
        data = copy.copy(self.valid_data)
        self.assertEqual(2, len(self.inst.read({})))
        self.inst.upsert(data)
        self.assertEqual(3, len(self.inst.read({})))

    def test_upsert_updates_existing_row(self):
        data = {
            **self.valid_data,
            **{'spl_id': self.label1['spl_id'],
               'set_id': self.label1['set_id'],
               'indication_text': self.label1['indication_text'],
               },
        }
        resp = self.inst.upsert(data)
        expected_data = {
            **data,
        }
        second_equals_first(
            expected_data,
            resp,
        )
        self.assertEqual(2, len(self.inst.read({})))
