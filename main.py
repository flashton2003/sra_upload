__author__ = 'flashton'

import argparse
import write_sra_submission_xml
import upload_to_ftp
import datetime
from lxml import etree
import os
import subprocess
'''
How to troubleshoot git https

http://mark.koli.ch/pushing-to-an-http-git-remote-ref-on-ubuntu-1004-lts-with-git-1704-403-inforefs
'''


def get_md5(fastq1, fastq2):
    md5s = []
    fastqs = [fastq1, fastq2]
    for fastq in fastqs:
        process = subprocess.Popen(['md5sum', fastq], stdout=subprocess.PIPE)
        stdout = process.communicate()
        md5s.append(stdout[0].split()[0])
    return md5s[0], md5s[1]

def upload_to_sra(args):
    xml_handle = args.outdir + '/%s.submission.init.xml' % (args.unique_id)
    final_xml_handle = args.outdir + '/%s.submission.xml' % (args.unique_id)
    md5_1, md5_2 = get_md5(args.fastq1, args.fastq2)
    root = write_sra_submission_xml.write_xml(args, md5_1, md5_2)
    xml_string = etree.tostring(root, pretty_print=True)
    print xml_handle
    with open(xml_handle, 'w') as fo:
        fo.write(xml_string)
    with open(xml_handle, 'r') as fi:
            with open(final_xml_handle, 'w') as fo:
                for line in fi.readlines():
                    stripped_line = line.strip()
                    if stripped_line.startswith('<BioSample schema_version="2.0" xsi="http://www.w3.org/2001/XMLSchema-instance"'):
                        fo.write( '          <BioSample schema_version="2.0" '
                                  'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                                  'xsi:noNamespaceSchemaLocation="http://www.ncbi.nlm.nih.gov/viewvc/v1/trunk/submit'
                                  '/public-docs/biosample/biosample.xsd?view=co">\n')
                    else:
                        fo.write(line)
    os.system('rm -rf %s/%s.submission.init.xml' % (args.unique_id, args.outdir))

    upload_to_ftp.upload_to_ftp(args, final_xml_handle)


def run_command(args):
    if args.command == 'sra_upload':
        upload_to_sra(args)


def parse_args():
    today = datetime.date.today()
    parser = argparse.ArgumentParser(prog = 'sra_upload_kit',
                                     description='The function of this script is to take a sequencing ' \
                                                'sample name, get meta-data on them from GDW and write xml to submit to SRA.')
    parser.add_argument('-v', '--version', help = 'installed version', action = 'version', version = 'alpha')
    subparsers = parser.add_subparsers(title='[sub-commands]', dest='command')
    parser_sra_upload = subparsers.add_parser('sra_upload', help = 'take a shit load of args and upload some data')

    ## data arguments
    parser_sra_upload.add_argument('--fastq1', action = 'store', help = 'First read of paired fastq - REQUIRED', required = True)
    parser_sra_upload.add_argument('--fastq2', action = 'store', help = 'Second read of paired fastq - REQUIRED', required = True)
    parser_sra_upload.add_argument('--test_prod', action = 'store', help = 'Either <Test> or <Production> Whether to '
                                                                     'upload to Test or Production - REQUIRED',required = True)
    parser_sra_upload.add_argument('--force', action = 'store', default = 'N', help = 'Force to run, even if submit.ready '
                                                                                      'already exists')
    parser_sra_upload.add_argument('--release_date', action = 'store', default = today + datetime.timedelta(days = 1),
                        help = 'Release date - default is tomorrow')
    parser_sra_upload.add_argument('--outdir', action = 'store', required = True, help = 'Where do you want the scripts to be '
                                                                                         'written to - REQUIRED')
    parser_sra_upload.add_argument('--unique_id', action = 'store', required = True, help = 'The unique identifier for this '
                                        'strain. Must not have been used in your namespace before. Will be publically visible. - REQUIRED')

    ## let's talk about you
    parser_sra_upload.add_argument('--namespace', action = 'store', default = 'your NCBI namespace', help = 'Your SPUID namespace')
    parser_sra_upload.add_argument('--email', action = 'store', default = 'you@place.com', help = 'Your email')
    parser_sra_upload.add_argument('--name', action = 'store', default = 'Your Name', help = 'Your name')
    parser_sra_upload.add_argument('--organisation', action = 'store', default = 'Your work', help = 'Your organisation')
    parser_sra_upload.add_argument('--department', action = 'store', default = 'Your Department',
                        help = 'Your department')
    parser_sra_upload.add_argument('--institution', action = 'store', default = 'Your Institution', help = 'Your '
                                                                                                                'institution')
    parser_sra_upload.add_argument('--street', action = 'store', default = 'Your Address', help = 'Your institution '
                                                                                                         'street address')
    parser_sra_upload.add_argument('--city', action = 'store', default = 'Your city', help = 'Your institution city')
    parser_sra_upload.add_argument('--country', action = 'store', default = 'Your country', help = 'Your institution country')
    parser_sra_upload.add_argument('--org_abbrev', action = 'store', default = 'Your abbrev', help = 'Your organisation abbreviation')
    parser_sra_upload.add_argument('--postcode', action = 'store', default = 'Your postcode', help = 'Your organisation postcode')

    ## lets talk about NCBI and your credentials

    parser_sra_upload.add_argument('--ncbi_username', action = 'store', default = 'uname', help = 'Your NCBI username')
    parser_sra_upload.add_argument('--ncbi_password', action = 'store', default = 'password', help = 'Your NCBI password')
    parser_sra_upload.add_argument('--ncbi_ftp_address', action = 'store', default = 'ncbi.ftp',
                                   help = 'NCBI ftp address')

    ## Bioproject level info
    parser_sra_upload.add_argument('--bioproject', action = 'store', default = 'PRJNAXXXXXXX', help = 'Your BioProject id - '
                                                                                                     'you have one right?')

    ## Biosample level info
    parser_sra_upload.add_argument('--isolate_name_alias', action = 'store', help = 'Short alias for the sample - REQUIRED', required = True)
    parser_sra_upload.add_argument('--species', action = 'store', help = 'The primary species identified in the sample')
    parser_sra_upload.add_argument('--subspecies', action = 'store', default = None,
                                   help = 'The primary subspecies identified in the sample')
    parser_sra_upload.add_argument('--serovar', action = 'store', help = 'The serovar identified in the sample')
    parser_sra_upload.add_argument('--isolation_source', action = 'store', help = 'Where was the sample isolate from?')
    parser_sra_upload.add_argument('--package', action = 'store', help = 'Enter Pathogen.env.1.0 if environmental, Pathogen.cl.1.0 if clinical', required = True)
    parser_sra_upload.add_argument('--host', action = 'store', help = 'Taxonomic name of species from which this isolate was '
                                                                      'taken.')
    parser_sra_upload.add_argument('--host_disease', action = 'store', default = None, help = 'What kind of disease was the '
                                                                    'isolate associated with? Gastroenteritis, invasive, etc.')
    parser_sra_upload.add_argument('--antigenic_structure', action = 'store', default = None, help = 'The antigenic structure '
                                                                                        'of the organism, e.g. 4, 5, 12:i:-')
    parser_sra_upload.add_argument('--collected_by', action = 'store', default = 'You?', help = 'Who was the sample collected by')
    parser_sra_upload.add_argument('--collection_date', action = 'store', help = 'What date was the sample collected? '
                                                                                       'ISO 8601 please')
    parser_sra_upload.add_argument('--geo_loc_name', action = 'store', help = 'Where was the sample collected from. Format '
                            'has to conform to INSDC standards http://www.insdc.org/documents/country-qualifier-vocabulary')
    parser_sra_upload.add_argument('--lat_lon', action = 'store', default= 'Missing', help = 'Latitude and longitude')
    parser_sra_upload.add_argument('--st', action = 'store', default = None, help = 'What sequence type is the isolate')
    parser_sra_upload.add_argument('--contamination', action = 'store', help = 'Any contaminating species that were identified')

    ## lets talk about your sequencing gubbins
    parser_sra_upload.add_argument('--total_length', action = 'store', default = '200', help = 'Sum of read lengths')
    parser_sra_upload.add_argument('--instrument_model', action = 'store', default = 'Illumina HiSeq 2500', help = 'Sequencer '
                                                                                                                   'used.')
    parser_sra_upload.add_argument('--library_strategy', action = 'store', default = 'WGS', help = 'library_strategy')
    parser_sra_upload.add_argument('--library_source', action = 'store', default = 'GENOMIC', help = 'Library source')
    parser_sra_upload.add_argument('--library_selection', action = 'store', default = 'Random', help = 'library_selection')
    parser_sra_upload.add_argument('--library_layout', action = 'store', default = 'Paired', help = 'Sequencer used.')
    parser_sra_upload.add_argument('--library_construction_protocol', action = 'store', default = 'Illumina Nextera XT',
                        help = 'library_construction_protocol')

    ## under development in the release branch
    # parser_get_results = subparsers.add_parser('get_results_of_upload', help = 'check upload of sra')


    args = parser.parse_args()
    return args





if __name__ == '__main__':
    args = parse_args()
    run_command(args)




# def old_main():
#     sra_meta_data = sra_meta_data.SraMetaData()
#     sra_meta_data = get_metadata.get_gdw_data(opts.sample, sra_meta_data)
#     ## isn't handling more than one res from the glob
#     fastqs = core_utils.get_fastqs(folder)
#     fastqs = sorted(fastqs)
#     fastq1 = fastqs[0].split('/')[-1]
#     fastq2 = fastqs[1].split('/')[-1]
#
#     st = get_metadata.get_st(opts.root_dir, folder, opts.sample)
#     sra_meta_data.st = st
#     contamination = get_metadata.get_kmer_result(folder, sra_meta_data)
#     if len(contamination) > 0:
#         sra_meta_data.contamination = '; '.join(contamination)
#     m = re.search('ailed', sra_meta_data.st)
#     if m:
#         print 'ST is failed'
#         sys.exit()
#     else:
#         molis_id = core_utils.extract_molis(opts.sample)
#         sequencing_id = opts.sample.split('_')[0]
#         if molis_id != None:
#             xml_handle = '%s/submission.init.xml' % (folder)
#             root = write_sra_submission_xml.write_xml(sra_meta_data, opts, molis_id, sequencing_id, fastq1, fastq2, md5_1, md5_2)
#             xml_string = etree.tostring(root, pretty_print=True)
#             with open(xml_handle, 'w') as fo:
#                 fo.write(xml_string)
#             xml_final_handle = '%s/submission.xml' % (folder)
#             with open(xml_handle, 'r') as fi:
#                 with open(xml_final_handle, 'w') as fo:
#                     for line in fi.readlines():
#                         stripped_line = line.strip()
#                         if stripped_line.startswith('<BioSample schema_version="2.0" xsi="http://www.w3.org/2001/XMLSchema-instance"'):
#                             fo.write( '          <BioSample schema_version="2.0" '
#                                       'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
#                                       'xsi:noNamespaceSchemaLocation="http://www.ncbi.nlm.nih.gov/viewvc/v1/trunk/submit/public-docs/biosample/biosample.xsd?view=co">\n')
#                         else:
#                             fo.write(line)
#             os.system('rm -rf %s/submission.init.xml' % folder)
#             upload_to_ftp.upload_to_ftp(fastqs, xml_final_handle, molis_id, sequencing_id, folder, opts.test_prod)
#             print str(sequencing_id) + 'has finished uploading'
#         else:
#             print 'Sample name %s does not appear to contain a molis id' % (opts.sample)
    ## after get ST, need to check that ST has been assigned in as a condition of upload


# if os.path.exists('%s/submit.ready' % folder):
#     if opts.force == 'Y':
#         main()
#     else:
#         print 'submit.ready already exists'
#         ## should replace this with query ftp for results - although how to solve the date issue?
#         pass
# else:
#     main()




