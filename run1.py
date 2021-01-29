"""
AUTHOR: IPvZero
Date: 29 January 2021

Overview:
This script uses the Scrapli Netconf library
to retrieve the current interface information
of the IOSXR and IOSXE Always-On Sandboxes.
The output is printed in tabular form.

********************************************************
Instructions:
1) Git clone the repository
git clone https://github.com/IPvZero/DEVNET-INTERFACES/

2) Change into the DEVNET-INTERFACES directory
cd DEVNET-INTERFACES

3) Pip (or pip3) install the requirements
python3 -m pip install -r requirements.txt
or 
pip3 install -r requirements.txt

4) Execute the script run1.py script
python3 run1.py

********************************************************
"""

import logging
import itertools
from io import StringIO
from lxml import etree
from nornir_scrapli.tasks import netconf_get
from nornir import InitNornir
from rich.console import Console
from rich.table import Table


# Initialise Nornir
nr = InitNornir(config_file="config.yaml")

# XR does not natively support xpath
# Subtree filter used to get initial OC Interfaces XML
oc_filter = """
  <interfaces xmlns="http://openconfig.net/yang/interfaces">
  </interfaces>
"""


def get_yang(task):
    # Create 2 empty lists
    # Build table with 2 columns
    up_list = []
    down_list = []
    table = Table(title=f"{task.host} INTERFACES")
    table.add_column("UP", justify="center", style="green")
    table.add_column("DOWN", justify="right", style="red")

    # Send Get request with oc_filter
    # Save output to variable called 'result'
    result = task.run(
        task=netconf_get,
        filter_type="subtree",
        filter_=oc_filter,
        severity_level=logging.DEBUG,
    )
    # Get the XML string by taking the .result attribute
    # Save this to a variable called 'output'
    output = result.result

    # Give etree the string XML from the 'output' variable
    et = etree.parse(StringIO(output), parser=etree.HTMLParser(recover=True))
    # Get root of tree
    root = et.getroot()
    # Use etree's xpath to find desired tags
    path = root.xpath("//subinterface/ipv4//config")
    # Loop through elements
    for element in path:
        # Get the value of the 'ip' tag
        ip = element.findtext("ip")
        # Get the value of the 'prefix-length' tag
        prefix = element.findtext("prefix-length")
        # Walk back up the tree to correlate the interface name
        interface = element.xpath("ancestor::interface/name/text()")
        # Xpath returns a list with one item - unwrap the list
        intf = interface[0]
        #Join the vars in the desired format
        joined = f"{intf} - {ip}/{prefix}"
        # Walk back up the tree to correlate the interface oper-status
        oper_status = element.xpath("ancestor::interface/state/oper-status/text()")
        # Xpath returns a list with one item = unwrap the list
        oper = oper_status[0]

        # If state is 'DOWN' - add interface to down list
        if oper == "DOWN":
            down_list.append(joined)
        # If state is "UP" - add interface to up list
        if oper == "UP":
            up_list.append(joined)

    # Zip the two lists and populate the table rows
    for up, down in itertools.zip_longest(up_list, down_list):
        table.add_row(up, down)

    # Initialise rich console
    console = Console()


    # Print the table
    print("\n")
    console.print(table)
    print("\n")

# Main Nornir execution point
nr.run(task=get_yang)
