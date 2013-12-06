deepfreeze
==========

A simple command-line utility to upload files to Amazon Glacier

## Examples ##

Upload a known file using command-line arguments:

    deepfreeze --aws-access-key-id ACCESS_KEY --aws-secret-access-key SECRET_ACCESS_KEY \
        --region AWS_REGION --vault VAULT_NAME filename.txt

Upload a known file using environment variables:

    AWS_ACCESS_KEY_ID="ACCESS_KEY" AWS_SECRET_ACCESS_KEY="SECRET_ACCESS_KEY" \
        AWS_REGION="AWS_REGION" AWS_GLACIER_VAULT="VAULT_NAME" deepfreeze filename.txt

Compress, encrypt, and upload to Glacier in one piped command:

    gzip -c myfile | gpg --encrypt --sign --recipient "destemail@mail.com" | deepfreeze

## Installation ##

Two options exist for
