# lambda-bahaimedia-distribute
Distribute files to regional s3 buckets after getting an upload in any one bucket

This function copies files uploaded in one s3 region to all other s3 regions. It captures and replicates the 'upload' action. 
In the case of a 'move' action files will not automatically be replicated and a cron job is triggered server-side that watches
for file moves and initiates a sync action with the US bucket. Less frequently, the US bucket will sync with all overseas buckets
so eventually this file that was moved will be everywhere. We don't need it to be everywhere immediately because of 
lambda-edge-file-redirect.

Note that each region where an origin bucket exists will also have a local copy of this lambda function and lambda-bahaimedia-delete-s3.

s3 buckets have event notifications tied to Amazon SNS which goes like this:
  1. Event copyReplication or event deleteReplication triggers SNS topic
  2. SNS topic has 1 subscription per region where files are going to be copied whose endpoint is this function or lambda-bahaimedia-delete-s3

Eg, on the US server in an SNS subscription for the distribute function, the endpoints are:
  1. Region 1 distribute lambda
  2. Region 2 distribute lambda
  3. Region 3 distribute lambda  
  
We avoid an infinite loop of files being copied because this function is triggered only on 'upload' and not on 'copy' actions, the original
bucket sees an upload action but all other buckets when receiving the file see it as a copy/receipt action and the function is not 
triggered in a loop. This also creates the need to especially watch for and somewhat manually replicate files that are moved by
mediawiki since that replicates the copy action and those files would not be distributed by this function. See lambda-edge-file-redirect
for how we deal with this.
  
