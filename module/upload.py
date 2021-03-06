#!/usr/bin/env python

from   mimetypes import MimeTypes
import cookielib
import mechanize
import os
import re
import sys
import urllib
import urllib2

################################################################################

filenameArch16n    = 'english.0.properties'
filenameCss        = 'ui_styling.css'
filenameDataSchema = 'data_schema.xml'
filenameUiLogic    = 'ui_logic.bsh'
filenameUiSchema   = 'ui_schema.xml'
filenameValidation = 'validation.xml'

filenames = [
        filenameArch16n,
        filenameCss,
        filenameDataSchema,
        filenameUiLogic,
        filenameUiSchema,
        filenameValidation]

username = 'faimsadmin@intersect.org.au'
password = 'Pass.123'

server = 'dev'
url    = 'http://%s.fedarch.org' % server

################################################################################
doDelete = len(sys.argv) > 1 and sys.argv[1] == '--rm'

# The module location can be set manually or be determined automatically
if len(sys.argv) > 1 and sys.argv[1] != '--rm':
    # Set module location from manually-given argument
    moduleLocation = sys.argv[1]
    moduleLocation = os.path.abspath(moduleLocation)
else:
    # Set module location to that of this script
    moduleLocation = os.path.realpath(__file__)
    moduleLocation = os.path.dirname(moduleLocation)
# Determine module name
moduleName = moduleLocation.split(os.sep)
moduleName = moduleName[-1]

# Check that all the given paths really exist
if not os.path.exists(moduleLocation):
    print 'ERROR: given module location does not exist'
    exit()

isMissing = False
for f in filenames:
    if not os.path.exists(moduleLocation + os.sep + f):
        print 'ERROR: Cannot find %s' % f
        isMissing = True
if isMissing:
    exit()

# Initialisation of `magic` module
mime = MimeTypes()
mime.add_type('text/plain', '.bsh')
mime.add_type('text/plain', '.properties')

# Make browser
br = mechanize.Browser()

# Initialisation of `mechanize` module (Some stuff I copied from Stack Overflow)
cookiejar = cookielib.LWPCookieJar()
br.set_cookiejar      (cookiejar)
br.set_handle_gzip    (True)
br.set_handle_equiv   (True)
br.set_handle_gzip    (True)
br.set_handle_redirect(True)
br.set_handle_referer (True)
br.set_handle_robots  (False)

################################################################################

def addFile(br, filename, inputName):
    fullFilename = moduleLocation + os.sep + filename
    mimetype     = mime.guess_type(filename)
    mimetype     = mimetype[0]

    br.form.add_file(open(fullFilename), mimetype, filename, name=inputName)

def addFiles(br, doUploadDataSchema):
    addFile    (br, filenameArch16n    , 'project_module[arch16n]')
    addFile    (br, filenameCss        , 'project_module[css_style]')
    if doUploadDataSchema:
        addFile(br, filenameDataSchema , 'project_module[data_schema]')
    addFile    (br, filenameUiLogic    , 'project_module[ui_logic]')
    addFile    (br, filenameUiSchema   , 'project_module[ui_schema]')
    addFile    (br, filenameValidation , 'project_module[validation_schema]')

def login(br):
    # Get login form and fill it out
    print 'Working on module with the name "%s"...' % moduleName
    print

    print 'Downloading login form...'
    res = br.open(url)

    br.select_form(nr=0)
    br['user[email]']    = username
    br['user[password]'] = password

    # Submit yer good ol' form
    print 'Submitting login form...'
    print
    res = br.submit()

def deleteModule(br):
    print 'Downloading delete form...'
    # Try clicking on link to module config page
    try:
        linkText = moduleName
        res      = br.follow_link(text_regex=linkText)
    except:
        print 'Cannot delete module; does not exist. Exiting.'
        return

    # Get URL to delete module
    linkText = 'Delete Module'
    req      = br.click_link(text_regex=linkText)
    url      = req.get_full_url()

    # Search for the stupid CSRF token
    token    = res.get_data()
    token    = re.search('"([^"]+)"\s+name="csrf-token"', token)
    token    = token.group(1)
    params   = {
            u'_method'            : 'delete',
            u'authenticity_token' : token
    }
    data = urllib.urlencode(params)

    # POST the deletion request
    try:
        br.open(url, data)
        print 'All done!'
    except:
        print 'Cannot delete module. Exiting.'

def uploadModule(br):
    # Determine if module's already been uploaded. (Yes, I know I've misused the
    # try-except statement.)
    print 'Downloading update/create form...'
    try:
        # The module's already been uploaded
        linkText = moduleName
        res      = br.follow_link(text_regex=linkText)

        linkText = 'Edit Module'
        res      = br.follow_link(text_regex=linkText)

        print 'Submitting update form...'
        print
        br.select_form(nr=0)
        addFiles(br, doUploadDataSchema=False)
        res = br.submit()
    except:
        # We need to create a new module
        linkText = 'Create Module'
        res      = br.follow_link(text_regex=linkText)

        print 'Submitting create form...'
        print
        br.select_form(nr=0)
        br['project_module[name]'] = moduleName
        addFiles(br, doUploadDataSchema=True)
        res = br.submit()
        res = res.get_data()
        reg = '<span class="help-inline">([^<]+)</span>'
        doesMatch = re.search(reg, res)
        Ms = re.finditer(reg, res)
        if not doesMatch:
            print 'All done!'
            return
        print 'Completed with errors:'
        for m in Ms:
            print '  - ', m.group(1)


################################################################################
login(br)
if doDelete:
    deleteModule(br)
else:
    uploadModule(br)
