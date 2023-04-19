from src.FaceBookCrawler.openfb import FaceBookCrawler
import sys
import shutil

if __name__ == '__main__':

    # Get Account prop
    with open('Account.prop', 'r') as f:
        prop = f.read().splitlines()

    if not prop:
        print('No prop file Defined !')
        sys.exit(1)

    properties = {}
    for p in prop:
        splited_p = p.split('=')
        properties[splited_p[0].upper()] = splited_p[1]

    if not shutil.which('chromedriver'):
        exe_path = 'tools/chromedriver/chromedriver'
    else:
        exe_path = 'tools/chromedriver/chromedriver'

    fb = FaceBookCrawler(url='https://www.facebook.com/groups/1260448967306807',
                         userid=properties.get('ACCOUNT'),
                         passwd=properties.get('PASSWORD'),
                         log_config='logging.conf',
                         path=exe_path
                         )
    fb.COMMENT_DEEP_COUNT = 0
    fb.start()
