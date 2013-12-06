#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import argparse
import json
import boto
import boto.glacier
import os
import sys
import select
from boto.glacier.exceptions import UnexpectedHTTPResponseError


class ValidationException(Exception):
    pass


class DeepFreeze(object):

    def __init__(self, arguments):
        self.arguments = arguments
        self.upload_id = None
        self.error_message = None

    def validate(self):
        self._validate_access_key()
        self._validate_secret_key()
        self._validate_region()
        self._validate_vault()
        self._validate_file()

    def _validate_access_key(self):
        if self.arguments.aws_access_key_id is None:
            raise ValidationException("Unable to determine the AWS access key id.")

    def _validate_secret_key(self):
        if self.arguments.aws_secret_access_key is None:
            raise ValidationException("Unable to determine the AWS secret access key.")

    def _validate_vault(self):
        if self.arguments.vault is None:
            raise ValidationException("Unable to determine the Glacier vault name.")

    def _validate_region(self):
        if self.arguments.region not in map(lambda region: region.name, boto.glacier.regions()):
            raise ValidationException("Unknown Glacier region '%s'." % (self.arguments.region,))

    def _validate_file(self):
        # if there's no file passed and no STDIN
        is_stdin = self.arguments.file == sys.stdin
        stdin_has_data = bool(select.select([sys.stdin], [], [], 0.0)[0])

        # if there's no file argument and STDIN has no data
        if is_stdin and not stdin_has_data:
            raise ValidationException("No file passed and no data from standard input.")

        # if there IS a file argument and it's empty
        if not is_stdin and os.fstat(self.arguments.file.fileno()).st_size == 0:
            raise ValidationException("Input file must not be empty.")

    def is_valid(self):
        try:
            self.validate()
            return True
        except ValidationException as e:
            self.error_message = e.args[0]
            return False

    def upload(self):
        if not self.is_valid():
            raise ValidationException(self.error_message)

        # create the connection to AWS
        connection = boto.connect_glacier(
            aws_access_key_id=self.arguments.aws_access_key_id,
            aws_secret_access_key=self.arguments.aws_secret_access_key,
            region_name=self.arguments.region,
        )

        # get the target vault
        vault = connection.get_vault(self.arguments.vault)

        # set uploaded object id
        self.upload_id = vault.create_archive_from_file(
            file_obj=self.arguments.file,
            description=self.arguments.description if self.arguments.description else None
        )

        # return the upload id
        return self.upload_id


def cli():
    """
    Does the things!
    """
    parser = argparse.ArgumentParser(
        prog="deepfreeze",
        description="A simple command-line client for uploading files to Amazon Glacier."
    )

    parser.add_argument('--aws-access-key-id', type=str, default=os.environ.get('AWS_ACCESS_KEY_ID'),
                        help="The AWS access key id with which to authenticate. If not specified, it will default to"
                             "the value of the AWS_ACCESS_KEY_ID environment variable.")
    parser.add_argument('--aws-secret-access-key', type=str, default=os.environ.get('AWS_SECRET_ACCESS_KEY'),
                        help="The AWS secret access key with which to authenticate. If not specified, it will default "
                             "to the value of the AWS_SECRET_ACCESS_KEY environment variable.")
    parser.add_argument('-r', '--region', type=str, default=os.environ.get('AWS_GLACIER_REGION') or 'us-east-1',
                        help="The AWS region to use. If not specified, it will default to the value of the "
                             "AWS_REGION environment variable, or will use the default region (us-east-1).")
    parser.add_argument('-v', '--vault', type=str, default=os.environ.get('AWS_GLACIER_VAULT'),
                        help="The AWS Glacier vault to use. If not specified, it will default to the value of the "
                             "AWS_GLACIER_VAULT environment variable.")
    parser.add_argument('-o', '--output-type', type=str, default='full', choices=('full', 'id'),
                        help="The output type for the script. If 'full', verbose output will be emitted. If 'id', "
                             "only the Glacier id of the uploaded file will be emitted.")
    parser.add_argument('-d', '--description', type=str,
                        help="The description to attach to the uploaded file to Glacier.")
    parser.add_argument('file', nargs="?", type=argparse.FileType('r'), default=sys.stdin,
                        help="The file to be uploaded to Glacier. If not specified, will try to read from STDIN.")

    args = parser.parse_args()

    # create the deep freezer and get goin'
    df = DeepFreeze(args)

    if not df.is_valid():
        sys.stderr.write("Error: %s\n" % (df.error_message,))
        sys.stderr.flush()
        sys.exit(1)

    try:
        upload_id = df.upload()

        if args.output_type == 'full':
            print('Upload Successful. Upload ID: \n%s' % (upload_id,))
        else:
            # sparse output, just return the upload id:
            print(upload_id)

        sys.exit(0)
    except UnexpectedHTTPResponseError as e:
        sys.stderr.write("Error: %s - %s\n" % (e.code, json.loads(e.body).get('message'),))
        sys.stderr.flush()
        sys.exit(1)


if __name__ == "__main__":
    cli()