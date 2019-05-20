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

    # def _read_s3_buckets(self, s3_connection):
    #     return s3_connection.buckets.all()

    def _list_buckets(self):
        list_buckets = self.s3_client.list_buckets()
        return  list_buckets['Buckets']

    def _show_bucket_details(self, bucket_name, bucket_creationdate):
        print("Bucket Name: {}".format(bucket_name))
        print("Bucket Creation Date: {}".format(bucket_creationdate))

    def _print_total_size(self, total_size):
        if self.unit == 'b':
            print ('s3 size = %.3f B' % (total_size))
        elif self.unit == 'kb':
            print ('s3 size = %.3f KB' % (total_size/1024))
        elif self.unit == 'mb':
            print ('s3 size = %.3f MB' % (total_size/1024/1024))
        elif self.unit == 'gb':
            print ('s3 size = %.3f GB' % (total_size/1024/1024/1024))
        else:
            print ("Warning: Unknown <unit> : {}".format(self.unit))
            print ('s3 size = %.3f B' % (total_size))
    def _get_matching_s3_keys(self, bucket, prefix='', suffix=''):
        """
        Generate the keys in an S3 bucket.

        :param bucket: Name of the S3 bucket.
        :param prefix: Only fetch keys that start with this prefix (optional).
        :param suffix: Only fetch keys that end with this suffix (optional).
        """
        # s3 = boto3.client('s3')
        s3 = self.s3_client
        kwargs = {'Bucket': bucket}

        # If the prefix is a single string (not a tuple of strings), we can
        # do the filtering directly in the S3 API.
        if isinstance(prefix, str):
            kwargs['Prefix'] = prefix

        while True:

            # The S3 API response is a large blob of metadata.
            # 'Contents' contains information about the listed objects.
            resp = s3.list_objects_v2(**kwargs)
            for obj in resp['Contents']:
                # print (obj)
                key = obj['Key']
                size = obj['Size']
                storage_class = obj['StorageClass']
                if key.startswith(prefix) and key.endswith(suffix):
                    yield key, size, storage_class

            # The S3 API is paginated, returning up to 1000 keys at a time.
            # Pass the continuation token into the next response, until we
            # reach the final page (when this field is missing).
            try:
                kwargs['ContinuationToken'] = resp['NextContinuationToken']
            except KeyError:
                break
