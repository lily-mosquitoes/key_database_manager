import unittest
import os
import pymysql
from models.model_dataset import ModelDataset

class ModelDatasetInputValidationTestCase(unittest.TestCase):

    def setUp(self):

        os.system('cd tests; ./setup_test_key_database.sh')

    def tearDown(self):

        os.system('cd tests; ./teardown_test_key_database.sh')

    def test_update_accepts_0(self):

        db = ModelDataset(
            user=os.environ.get('MYSQL_USER'),
            host=os.environ.get('MYSQL_HOST'),
            password=os.environ.get('MYSQL_PASSWORD'),
            db='test_key_database'
        )

        try:
            db.update(species="Anopheles (Anopheles) walkeri", value='0', couplet='cp_Mesopostnotum')
        except pymysql.Error as e:
            self.fail(e)

        db.connection.close()

    def test_update_accepts_1(self):

        db = ModelDataset(
            user=os.environ.get('MYSQL_USER'),
            host=os.environ.get('MYSQL_HOST'),
            password=os.environ.get('MYSQL_PASSWORD'),
            db='test_key_database'
        )

        try:
            db.update(species="Anopheles (Anopheles) walkeri", value='1', couplet='cp_Mesopostnotum')
        except pymysql.Error as e:
            self.fail(e)

        db.connection.close()

    def test_update_accepts_01(self):

        db = ModelDataset(
            user=os.environ.get('MYSQL_USER'),
            host=os.environ.get('MYSQL_HOST'),
            password=os.environ.get('MYSQL_PASSWORD'),
            db='test_key_database'
        )

        try:
            db.update(species="Anopheles (Anopheles) walkeri", value='01', couplet='cp_Mesopostnotum')
        except pymysql.Error as e:
            self.fail(e)

        db.connection.close()

    def test_update_accepts_10(self):

        db = ModelDataset(
            user=os.environ.get('MYSQL_USER'),
            host=os.environ.get('MYSQL_HOST'),
            password=os.environ.get('MYSQL_PASSWORD'),
            db='test_key_database'
        )

        try:
            db.update(species="Anopheles (Anopheles) walkeri", value='10', couplet='cp_Mesopostnotum')
        except pymysql.Error as e:
            self.fail(e)

        db.connection.close()

    def test_update_accepts_NA(self):

        db = ModelDataset(
            user=os.environ.get('MYSQL_USER'),
            host=os.environ.get('MYSQL_HOST'),
            password=os.environ.get('MYSQL_PASSWORD'),
            db='test_key_database'
        )

        try:
            db.update(species="Anopheles (Anopheles) walkeri", value='NA', couplet='cp_Mesopostnotum')
        except pymysql.Error as e:
            self.fail(e)

        db.connection.close()

    def test_update_accepts_None(self):

        db = ModelDataset(
            user=os.environ.get('MYSQL_USER'),
            host=os.environ.get('MYSQL_HOST'),
            password=os.environ.get('MYSQL_PASSWORD'),
            db='test_key_database'
        )

        try:
            db.update(species="Anopheles (Anopheles) walkeri", value=None, couplet='cp_Mesopostnotum')
        except pymysql.Error as e:
            self.fail(e)

        db.connection.close()

    def test_update_not_accepts_other_values(self):

        db = ModelDataset(
            user=os.environ.get('MYSQL_USER'),
            host=os.environ.get('MYSQL_HOST'),
            password=os.environ.get('MYSQL_PASSWORD'),
            db='test_key_database'
        )

        with self.assertRaises(pymysql.IntegrityError):
            db.update(species="Anopheles (Anopheles) walkeri", value='not-valid-value', couplet='cp_Mesopostnotum')

        db.connection.close()
