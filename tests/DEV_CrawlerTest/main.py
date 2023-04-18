from src.FaceBookCrawler.openfb import FaceBookCrawler
import sys
import shutil

if __name__ == '__main__':

    # Get Account prop
    with open('../../Account.prop', 'r') as f:
        prop = f.read().splitlines()

    if not prop:
        print('No prop file Defined !')
        sys.exit(1)

    if len(prop[0].split('ACCOUNT=')) > 1:
        account = prop[0].split('ACCOUNT=')[1]
    else:
        account = None
    if len(prop[1].split('PASSWORD=')) > 1:
        pwd = prop[1].split('PASSWORD=')[1]
    else:
        pwd = None

    if not shutil.which('chromedriver'):
        exe_path = '../../tools/chromedriver/chromedriver'
    else:
        exe_path = None

    fb = FaceBookCrawler(url='https://www.facebook.com/groups/1260448967306807',
                         userid=account, passwd=pwd,
                         log_config='../../logging.conf',
                         path=exe_path
                         )
    fb.start()
