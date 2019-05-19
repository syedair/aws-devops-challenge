import uuid
import boto3

class S3Inspect():

    def __init__(self, s3_client, unit):
        self.s3_client = s3_client
        self.unit = unit

    @staticmethod
    def _create_bucket_name(bucket_prefix):
        # The generated bucket name must be between 3 and 63 chars long
        return ''.join([bucket_prefix, str(uuid.uuid4())])

    def _create_bucket(self, bucket_prefix, s3_connection):
        session = boto3.session.Session()
        current_region = session.region_name
        bucket_name = self._create_bucket_name(bucket_prefix)
        bucket_response = s3_connection.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
            'LocationConstraint': current_region})
        print(bucket_name, current_region)
        return bucket_name, bucket_response

    def _read_s3_buckets(self, s3_connection):
        return s3_connection.buckets.all()

    def _list_buckets(self):
        list_buckets = self.s3_client.list_buckets()
        return  list_buckets['Buckets']

    def _show_bucket_details(self, bucket_name, bucket_creationdate):
        print("Bucket Name: {}".format(bucket_name))
        print("Bucket Creation Date: {}".format(bucket_creationdate))



    def _read_files(self, bucket, s3_connection):
        return bucket.objects.all()
