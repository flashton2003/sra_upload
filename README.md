# upload_to_sra

This code will help you write the submission.xml files you need to upload fastqs to NCBI SRA.

It will also upload them for you using python ftplib, generate the md5 checksums and all that.

The basic stucture is that you have to pass main.py 2 fastqs and a lot of information, this will then write an xml for those fastqs and upload the data. The idea is that you know your meta data source best, so can write a wrapper script to pass that data to main.py.

You need NCBI credentials to successfully upload (ftp username and password), contact the SRA helpdesk for these.

Run python main.py -h for more details.

This code (especially the public release) is in an alpha release state, any problems, raise a github issue or @flashton2003

Also, it assumes you want to upload to Genome Trackr which is for foodborne pathogens only. If you ask nicely, I might look into giving another option.

# Dependencies (tested with below):

python v2.7

lxml v3.2.3
