from time import sleep
import picamera
import os
import yaml
import boto3
from datetime import datetime

# testing
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

# photo props
file_name = datetime.now().strftime("%Y-%m-%d %H-%M-%S") + " " + cfg['image_settings']['file_name']

# camera setup
camera = picamera.PiCamera()
camera.resolution = (cfg['image_settings']['horizontal_res'], cfg['image_settings']['vertical_res'])
camera.awb_mode = cfg['image_settings']['awb_mode']

# camera warm-up time
sleep(2)

print('[debug] Taking photo and saving to path ' + file_name)

# Take Photo
camera.capture(file_name)

print('[debug] Uploading ' + file_name + ' to s3')

# Upload to S3
session = boto3.Session(
    aws_access_key_id=cfg['s3']['access_key_id'],
    aws_secret_access_key=cfg['s3']['secret_access_key']
)
s3 = session.client('s3')
#s3.upload_file(file_name, bucket, object_name)
with open(file_name, "rb") as f:
    s3.upload_fileobj(f, cfg['s3']['bucket_name'], file_name)

# Cleanup
if os.path.exists(file_name):
    os.remove(file_name)
