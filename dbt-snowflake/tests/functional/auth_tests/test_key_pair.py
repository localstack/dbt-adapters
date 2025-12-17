import os

from dbt.tests.util import run_dbt
import pytest


class TestKeyPairAuth:
    @pytest.fixture(scope="class", autouse=True)
    def dbt_profile_target(self):
        private_key_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "rsa_key.p8")
        )
        return {
            "type": "snowflake",
            "threads": 4,
            "account": "localstack",
            "host": "snowflake.localhost.localstack.cloud",
            "user": os.getenv("SNOWFLAKE_TEST_USER"),
            "private_key": os.getenv("SNOWFLAKE_TEST_PRIVATE_KEY"),
            "database": os.getenv("SNOWFLAKE_TEST_DATABASE"),
            "warehouse": os.getenv("SNOWFLAKE_TEST_WAREHOUSE"),
        }

    @pytest.fixture(scope="class")
    def models(self):
        return {"my_model.sql": "select 1 as id"}

    def test_connection(self, project):
        run_dbt()
