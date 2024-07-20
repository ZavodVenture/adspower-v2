from source.helpers import adspower, bypass
from configparser import ConfigParser
from progress.bar import Bar
from threading import Thread
from source.helpers.profileWorker import Worker, WorkerException
from time import sleep

config = ConfigParser()
config.read('config.ini')

MAX_THREADS = int(config['settings']['threads'])
CURRENT_THREADS = 0

DO_METAMASK = int(config['settings']['DO_METAMASK'])
DO_KEPLR = int(config['settings']['DO_KEPLR'])
DO_PHANTOM = int(config['settings']['DO_PHANTOM'])


def create_profiles(offset, profiles_number, proxies, bar: Bar):
    group_tag = config['settings']['group_name']

    group_name = f'Profiles{offset + 1}-{offset + profiles_number}_{group_tag}'

    group_id = adspower.get_group_id(group_name)

    if not group_id:
        group_id = adspower.create_group(group_name)

    serial_numbers = []

    for i in range(profiles_number):
        serial_numbers.append(adspower.create_profile(group_id, proxies[i]))
        bar.next()

    return serial_numbers


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

    try:
        proxies = open('proxy.txt').read().split('\n')
    except FileNotFoundError:
        print('File proxy.txt not found. Proxies will not be used.\n')
        proxies = [None] * len(seeds)
    else:
        if not proxies[-1]:
            proxies = proxies[:-1]

    if len(proxies) != len(seeds):
        print(f'An unequal number of proxies ({len(proxies)}) and seeds ({len(seeds)}) were transmitted')
        input("\nPress Enter to close program...")
        exit()

    offset = int(config['settings']['offset'])
    profiles_number = int(config['settings']['profiles_number'])

    seeds = seeds[offset:offset + profiles_number]
    proxies = proxies[offset:offset + profiles_number]

    if len(seeds) != profiles_number:
        print(f'The number of seeds passed is not enough to use offset {offset} and the number {profiles_number}')
        input("\nPress Enter to close program...")
        exit()

    print(f'Verification is complete. Creating {offset+1}-{offset + profiles_number} profiles...\n')

    bar = Bar('Creating profiles', max=profiles_number)
    bar.start()

    try:
        serial_numbers = create_profiles(offset, profiles_number, proxies, bar)
    except Exception as e:
        bar.finish()
        print(f'\nError while creating profiles: {e}')
        input("\nPress Enter to close program...")
        exit()

    bar.finish()

    print('\nProfiles have been created successfully. Configuring profiles...\n')

    bar = Bar('Configuring profiles', max=len(seeds))
    bar.start()

    for i in range(len(serial_numbers)):
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
