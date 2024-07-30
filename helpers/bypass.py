from string import ascii_uppercase
import os
import re
from shutil import rmtree


def bypass():
    for disk in ascii_uppercase:
        try:
            os.listdir(f'{disk}:\\.ADSPOWER_GLOBAL')
        except FileNotFoundError:
            continue
        else:
            adspower_path = f'{disk}:\\.ADSPOWER_GLOBAL'
            break
    else:
        return False

    if 'ext' in os.listdir(adspower_path):
        ext_folders = os.listdir(f'{adspower_path}\\ext')

        bypassed = False

        for extension in ext_folders:
            extension_path = f'{adspower_path}\\ext\\{extension}'

            if not os.path.isdir(extension_path):
                continue

            if 'scripts' in os.listdir(extension_path):
                lavamoant_path = f'{extension_path}\\scripts\\runtime-lavamoat.js'

                try:
                    file = open(lavamoant_path, encoding='utf-8').read()
                except FileNotFoundError:
                    continue

                replaced = re.sub(r'} = {"scuttleGlobalThis":\{.*}','} = {"scuttleGlobalThis":{"enabled":false,"scuttlerName":"SCUTTLER","exceptions":[]}}', file)

                with open(lavamoant_path, 'w', encoding='utf-8') as file:
                    file.write(replaced)
                    file.close()

                bypassed = True

        if bypassed:
            return True
        else:
            return False
    else:
        return False


def reset_keplr():
    for disk in ascii_uppercase:
        try:
            os.listdir(f'{disk}:\\.ADSPOWER_GLOBAL')
        except FileNotFoundError:
            continue
        else:
            adspower_path = f'{disk}:\\.ADSPOWER_GLOBAL'
            break
    else:
        raise Exception('ADSPOWER not found')

    cache = f'{adspower_path}\\cache'

    for profile in [f'{cache}\\{i}' for i in os.listdir(cache)]:
        storage_path = f'{profile}\\Default\\Local Extension Settings'

        try:
            extension_dirs = [f'{storage_path}\\{i}' for i in os.listdir(storage_path)]
        except FileNotFoundError:
            continue

        for extension in extension_dirs:
            log_files = [f'{extension}\\{i}' for i in os.listdir(extension) if '.log' in i]

            for log in log_files:
                file = open(log, encoding='ANSI').read()
                if 'wallet.keplr.app' in file:
                    break
            else:
                continue

            try:
                rmtree(extension)
            except:
                raise Exception('all profiles must be closed')
