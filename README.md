deepfreeze
==========

A simple command-line utility to upload files to Amazon Glacier.

## Examples ##

Upload a known file using command-line arguments:

    deepfreeze --aws-access-key-id ACCESS_KEY --aws-secret-access-key SECRET_ACCESS_KEY \
        --region AWS_REGION --vault VAULT_NAME filename.txt

Upload a known file using environment variables:

    AWS_ACCESS_KEY_ID="ACCESS_KEY" AWS_SECRET_ACCESS_KEY="SECRET_ACCESS_KEY" \
        AWS_GLACIER_REGION="AWS_REGION" AWS_GLACIER_VAULT="VAULT_NAME" deepfreeze filename.txt

Compress, encrypt, and upload to Glacier in one piped command:

    gzip -c filename.txt | gpg --encrypt --recipient "joe@mail.com" | deepfreeze

On success, output is returned like this:

    $ deepfreeze filename.txt
    Upload Successful. Upload ID:
    TIubeOaLT79H_0hp6EDEUk4IYr4K9w76JG9vj2V1AFAe4OYK8HK1G5lTRQKxuF2M5VKyvVKRbUg7HNpKcC6UGrO27zFfxZeJP7Q-Ds4hKtxbnYO5PxTzfw1768Yy2sJ6dPXAQ06rUw

If you'd like, you can change the output to just the upload ID with the `-o` param:

    $ deepfreeze -o id filename.txt
    TIubeOaLT79H_0hp6EDEUk4IYr4K9w76JG9vj2V1AFAe4OYK8HK1G5lTRQKxuF2M5VKyvVKRbUg7HNpKcC6UGrO27zFfxZeJP7Q-Ds4hKtxbnYO5PxTzfw1768Yy2sJ6dPXAQ06rUw

Upload a compressed and encrypted file to Glacier, then send email with the upload id:

    UPLOAD_ID="$(cat filename.txt | gzip --encrypt --recipient "joe@mail.com" | \
        deepfreeze -o id)"

    mail -s "$(date +%Y/m/%d) Backup Created for filename.txt" \
        -b "joe@mail.com" << END_DOCUMENT
    A Glacier backup has been created for filename.txt on $(date +%Y/%m/%d) at
    $(date +%H:%M:%S).

    The Glacier upload id is $(UPLOAD_ID).
    END_DOCUMENT

## Installation ##

The easiest way to install `deepfreeze` is with `pip`:

    sudo pip install deepfreeze

Alternatively, you can install `deepfreeze` from source:

    git clone git@github.com:rfkrocktk/deepfreeze.git
    cd deepfreeze
    sudo python setup.py install
