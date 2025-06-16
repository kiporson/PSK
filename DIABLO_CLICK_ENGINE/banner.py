#!/usr/bin/env python3
"""Display colored ASCII banner with statistics."""

from pyfiglet import Figlet

# ANSI color codes
RED = "\033[91m"
CYAN = "\033[96m"
GREEN = "\033[92m"
BLUE = "\033[94m"
WHITE = "\033[97m"
RESET = "\033[0m"

SKULL = r'''
      .ed""" """$$$be.
    -"           ^""**$$$e.
  ."                   '$$$c
 /                      "4$$b
/                        d$$$
|                         $$$
'             .eeeeee.    $$$
  .          ""    ""   .$$$
   ".                 .$$$$
     "-.._____..-"$$$$$$"
'''


def show_banner(valid: int, total: int, ip: str, durasi: float) -> None:
    """Print skull, DIABLO text and usage instructions."""
    fig = Figlet(font="slant")
    diablo_text = fig.renderText("DIABLO")

    print(f"{RED}{SKULL}{RESET}")
    print(f"{CYAN}{diablo_text}{RESET}")
    print(f"{BLUE}IP Lokal : {ip}{RESET}")
    print(f"{BLUE}Durasi   : {durasi:.2f}s{RESET}")
    print(f"{BLUE}Proxy OK : {valid}/{total}{RESET}")
    print(f"{GREEN}BOT READY{RESET}\n")
    print(f"{WHITE}jalankan: bash start.sh{RESET}")
    print(f"{WHITE}masukkan link satu per satu kemudian ketik 'DONE'{RESET}\n")


