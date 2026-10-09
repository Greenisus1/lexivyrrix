# lexivyrrix 1.0.0

Original offline fullscreen five-letter deduction game inspired by Wordle. Six guesses, green correct-position marks, yellow elsewhere marks and gray absent-letter marks. Duplicate-letter scoring counts only the unused answer letters. An on-screen keyboard keeps the best known result for each letter. Random rounds, not an official daily puzzle, and no official branding or assets.

Type a five-letter word and press Enter. Backspace erases. Esc opens commands: N starts a fresh round, Q exits, Esc returns. These command keys do not interfere with typing words containing n or q. Six failed guesses reveal the answer. Only the bundled, hand-curated word list is accepted, not every dictionary word. No hard mode, stats or saved rounds.

Python 3 and curses standard library, no network, pip or account. Minimum52x25; gameplay pauses while smaller. Color terminals show green/yellow/gray; monochrome terminals show G/Y/- for the latest guess. Install checks dependencies/source without installing system packages.

    bash app-store.sh install
    bash app-store.sh run
    python3 -m unittest -v

Ten game tests, fullscreen typing/guess/resize/exit/restoration and actual rendered pixels checked on Linux. Physical Raspberry Pi and non-Linux untested. MIT license.
