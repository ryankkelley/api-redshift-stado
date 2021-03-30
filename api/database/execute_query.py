import time
import boto3
from config import Config
from api.database.schemas.TradeDesk import get_schema


def execute_query(sql):
    data_client = boto3.client('redshift-data')
    result = data_client.execute_statement(
        ClusterIdentifier=Config.CLUSTER_NAME,
        Database=Config.DATABASE_NAME,
        DbUser=Config.DB_USER,
        Sql=sql,
    )


    id = result['Id']
    #print('id = {}'.format(id))

    statement = ''
    status = ''
    while status != 'FINISHED' and status != 'FAILED' and status != 'ABORTED':
        statement = data_client.describe_statement(Id=id)
        #print(statement)
        status = statement['Status']
        time.sleep(1)

    if status == 'FINISHED':
        if int(statement['ResultSize']) > 0:
            statement = data_client.get_statement_result(Id=id)
            results = []
            for row in statement['Records']:
                schema = get_schema(row)
                results.append(schema)
            return results
        else:
            print('QUERY FINISHED')
            return None
    elif status == 'FAILED':
        print('QUERY FAILED\n{}'.format(statement))
        return None
    elif status == 'ABORTED':
        print('QUERY ABORTED: The query run was stopped by the user.')


