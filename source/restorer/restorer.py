from source.helpers import adspower, bypass
from configparser import ConfigParser
from progress.bar import Bar
from threading import Thread
from source.helpers.profileWorker import Worker, WorkerException
from time import sleep
import re

config = ConfigParser()
config.read('config.ini')

MAX_THREADS = int(config['settings']['threads'])
CURRENT_THREADS = 0

PROFILE_NUMBER = int(config['settings']['profile_number'])
FIRST_PROFILE = int(config['settings']['first_profile'])

DO_METAMASK = int(config['settings']['DO_METAMASK'])
DO_KEPLR = int(config['settings']['DO_KEPLR'])
DO_PHANTOM = int(config['settings']['DO_PHANTOM'])


def search_profiles():
    serial_numbers = list(range(FIRST_PROFILE, FIRST_PROFILE + PROFILE_NUMBER))

    profile_data = adspower.get_profile_data(config['settings']['first_profile'])

    group_name = profile_data['group_name']

    try:
        offset = int(re.findall(r'Profiles(\d*)-\d*_.*', group_name)[0]) - 1
    except Exception as e:
        raise Exception('Could not determine the number of the first profile in the group (the group has a non-standard name)')

    profiles_in_group = adspower.get_profiles_in_group(profile_data['group_id'])

    for serial_number in serial_numbers:
        try:
            [i for i in profiles_in_group if int(i['serial_number']) == serial_number][0]
        except ValueError:
            raise Exception(f'Couldn\'t find profile {serial_number} in group')

    return offset


def worker(serial_number, seed, bar: Bar):
    global CURRENT_THREADS

    try:
        ws, driver_path = adspower.run_profile(serial_number)

        p_worker = Worker(ws, driver_path, seed, config['settings']['password'])

        sleep(5)
        p_worker.close_all_tabs()

        if DO_METAMASK:
            metamask_status = p_worker.get_metamask_status()

            if metamask_status == 'unlocked':
                pass
            elif metamask_status == 'locked':
                p_worker.restore_metamask()
            else:
                p_worker.import_metamask()
        if DO_KEPLR:
            p_worker.import_keplr()
    except WorkerException as e:
        print(e)
    except Exception as e:
        print(type(e))
    finally:
        bar.next()
        CURRENT_THREADS -= 1


def main():
    global CURRENT_THREADS

    print('Pre-launch verefication...\n')

    try:
        adspower.check_adspower()
    except Exception as e:
        print(f'Failed to check adspower: {e}')
        input("\nPress Enter to close program...")
        exit()

    try:
        r = bypass.bypass()
    except Exception as e:
        print(f'MetaMask bypass failed: {e}')
        input("\nPress Enter to close program...")
        exit()

    if DO_KEPLR:
        try:
            bypass.reset_keplr()
        except Exception as e:
            print(f'Keplr reset error: {e}')
            input("\nPress Enter to close program...")
            exit()

    if not r:
        print('MetaMask bypass error. Check if the last version of extension is installed in AdsPower.')
        input("\nPress Enter to close program...")
        exit()

    try:
        seeds = open('metamask.txt').read().split('\n')
    except FileNotFoundError:
        print('File metamask.txt not found')
        input("\nPress Enter to close program...")
        exit()

    if not seeds[-1]:
        seeds = seeds[:-1]

    print(f'Verification is complete. Searching profiles...\n')

    try:
        offset = search_profiles()
    except Exception as e:
        print(f'Couldn\'t find profiles: {e}')
        input("\nPress Enter to close program...")
        exit()

    seeds = seeds[offset:offset + PROFILE_NUMBER]
    serial_numbers = list(range(FIRST_PROFILE, FIRST_PROFILE + PROFILE_NUMBER))

    if len(seeds) != PROFILE_NUMBER:
        print(f'For profiles {FIRST_PROFILE}-{FIRST_PROFILE + PROFILE_NUMBER - 1} in the metamask file.txt must be at least {offset + PROFILE_NUMBER} seeds')
        input("\nPress Enter to close program...")
        exit()

    print(f'Search complete. Configuring profiles...\n')

    bar = Bar('Configuring profiles', max=len(seeds))

    bar.start()

    for i in range(len(seeds)):
        while CURRENT_THREADS >= MAX_THREADS:
            continue

        CURRENT_THREADS += 1

        thread = Thread(target=worker, args=(serial_numbers[i], seeds[i], bar))
        thread.start()

    while CURRENT_THREADS != 0:
        continue

    input("\n\nPress Enter to close program...")


if __name__ == '__main__':
    main()
