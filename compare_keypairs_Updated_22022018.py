import boto3
import boto.ec2

n=str()
count=0
Found=False  #Bool to track duplicates


print ( "Enter cred for account X" )
key="xxxx"
secret="xxxx"

client=boto3.client('ec2',aws_access_key_id=key,aws_secret_access_key=secret)
ec2_conn1=boto.ec2.connect_to_region(region=region_name,aws_access_key_id=key,aws_secret_access_key=secret)
live_keypairs1=dict()
live_keypairs2=dict()
temp_keys1=dict()
temp_keys1=client.describe_key_pairs()

for host, value in temp_keys1.items():
	for n in value:
		if 'KeyName' in n:
			live_keypairs1.update({n['KeyName']:n['KeyFingerprint']})


#print live_keypairs1


print ( "Enter cred for account Y" )

key="xxx"
secret="xxxx"

client=boto3.client('ec2',aws_access_key_id=key,aws_secret_access_key=secret)
ec2_conn2=boto.ec2.connect_to_region(region=region_name,aws_access_key_id=key,aws_secret_access_key=secret)
temp_keys2=client.describe_key_pairs()

for host, value in temp_keys2.items():
        for n in value:
                if 'KeyName' in n:
                        live_keypairs2.update({n['KeyName']:n['KeyFingerprint']})



for key1,value1 in live_keypairs1.items():
	for key2,value2 in live_keypairs2.items():
		if value1 == value2:
			reservations1=ec2_conn1.get_all_instances()
			print "\n Instances present in account X using %s are : \n"%(key1), [s.id for res in reservations1 for s in res.instances if s.key_name == key1]
			reservations2=ec2_conn2.get_all_instances()
			print "\n Instances present in account Y using %s are : \n"%(key2), [s.id for res in reservations2 for s in res.instances if s.key_name == key2]
			Found=True 

if not Found:
	print "No duplicate key pair finger print found"