import boto3


def list_instances(tagvalue, region, public):
    # When passed a tag key, tag value this will return a list of InstanceIds that were found.
    try:
        ec2client = boto3.client('ec2', region_name=region)

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
    except Exception as e:
        print("%s"%e)
        instancelist = []
        return instancelist