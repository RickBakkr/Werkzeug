from optparse import OptionParser
import yaml
import random
import string
import subprocess

def procedure(version):

    global sessions, filters, counter, peer

    asn = str(peer['as'])
    if version == 4:
        tmpCfg = template_ipv4
        name = "AS" + asn + "_V4"
        index = "ipv4"
    if version == 6:
        tmpCfg = template_ipv6
        name = "AS" + asn + "_V6"
        index = "ipv6"

    # Adjust counter
    if (name not in counter.keys()):
        counter.update({name: 1})
    else:
        counter.update({name: counter.get(name) + 1})
    # Apply variables
    tmpCfg = tmpCfg.replace('|MYAS|', myas)
    tmpCfg = tmpCfg.replace('|ORG|', peer['name'])
    tmpCfg = tmpCfg.replace('|NAME|', get_id(name))
    tmpCfg = tmpCfg.replace('|NEIGHBOR_AS|', asn)
    tmpCfg = tmpCfg.replace('|NEIGHBOR_IP|', str(peer[index]['address']))

    inFilter = "none"
    outFilter = "none"

    if peer[index]['import']['type'] == 'irr' and peer[index]['import']['irr'] is not None:
        if(version == 4):
            v = "V4"
            params = '-A4b'
        else:
            v = "V6"
            params = '-A6b'

        filterName = 'AS' + asn + "_" + v + "_" + get_uuid()
        listName = "PL_" + filterName
        raw_prefixlist = subprocess.check_output([
            'bgpq3', '-S', 'RIPE,APNIC,AFRINIC,ARIN,JPIRR,NTTCOM,RADB,ALTDB,BELL,LEVEL3,RGNET,TC', params,
            peer[index]['import']['irr'], '-l', listName
        ], universal_newlines=True)

        filter = template_filter
        filter = filter.replace('|LIST_DEFINITION|', raw_prefixlist)
        filter = filter.replace('|LIST_NAME|', listName)
        filter = filter.replace('|NAME|', filterName)

        filters += filter + "\n\n\n"

        inFilter = "filter " + filterName

    if peer[index]['import']['type'] == 'filter' and peer[index]['import']['name'] is not None:
        inFilter = "filter " + peer[index]['import']['name']

    if peer[index]['import']['type'] == 'ANY':
        inFilter = "all"

    if peer[index]['export']['type'] == 'filter' and peer[index]['export']['name'] is not None:
        outFilter = "filter " + peer[index]['export']['name']

    if peer[index]['export']['type'] == 'ANY':
        outFilter = "all"

    limitIn = ""
    limitOut = ""
    if "limit" in peer[index]['import'].keys():
        print("Set import limit")
        limitIn = "import limit " + str(peer[index]['import']['limit']) + " action restart;"
    if "limit" in peer[index]['export'].keys():
        print("Set export limit")
        limitOut = "export limit " + str(peer[index]['export']['limit']) + " action restart;"

    tmpCfg = tmpCfg.replace('|IMPORT_POLICY|', inFilter)
    tmpCfg = tmpCfg.replace('|EXPORT_POLICY|', outFilter)

    tmpCfg = tmpCfg.replace('|IMPORT_LIMIT|', limitIn)
    tmpCfg = tmpCfg.replace('|EXPORT_LIMIT|', limitOut)

    password = ""
    if password in peer.keys():
        print("Setting MD5 password")
        password = "password \"" + peer['password'] + "\";"

    tmpCfg = tmpCfg.replace('|MD5_PASSWORD|', password)

    # Generated, append to our config
    print("Append to config")
    sessions += tmpCfg + "\n\n\n"

def get_id(name):
    global counter
    return name + "_" + f"{counter[name]:03d}"

def get_uuid():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(5)]).upper()

peeringFile = "conf/peering.yaml"

dryRun = False

parser = OptionParser()
parser.add_option("-a", "--as-number", dest="myas",
                  help="Your Autonomous Systen Number")
parser.add_option("-c", "--config", dest="peeringFile",
                  help="Path to router specific peering configuration YAML file", metavar="FILE", default=peeringFile)
parser.add_option('--dry-run', default=False, action='store_true', dest="dryRun", help="Does not write generated configs, just outputs to screen")
(options, args) = parser.parse_args()

if not options.myas:   # if filename is not given
    parser.error('You have not provided us with any ASN. Use -a 65000 or --as-number 65000')

myas = options.myas
peeringFile = options.peeringFile
dryRun = options.dryRun

print("-------- [ WERKZEUG by Rick Bakker ] --------")
print("Environment:")
print("ASN: " + str(myas))
print("Configuration file: " + str(peeringFile))
if(dryRun):
    print("RUNNING IN DRY-RUN MODE - WILL OUTPUT CONFIG HERE, NOT WRITE TO OUTPUT DIR.")

print("")
with open("templates/ipv4.tpl", "r") as file:
    template_ipv4 = file.read()

with open("templates/ipv6.tpl", "r") as file:
    template_ipv6 = file.read()

with open("templates/filter.tpl", "r") as file:
    template_filter = file.read()

with open(peeringFile, "r") as file:
    raw = file.read()
    data = yaml.safe_load(raw)

counter = {}

filters = ""
sessions = ""

for peer in data:

    print('--- Generating session/filters for AS' + str(peer['as']) + ' (' + peer['name'] + ') ---')
    if peer['ipv4'] is not None:
        print("Setting up IPv4 session")
        procedure(4)

    if peer['ipv6'] is not None:
        print("Setting up IPv6 session")
        procedure(6)

if dryRun:
    print("SESSIONS:")
    print(sessions)
    print("FILTERS:")
    print(filters)
else:
    with open("out/sessions.conf", "w") as myfile:
        myfile.write(sessions)
    with open("out/filters.conf", "w") as myfile:
        myfile.write(filters)
