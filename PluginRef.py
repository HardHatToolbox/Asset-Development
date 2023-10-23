import xml.etree.ElementTree as ET
import xml.dom.minidom
import re
import argparse

def get_package_references(csproj_path):
    """Extract package references from a .csproj file."""
    tree = ET.parse(csproj_path)
    root = tree.getroot()

    references = {}
    for package_ref in root.findall(".//PackageReference"):
        package_name = package_ref.attrib.get('Include')
        package_version = package_ref.attrib.get('Version')
        if package_name and package_version:
            references[package_name] = package_version

    return references

def fix_missing_package_refs(csproj_path, missing_refs, mismatched_versions):
    """Add any missing or mismatched refs to the plugin"""
    tree = ET.parse(csproj_path)
    root = tree.getroot()

    # Handle mismatched versions
    for package_ref in root.findall(".//PackageReference"):
        package_name = package_ref.attrib.get('Include')
        if package_name in mismatched_versions:
            package_ref.attrib['Version'] = mismatched_versions[package_name]

    # Handle missing references
    # First, find or create an ItemGroup for PackageReference
    item_group = root.find(".//ItemGroup[PackageReference]")
    if item_group is None:
        item_group = ET.SubElement(root, 'ItemGroup')
    
    for name, version in missing_refs.items():
        package_ref = ET.SubElement(item_group, 'PackageReference')
        package_ref.attrib['Include'] = name
        package_ref.attrib['Version'] = version

    # Convert the ElementTree to a string
    xml_str = ET.tostring(root, encoding='utf-8').decode('utf-8')

    # Prettify the XML string
    pretty_xml_str = prettify_xml(xml_str)

    # Save the prettified XML string to the .csproj file
    with open(csproj_path, 'w', encoding='utf-8') as f:
        f.write(pretty_xml_str)


def prettify_xml(xml_str):
    """Prettify XML string without adding extra line breaks."""
    # Prettify the XML string using minidom
    dom = xml.dom.minidom.parseString(xml_str)
    pretty_xml_str = dom.toprettyxml(indent="  ")

    # Remove extra line breaks added by toprettyxml
    pretty_xml_str = re.sub(r'\n\s*\n', '\n', pretty_xml_str)
    return pretty_xml_str



def main():

    # parse arguments for -HH which is the main project path and -Plugin which is the plugin project path
    parser = argparse.ArgumentParser(description='Check for missing package references in a plugin')
    parser.add_argument('-HH', '--HardHat', help='Path to the HardHatC2Client.csproj file', required=True)
    parser.add_argument('-PF', '--Plugin', help='Path to the Rivet_ClientPlugin.csproj file', required=True)
    args = parser.parse_args()


    main_project_path = args.HardHat
    plugin_project_path = args.Plugin

    main_references = get_package_references(main_project_path)
    plugin_references = get_package_references(plugin_project_path)


    missing_references = {k: v for k, v in main_references.items() if k not in plugin_references}
    mismatched_versions = {k: v for k, v in main_references.items() if k in plugin_references and plugin_references[k] != v}

    if missing_references:
        print("Missing package references in plugin:")
        for name, version in missing_references.items():
            print(f"- {name} ({version})")

    if mismatched_versions:
        print("\nMismatched package versions:")
        for name, version in mismatched_versions.items():
            print(f"- Expected {name} ({version}), but found {plugin_references[name]}")

    if missing_references or mismatched_versions:
        fix_missing_package_refs(plugin_project_path,missing_references,mismatched_versions)
        print("\nFixed missing package references and mismatched versions in plugin!")

    if not missing_references and not mismatched_versions:
        print("All package references are consistent!")


if __name__ == "__main__":
    main()