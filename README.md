# lambda-bahaimedia-distribute
Distribute files to regional s3 buckets after getting an upload in any one bucket

This function copies files uploaded in one s3 region to all other s3 regions. It captures and replicates the 'upload' action. 
In the case of a 'move' action files will not automatically be replicated and a cron job is triggered server-side that watches
for file moves and initiates a sync action with the US bucket. Less frequently, the US bucket will sync with all overseas buckets
so eventually this file that was moved will be everywhere. We don't need it to be everywhere immediately because of 
lambda-edge-file-redirect.
