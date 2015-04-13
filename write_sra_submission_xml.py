__author__ = 'flashton'

from lxml import etree

## see http://stackoverflow.com/questions/863183/python-adding-namespaces-in-lxml

#print lxml_doc
#print dir(lxml_doc)

# write_xml(sra_meta_data, opts, molis_id, args.unique_id, fastq1, fastq2, md5_1, md5_2)


def write_xml(args, md5_1, md5_2):

    #print etree.tostring(root, pretty_print=True)
    NS = 'http://www.w3.org/2001/XMLSchema-instance'
    location_attribute = '{%s}noNamespaceSchemaLocation' % NS
    #root = etree.Element('Submission', attrib={location_attribute:'http://www.ncbi.nlm.nih.gov/viewvc/v1/trunk/submit/public
    # -docs/common/submission.xsd?view=co'})

    root = etree.Element('Submission', schema_version = '2.0')
    description = etree.SubElement(root, 'Description')
    comment = etree.SubElement(description, 'Comment')
    comment.text = 'New Submission. Sample + Experiment + Runs'
    organisation = etree.SubElement(description, 'Organization', role = 'owner', type = 'institute')
    org_name = etree.SubElement(organisation, 'Name', abbr = args.org_abbrev)
    org_name.text = args.organisation

    address = etree.SubElement(organisation, 'Address', postal_code = args.postcode)
    department = etree.SubElement(address, 'Department')
    department.text = args.department
    institution = etree.SubElement(address, 'Institution')
    institution.text = args.institution
    street = etree.SubElement(address, 'Street')
    street.text = args.street
    city = etree.SubElement(address, 'City')
    city.text = args.city
    country = etree.SubElement(address, 'Country')
    country.text = args.country
    contact = etree.SubElement(organisation, 'Contact', email = args.email)
    cont_name = etree.SubElement(contact, 'Name')
    fname = etree.SubElement(cont_name, 'First')
    fname.text = args.name.split(' ')[0]
    lname = etree.SubElement(cont_name, 'Last')
    lname.text = args.name.split(' ')[1]
    date_string = str(args.release_date)
    hold = etree.SubElement(description, 'Hold', release_date = date_string)

    action = etree.SubElement(root, 'Action')
    adddata = etree.SubElement(action, 'AddData', target_db = 'BioSample')
    data = etree.SubElement(adddata, 'Data', content_type = 'XML')
    xml_content = etree.SubElement(data, 'XmlContent')

    #biosample = etree.SubElement(xml_content, 'BioSample', attrib={'xsi':'http://www.w3.org/2001/XMLSchema-instance',
    # location_attribute:'http://www.ncbi.nlm.nih.gov/viewvc/v1/trunk/submit/public-docs/biosample/biosample.xsd?view=co', 'schema_version':'2.0'})

    biosample = etree.SubElement(xml_content, 'BioSample', schema_version = '2.0')
    sampleid = etree.SubElement(biosample, 'SampleId')
    spuid = etree.SubElement(sampleid, 'SPUID', spuid_namespace = args.namespace)
    spuid.text = '%s.biosample' % args.unique_id
    descriptor = etree.SubElement(biosample, 'Descriptor')
    title = etree.SubElement(descriptor, 'Title')
    if args.subspecies != None:
        title.text = '{0} {1} serovar {2} {3}'.format(args.species, args.subspecies, args.serovar, args.unique_id)
    else:
        title.text = '{0} serovar {1} {2}'.format(args.species, args.serovar, args.unique_id)

    organism = etree.SubElement(biosample, 'Organism')
    organism_name = etree.SubElement(organism, 'OrganismName')
    organism_name.text = args.species

    bioproject = etree.SubElement(biosample, 'BioProject')
    primaryid = etree.SubElement(bioproject, 'PrimaryId', db = 'BioProject')
    primaryid.text = args.bioproject
    package = etree.SubElement(biosample, 'Package')

    package.text = args.package

    attributes = etree.SubElement(biosample, 'Attributes')
    attribute = etree.SubElement(attributes, 'Attribute', attribute_name = 'strain')
    attribute.text = args.unique_id
    attribute = etree.SubElement(attributes, 'Attribute', attribute_name = 'collected_by')
    attribute.text = args.collected_by
    collection_date = str(args.collection_date)
    attribute = etree.SubElement(attributes, 'Attribute', attribute_name = 'collection_date')
    attribute.text = collection_date
    attribute = etree.SubElement(attributes, 'Attribute', attribute_name = 'isolation_source')
    attribute.text = args.isolation_source
    attribute = etree.SubElement(attributes, 'Attribute', attribute_name = 'geo_loc_name')
    attribute.text = 'United Kingdom: %s' % args.geo_loc_name
    attribute = etree.SubElement(attributes, 'Attribute', attribute_name = 'lat_lon')
    attribute.text = args.lat_lon
    attribute = etree.SubElement(attributes, 'Attribute', attribute_name = 'serovar')
    attribute.text = args.serovar
    attribute = etree.SubElement(attributes, 'Attribute', attribute_name = 'isolate_name_alias')
    attribute.text = args.unique_id
    if args.st != None:
        attribute = etree.SubElement(attributes, 'Attribute', attribute_name = 'sequence_type')
        attribute.text = args.st

    if args.subspecies != None:
        attribute = etree.SubElement(attributes, 'Attribute', attribute_name = 'sub_species')
        attribute.text = args.subspecies

    if args.contamination != None:
        attribute = etree.SubElement(attributes, 'Attribute', attribute_name = 'potential_contaminant')
        attribute.text = args.contamination

    elif args.contamination == None:
        attribute = etree.SubElement(attributes, 'Attribute', attribute_name = 'potential_contaminant')
        attribute.text = 'None detected'

    if args.isolation_source == 'Human':
        attribute = etree.SubElement(attributes, 'Attribute', attribute_name = 'host')
        attribute.text = 'Homo sapiens'
        attribute = etree.SubElement(attributes, 'Attribute', attribute_name = 'host_disease')
        attribute.text = 'Not available'

    if args.antigenic_structure != None:
        attribute = etree.SubElement(attributes, 'Attribute', attribute_name = 'antigenic_structure')
        attribute.text = args.antigenic_structure

    identifier = etree.SubElement(adddata, 'Identifier')
    spuid_2 = etree.SubElement(identifier, 'SPUID', spuid_namespace = args.namespace)
    spuid_2.text = '%s.biosample' % args.unique_id

    action3 = etree.SubElement(root, 'Action')
    addfiles = etree.SubElement(action3, 'AddFiles', target_db = 'SRA')
    ## need to split the name out of the fastq arg as original is the absolute path
    file1 = etree.SubElement(addfiles, 'File', file_path = args.fastq1.split('/')[-1], md5 = md5_1)
    data_type = etree.SubElement(file1, 'DataType')
    data_type.text = 'generic-data'
    file2 = etree.SubElement(addfiles, 'File', file_path = args.fastq2.split('/')[-1], md5 = md5_2)
    data_type = etree.SubElement(file2, 'DataType')
    data_type.text = 'generic-data'

    attribute = etree.SubElement(addfiles, 'Attribute', name = 'instrument_model')
    attribute.text = 'Illumina HiSeq 2500'
    attribute = etree.SubElement(addfiles, 'Attribute', name = 'library_name')
    attribute.text = args.unique_id
    attribute = etree.SubElement(addfiles, 'Attribute', name = 'library_strategy')
    attribute.text = 'WGS'
    attribute = etree.SubElement(addfiles, 'Attribute', name = 'library_source')
    attribute.text = 'GENOMIC'
    attribute = etree.SubElement(addfiles, 'Attribute', name = 'library_selection')
    attribute.text = 'RANDOM'
    attribute = etree.SubElement(addfiles, 'Attribute', name = 'library_layout')
    attribute.text = 'PAIRED'
    attribute = etree.SubElement(addfiles, 'Attribute', name = 'library_construction_protocol')
    attribute.text = 'Illumina Nextera XT'

    attribute_ref_id = etree.SubElement(addfiles, 'AttributeRefId', name = 'BioProject')
    refid = etree.SubElement(attribute_ref_id, 'RefId')
    primaryid = etree.SubElement(refid, 'PrimaryId')
    primaryid.text = args.bioproject
    attribute_ref_id = etree.SubElement(addfiles, 'AttributeRefId', name = 'BioSample')
    refid = etree.SubElement(attribute_ref_id, 'RefId')
    spuid4 = etree.SubElement(refid, 'SPUID', spuid_namespace = args.namespace)
    spuid4.text = '%s.biosample' % args.unique_id
    identifier = etree.SubElement(addfiles, 'Identifier')
    spuid_5 = etree.SubElement(identifier, 'SPUID', spuid_namespace = args.namespace)
    spuid_5.text = '%s' % args.unique_id
    #print (etree.tostring(root, pretty_print=True))
    return root






