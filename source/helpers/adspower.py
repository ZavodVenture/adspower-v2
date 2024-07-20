import requests
from time import sleep
from threading import Lock

lock = Lock()

API_URL = 'http://localhost:50325/'


def check_adspower():
    try:
        lock.acquire()
        requests.get(API_URL + 'status').json()
        sleep(1)
    except requests.exceptions.ConnectionError:
        raise Exception('The API is unavailable. Check if AdsPower is running')
    else:
        return True
    finally:
        lock.release()


def get_group_id(group_name):
    args = {
        'group_name': group_name
    }

    try:
        lock.acquire()
        r = requests.get(API_URL + 'api/v1/group/list', params=args).json()
        sleep(1)
    except Exception as e:
        raise Exception(f'Couldn\'t find out if the group exists: {str(e)}')
    else:
        if r['code'] != 0:
            raise Exception(r['msg'])
        else:
            if r['data']['list']:
                return r['data']['list'][0]['group_id']
            else:
                return None
    finally:
        lock.release()


def create_group(name):
    try:
        lock.acquire()
        r = requests.post(API_URL + 'api/v1/group/create', json={'group_name': name}).json()
        sleep(1)
    except Exception as e:
        raise Exception(f'An error occurred when sending an AdsPower request: {str(e)}')
    else:
        if r['code'] != 0:
            raise Exception(r['msg'])
        else:
            return r['data']['group_id']
    finally:
        lock.release()


def create_profile(group_id='0', proxy=None):
    if not proxy:
        account_data = {
            'group_id': group_id,
            'user_proxy_config': {
                'proxy_soft': 'no_proxy'
            }
        }
    else:
        host, port, user, password = proxy.split(':')

        account_data = {
            'group_id': group_id,
            'user_proxy_config': {
                'proxy_soft': 'other',
                'proxy_type': 'socks5',
                'proxy_host': host,
                'proxy_port': port,
                'proxy_user': user,
                'proxy_password': password
            }
        }

    try:
        lock.acquire()
        r = requests.post(API_URL + 'api/v1/user/create', json=account_data).json()
        sleep(1)
    except Exception as e:
        raise Exception(f'An error occurred when sending an AdsPower request: {str(e)}')
    else:
        if r['code'] != 0:
            raise Exception(r['msg'])
        else:
            return r['data']['serial_number']
    finally:
        lock.release()


def run_profile(serial_number):
    args = {
        'serial_number': serial_number,
        'ip_tab': 0
    }
    try:
        lock.acquire()
        r = requests.get(API_URL + 'api/v1/browser/start',  params=args).json()
        sleep(1)
    except Exception as e:
        raise Exception(f'An error occurred when sending an AdsPower request: {str(e)}')
    else:
        if r['code'] != 0:
            raise Exception(r['msg'])
        else:
            ws = r["data"]["ws"]["selenium"]
            driver_path = r["data"]["webdriver"]
            return ws, driver_path
    finally:
        lock.release()


def close_profile(serial_number):
    args = {
        'serial_number': serial_number
    }

    try:
        lock.acquire()
        requests.get(API_URL + 'api/v1/browser/stop', params=args)
        sleep(1)
    except Exception as e:
        raise Exception(f'Failed to close the profile: {str(e)}')
    finally:
        lock.release()


def delete_profile(serial_number):
    args = {
        'serial_number': serial_number
    }

    try:
        lock.acquire()
        r = requests.get(API_URL + 'api/v1/user/list', params=args).json()
        sleep(1)
    except Exception as e:
        raise Exception(f'The profile\'s user_id could not be found: {str(e)}')
    finally:
        lock.release()

    if not r['data']['list']:
        raise Exception('The profile to delete was not found')

    user_id = r['data']['list'][0]['user_id']

    try:
        lock.acquire()
        r = requests.post(API_URL + 'api/v1/user/delete', json={'user_ids': [user_id]}).json()
        sleep(1)
    except Exception as e:
        raise Exception(f'Error deleting the profile: {str(e)}')
    finally:
        lock.release()

    if r['code'] != 0:
        raise Exception(r['msg'])


def get_profile_data(serial_number):
    args = {
        'serial_number': serial_number
    }

    try:
        lock.acquire()
        r = requests.get(API_URL + 'api/v1/user/list', params=args).json()
        sleep(1)
    except Exception as e:
        raise Exception(f'Profile could not be found: {str(e)}')
    finally:
        lock.release()

    if not r['data']['list']:
        raise Exception('The profile was not found')

    return r['data']['list'][0]


def get_profiles_in_group(group_id):
    args = {
        'group_id': group_id,
        'page_size': 100
    }

    try:
        lock.acquire()
        r = requests.get(API_URL + 'api/v1/user/list', params=args).json()
        sleep(1)
    except Exception as e:
        raise Exception(f'Profiles could not be found: {str(e)}')
    finally:
        lock.release()

    if not r['data']['list']:
        raise Exception('Profiles was not found')

    return r['data']['list']
