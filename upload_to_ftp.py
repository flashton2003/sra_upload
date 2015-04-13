__author__ = 'flashton'

import ftplib
import os

'''
see http://stackoverflow.com/questions/2911754/how-to-upload-binary-file-with-ftplib-in-python
'''

def upload_to_ftp(args, xml_handle):
    ftp = ftplib.FTP('ncbi-ftp')
    ftp.login(user=args.ncbi_username, passwd=args.ncbi_password)
    #ftp.retrlines('LIST')
    #print str(today)
    ftp.cwd(args.test_prod)
    try:
        ftp.cwd(args.unique_id)
    except ftplib.error_perm:
        ftp.mkd(args.unique_id)
        ftp.cwd(args.unique_id)
    xml_upload_cmd = 'STOR submission.xml'
    ftp.storlines(xml_upload_cmd, open(xml_handle, 'r'))
    fastqs = [args.fastq1, args.fastq2]
    for fq in fastqs:
        fq_upload_cmd = 'STOR %s' % fq.split('/')[-1]
        ftp.storbinary(fq_upload_cmd, open(fq, 'rb'))
    # os.system('touch %s/submit.ready' % args.outdir)
    # submission_ready_cmd = 'STOR submit.ready'
    # ftp.storlines(submission_ready_cmd, open('%s/submit.ready' % args.outdir))
    ftp.quit()