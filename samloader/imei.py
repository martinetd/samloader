# SPDX-License-Identifier: GPL-3.0+

import random

from . import tacs

def imei_required(args):
    """
    Check if we need to fix up imei
    Only required for download and decrypt v4
    """
    if args.command == "download":
        return True
    if args.command == "decrypt" and args.enc_ver == 4:
        return True
    return False


def luhn_checksum(imei):
    """
    Return luhn check digit (as int)
    """
    imei += '0'
    parity = len(imei) % 2
    s = 0
    for idx, char in enumerate(imei):
        d = int(char)
        if idx % 2 == parity:
            d *= 2
            if d > 9:
                d -= 9
        s += d
    return (10 - (s % 10)) % 10


def fixup_imei(args):
    """
    Try to fill in args.imei if required
    """
    # only required for download or decrypt with v4
    if not imei_required(args):
        return 0

    if not args.dev_imei:
        found = tacs.TACS.get(args.dev_model)
        if not found:
            print(f"No known tacs for {args.dev_model}, set it manually through --dev-imei")
            print("(Also consider submitting it to https://github.com/zacharee/SamloaderKotlin/issues/116)")
            return 1
        args.dev_imei = random.choice(found)

    if not args.dev_imei.isdecimal():
        # probably a serial number, leave as is
        return 0

    if len(args.dev_imei) < 8:
        print("Need to provide at least 8 digits to have a chance of working")
        return 1

    if len(args.dev_imei) < 15:
        # Only prefix, append n digits and checksum
        missing = 14 - len(args.dev_imei)
        if missing > 0:
            rng = random.randint(0, 10 ** missing - 1)
            args.dev_imei += f"%0{missing}d" % rng
        args.dev_imei += str(luhn_checksum(args.dev_imei))
        print(f"Filled up imei to {args.dev_imei}")

    return 0
