###############################
# Script to Demo S3 AWS CLI
# SDEV400
###############################
# Make a project 2 bucket
aws s3 mb s3://edu.umuc.sdev400.robertson.project22020
# List the current buckets
aws s3 ls
# Copy some images to folders
# Note I already uploaded the Images to Cloud9
aws s3 cp CAM00190.jpg s3://edu.umuc.sdev400.robertson.project22020/2019/
aws s3 cp CAM00198.jpg s3://edu.umuc.sdev400.robertson.project22020/2019/
# copy a file from one folder to another
aws s3 cp s3://edu.umuc.sdev400.robertson.project22020/2019/CAM00190.jpg
s3://edu.umuc.sdev400.robertson.project1/2019/
# Check the folders
aws s3 ls s3://edu.umuc.sdev400.robertson.project22020/ --recursive --summarize
aws s3 ls s3://edu.umuc.sdev400.robertson.project1/ --recursive --summarize