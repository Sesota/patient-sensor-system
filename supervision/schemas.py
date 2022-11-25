from ninja import Schema

from datasource.enums import Datasources


class SupervisionDatasourcesConfig(Schema):
    datasource: Datasources
