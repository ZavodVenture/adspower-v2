from helpers import bypass


def main():
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

    print('MetaMask successfully bypassed')
    input("\nPress Enter to close program...")
    exit()


if __name__ == '__main__':
    main()
