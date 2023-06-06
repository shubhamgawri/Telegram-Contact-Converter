import argparse
import json
import os

# vCard template
def vcf(fname, lname, cell):
    cell = cell.replace(" ", "")

    vcard = (
             f"BEGIN:VCARD\n"
             "VERSION:3.0\n"
             f"FN:{fname}{' ' if fname else ''}{lname}\n"
             f"N:{lname};{fname};;;\n"
             f"TEL;TYPE=CELL:{cell}\n"
             "END:VCARD\n"
    )

    return vcard

parser = argparse.ArgumentParser(
    description="Convert exported Telegram contacts JSON file to VCF file"
)

parser.add_argument(
    "json_file",
    help="input json file",
    action="store",
)

parser.add_argument(
    "vcf_file",
    help="output vcf file",
    action="store",
)

args = parser.parse_args()
json_file = args.json_file
vcf_file = args.vcf_file

if os.path.isdir(vcf_file):
    print(f"\n{vcf_file} is a directory! 'Contacts.vcf' is created in it.")
    if not vcf_file.endswith(os.sep):
        vcf_file += os.sep
    vcf_file += "Contacts.vcf"

# Check if the entered vcf_file exists.
# If the file already exists, then the file is renamed.
if os.path.isfile(vcf_file):
    head, tail = os.path.split(vcf_file)
    new_file_name = "new_" + tail
    print(f"\n{tail} already exists. Renaming it to {new_file_name}.")
    vcf_file = head + os.sep + new_file_name

try:
    contacts = json.load(open(json_file, encoding="utf8"))
    contacts = contacts["contacts"]["list"]
except Exception as err:
    raise RuntimeError("An unexpected error happened!") from err

with open(vcf_file, "w", encoding="utf8") as f:
    for contact in contacts:
        fname = contact["first_name"]
        lname = contact["last_name"]
        cell = contact["phone_number"]
        vcard = vcf(fname, lname, cell)
        f.write(vcard)
