#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Example URL:
http://bionmr.unl.edu/dgs-gensched.php?schedType=dbag&nx=1024&ny=256&nz=128&density=10&ndims=1&raw=yes
"""

import argparse
import requests
import subprocess
import tkinter as tk
import tkinter.font as font
import tkinter.scrolledtext as tkst


def parse_arguments():
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        "--schedule_type",
        required=True,
        type=str,
        default="SB",
        choices=["SB", "SG", "PG"],
        help="schedule type: Sine-burst (SB), Sine-gap (SG), Poisson-gap (PG)",
    )
    parser.add_argument(
        "--ndims",
        required=True,
        type=int,
        choices=[2, 3, 4],
        help="number of dimensions: 2, 3 or 4",
    )
    parser.add_argument(
        "--density", required=True, type=int, help="density of the sampling"
    )
    parser.add_argument(
        "--nx",
        required=True,
        type=int,
        help="number of points in first NUS dimension",
    )

    parser.add_argument(
        "--ny",
        type=int,
        help="number of points in second NUS dimension",
    )
    parser.add_argument(
        "--nz",
        type=int,
        help="number of points in third NUS dimension",
    )

    args = parser.parse_args()

    return args


def get_sampling_schedule(base_url, args):

    if args.schedule_type == "SB":
        args.schedule_type = "dbag"
    elif args.schedule_type == "SG":
        args.schedule_type = "dpg"
    elif args.schedule_type == "PG":
        args.schedule_type = "spg"

    parameters = {
        "schedType": args.schedule_type,
        "ndims": args.ndims,
        "density": args.density,
        "nx": args.nx,
        "ny": args.ny,
        "nz": args.nz,
        "raw": "yes",
    }

    try:
        response = requests.get(base_url, params=parameters, timeout=3)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        raise SystemExit(errh)
    except requests.exceptions.ConnectionError as errc:
        raise SystemExit(errc)
    except requests.exceptions.Timeout as errt:
        raise SystemExit(errt)
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

    nuslist = response.text

    return nuslist


def show_onscreen(nuslist, args):

    if args.schedule_type == "dbag":
        schedule_type = "Sine-burst"
    elif args.schedule_type == "dpg":
        schedule_type = "Sine-gap"
    elif args.schedule_type == "spg":
        schedule_type = "Poisson-gap"

    schedule_type = "Sine-burst"

    window = tk.Tk()
    window.title("NUS schedule")

    frame_title = tk.Frame(master=window)
    frame_results = tk.Frame(master=window)
    frame_warning = tk.Frame(master=window)
    frame_button = tk.Frame(master=window)

    text1 = tk.Label(
        master=frame_title,
        text="NUS list using a {} sampling schedule".format(schedule_type),
        padx=100,
    )
    text1.pack()

    text2 = tk.Label(
        master=frame_title,
        text="For a {}D dataset, with a {}% NUS density".format(
            args.ndims, args.density
        ),
    )
    text2.pack()

    results_list = tkst.ScrolledText(
        master=frame_results, wrap=tk.WORD, width=30, height=50
    )
    results_list.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    results_list.insert(tk.INSERT, nuslist)

    warning_text_font = font.Font(slant="italic", size=10)
    text3 = tk.Label(
        master=frame_warning,
        text="The NUS schedule has been copied to the clipboard",
        font=warning_text_font,
        pady=10,
    )
    text3.pack()

    done_button = tk.Button(master=frame_button, text="Done", command=window.destroy)
    done_button.pack()

    frame_title.pack()
    frame_results.pack(fill="both", expand="yes")
    frame_warning.pack()
    frame_button.pack()

    window.clipboard_clear()
    window.clipboard_append(nuslist)
    window.update()
    window.mainloop()


def main():
    base_url = "http://bionmr.unl.edu/dgs-gensched.php"

    args = parse_arguments()

    nuslist = get_sampling_schedule(base_url, args)

    show_onscreen(nuslist, args)

    return nuslist


if __name__ == "__main__":
    nuslist = main()
