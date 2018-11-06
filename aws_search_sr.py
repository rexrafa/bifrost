import boto3

def switching_role(arn, nome):
    sts_client = boto3.client('sts')
    credentials = ""
    try:
        assumedRoleObject = sts_client.assume_role(
            RoleArn=arn,
            RoleSessionName=nome
        )
        credentials = assumedRoleObject['Credentials']
    except Exception as e:
        #Tratamento de erro para caso nao seja possivel realizar o switch role
        print ("Nao foi possivel realizar o switch role {}".format(e))
        credentials = False
    return credentials


def ec2_connection(credentials, region):
    client = boto3.client(
        'ec2',
        aws_access_key_id = credentials['AccessKeyId'],
        aws_secret_access_key = credentials['SecretAccessKey'],
        aws_session_token = credentials['SessionToken'],
        region_name = region
    )
    return client


def list_instances_sr(tagvalue, region, public, arn, name):
    # When passed a tag key, tag value this will return a list of InstanceIds that were found.

    try:
        credentials = switching_role(arn, name)
    except Exception as e:
        print("%s"%e)
        credentials = False

    if credentials:
        ec2client = ec2_connection(credentials, region)

        response = ec2client.describe_instances(
            Filters=[
                {
                    'Name': "tag:Name", 
                    'Values': [tagvalue,],
                }
            ]
        )
        instancelist = []

        for reservation in (response["Reservations"]):
            for instance in reservation["Instances"]:
                if (instance['State']['Name']+"\n") == "running\n":
                    if public and 'PublicIpAddress' in instance:
                         for tag in (instance['Tags']):
                            if tag['Key'] == 'Name':
                                instancelist.append({tag['Value']:instance['PublicIpAddress']})
                    else:
                        for tag in (instance['Tags']):
                            if tag['Key'] == 'Name':
                              instancelist.append({tag['Value']:instance['NetworkInterfaces'][0]['PrivateIpAddress']})
        return instancelist
    else:
        instancelist = []
        return instancelist
