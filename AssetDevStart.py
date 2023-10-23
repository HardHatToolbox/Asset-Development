import xml.etree.ElementTree as ET
import xml.dom.minidom
import re
import argparse
import os
import subprocess
import platform
import json
import shutil

def get_latest_dotnet7_sdk_version():
    # Fetch the release data from the .NET releases API
    response = subprocess.run("curl -sSL https://dotnetcli.blob.core.windows.net/dotnet/release-metadata/7.0/releases.json", capture_output=True, shell=True)
    # Parse the JSON response
    releases = json.loads(response.stdout.decode('utf-8'))
    # Get the latest SDK version
    latest_sdk_version = releases['latest-sdk']
    return latest_sdk_version


def main():


    # parse arguments for -HH which is the main project path and -Plugin which is the plugin project path
    parser = argparse.ArgumentParser(description='Check for missing package references in a plugin')
    parser.add_argument('-HH', '--HardHat', help='Path to the HardHat base folder', required=True)
    parser.add_argument('-PF', '--PluginFolder', help='Path to the folder for the plugin can be existing empty folder or not yet exist', required=True)
    parser.add_argument('-PN', '--PluginName', help='Desired name for the plugin example Rivet, Engineer etc.', required=True)
    args = parser.parse_args()

    main_project_path = args.HardHat
    plugin_project_path = args.PluginFolder
    plugin_name = args.PluginName

    # execute the dotnet --version command and check if the output starts with a 7
    # if not print an error message and exit
    if not subprocess.run(["dotnet", "--version"], capture_output=True).stdout.decode('utf-8').startswith("7"):
        print("Error: dotnet 7.0 SDK is required")
        # Prompt the user
        response = input("Do you want to install .NET 7 SDK? (yes/no): ").strip().lower()

        # Check the response
        if response == "yes":
            # Install .NET 7 SDK
            print("Installing latest .NET 7 SDK...")
            latestDotnet = get_latest_dotnet7_sdk_version()
            # check the OS and install the appropriate .NET 7 SDK
            currentOS = platform.system()
            # For Windows
            if currentOS == "Windows":
                os.system(f"powershell -Command Start-Process -Wait -FilePath 'https://dotnet.microsoft.com/download/dotnet/thank-you/sdk-{latestDotnet}-windows-x64-installer'")
            # For Linux
            elif currentOS == "Linux":
                os.system(f"wget https://dotnet.microsoft.com/download/dotnet/thank-you/sdk-{latestDotnet}-linux-x64-binaries -O dotnet-sdk-{latestDotnet}-linux-x64.tar.gz")
                os.system(f"mkdir -p $HOME/dotnet && tar zxf dotnet-sdk-{latestDotnet}-linux-x64.tar.gz -C $HOME/dotnet")
                os.system("export DOTNET_ROOT=$HOME/dotnet")
                os.system("export PATH=$PATH:$HOME/dotnet")
            # For Mac
            elif currentOS == "Darwin":
                os.system(f"wget https://dotnet.microsoft.com/download/dotnet/thank-you/sdk-{latestDotnet}-macos-x64-installer -O dotnet-sdk-{latestDotnet}-macos-x64-installer.pkg")
                os.system(f"sudo installer -pkg dotnet-sdk-{latestDotnet}-macos-x64-installer.pkg -target /")

            else:
                print("Error: OS detection failed, please install .NET 7 SDK manually")
                exit(1)

            # Check if the installation was successful
            if not subprocess.run(["dotnet", "--version"], capture_output=True).stdout.decode('utf-8').startswith("7"):
                print("Error: .NET 7 SDK installation failed")
                exit(1)
            print(".NET 7 SDK installation complete!")
        else:
            print("Installation skipped. Exiting...")  
            exit(1)
    print("dotnet 7.0 SDK found")


   # check if the plugin folder exists if not create it
    if not os.path.exists(plugin_project_path):
        os.makedirs(plugin_project_path)
        os.makedirs(plugin_project_path + plugin_name + "_Asset")
        print("Plugin folder created at " + plugin_project_path)
        print("Plugin asset folder created at " + plugin_project_path + plugin_name + "_Asset")
    # in the plugin folder run dotnet new razorclasslib -n {plugin_name_ServerPlugin} -o {plugin_name_ServerPlugin}
    print("Creating team server plugin project")
    subprocess.run(["dotnet", "new", "classlib", "-n", plugin_name + "_ServerPlugin", "-o", plugin_project_path + plugin_name + "_ServerPlugin"])
    print("Plugin project created at " + plugin_project_path + plugin_name + "_ServerPlugin")

    # create the client plugin project with dotnet new razorlib -n {plugin_name_ClientPlugin} -o {plugin_name_ClientPlugin}
    print("Creating client plugin project")
    subprocess.run(["dotnet", "new", "razorclasslib", "-n", plugin_name + "_ClientPlugin", "-o", plugin_project_path + plugin_name + "_ClientPlugin"])
    print("Plugin project created at " + plugin_project_path + plugin_name + "_ClientPlugin")

    # exexcute dotnet build -c Release on the HardHat project to ensure we have dlls to reference
    print("Building HardHat project")
    subprocess.run(["dotnet", "build", "-c", "Release"], cwd=main_project_path)
    print("HardHat project built")

    #update the server project csproj file to set the sdk as Sdk="Microsoft.NET.Sdk.Web"
    print("Updating server project csproj file")
    server_project_path = plugin_project_path + plugin_name + "_ServerPlugin"
    server_project_csproj_path = server_project_path + "\\" + plugin_name + "_ServerPlugin.csproj"
    server_project_csproj_file = open(server_project_csproj_path, "r")
    server_project_csproj_file_contents = server_project_csproj_file.read()
    server_project_csproj_file.close()

    # add reference to the HardHat project TeamServer and ApiModels release dlls in the server project csproj file, use the absolute path to the dlls 
    HardHatTeamServerPath = (main_project_path + "TeamServer\\bin\\Release\\net7.0\\TeamServer.dll").replace('\\', '\\\\')
    HardHatApiModelsPath = (main_project_path + "ApiModels\\bin\\Release\\net7.0\\ApiModels.dll").replace('\\', '\\\\')

    server_project_csproj_file_contents = re.sub(r'<Project Sdk="Microsoft.NET.Sdk">', '<Project Sdk="Microsoft.NET.Sdk.Web">', server_project_csproj_file_contents)
    server_project_csproj_file_contents = re.sub(r'</Project>', '<ItemGroup><Reference Include="TeamServer"><HintPath>' + HardHatTeamServerPath + '</HintPath></Reference><Reference Include="ApiModels"><HintPath>' 
    + HardHatApiModelsPath + '</HintPath></Reference></ItemGroup></Project>', server_project_csproj_file_contents)

    #update the csproj file to the new contents 
    server_project_csproj_file = open(server_project_csproj_path, "w")
    server_project_csproj_file.write(server_project_csproj_file_contents)
    server_project_csproj_file.close()

    #update the client project csproj file
    print("Updating client project csproj file")
    client_project_path = plugin_project_path + plugin_name + "_ClientPlugin"
    client_project_csproj_path = client_project_path + "\\" + plugin_name + "_ClientPlugin.csproj"
    client_project_csproj_file = open(client_project_csproj_path, "r")
    client_project_csproj_file_contents = client_project_csproj_file.read()
    client_project_csproj_file.close()

    # add reference to the hardHat projects Client and ApiModels release dlls in the client project csproj file, use the absolute path to the dlls
    HardHatClientPath = (main_project_path + "HardHatC2Client\\bin\\Release\\net7.0\\HardHatC2Client.dll").replace('\\', '\\\\')
    
    client_project_csproj_file_contents  = re.sub(r'</Project>', '<ItemGroup><Reference Include="HardHatC2Client"><HintPath>' + HardHatClientPath + '</HintPath></Reference><Reference Include="ApiModels"><HintPath>' 
    + HardHatApiModelsPath + '</HintPath></Reference></ItemGroup></Project>', client_project_csproj_file_contents)

    #update the csproj file to the new contents
    client_project_csproj_file = open(client_project_csproj_path, "w")
    client_project_csproj_file.write(client_project_csproj_file_contents)
    client_project_csproj_file.close()

    # execute the pluginRef.py script to update the plugin references in the HardHat project for the server
    print("Updating HardHat server project plugin references")
    subprocess.run(["python3", "pluginRef.py", "-HH", main_project_path + "TeamServer\\TeamServer.csproj", "-PF", server_project_csproj_path])
    print("HardHat server project plugin references updated")
    # execute the pluginRef.py script to update the plugin references in the HardHat project for the client
    print("Updating HardHat client project plugin references")
    subprocess.run(["python3", "pluginRef.py", "-HH", main_project_path + "HardHatC2Client\\HardHatC2Client.csproj", "-PF", client_project_csproj_path])
    print("HardHat client project plugin references updated")


    # copy the files from the current folder ./Client_Starter_File to the client project folder and the files from ./Server_Starter_File to the server project folder
    print("Copying starter files to plugin project folders")
    shutil.copytree("./Asset_Client_Starter_Files", client_project_path + "/src",dirs_exist_ok=True)
    shutil.copytree("./Asset_Server_Starter_Files", server_project_path + "/src",dirs_exist_ok=True)
    print("Starter files copied to plugin project folders")

    # modify each starter file to replace the keyword Asset with the plugin name provided by the user
    print("Updating starter files with plugin name")
    for file in os.listdir(client_project_path + "/src"):
        file_path = os.path.join(client_project_path  + "/src", file)
        with open(file_path, "r") as f:
            file_contents = f.read()
            file_contents = re.sub(r'Asset', plugin_name, file_contents)
        with open(file_path, "w") as f:
            f.write(file_contents)
        #if file name contains Asset, rename the file to the plugin name
        if "Asset" in file:
            new_file_path = os.path.join(client_project_path  + "/src", file.replace("Asset", plugin_name))
            os.rename(file_path, new_file_path)

    for file in os.listdir(server_project_path  + "/src"):
        file_path = os.path.join(server_project_path  + "/src", file)
        with open(file_path, "r") as f:
            file_contents = f.read()
            file_contents = re.sub(r'Asset', plugin_name, file_contents)
        with open(file_path, "w") as f:
            f.write(file_contents)
        #if file name contains Asset, rename the file to the plugin name
        if "Asset" in file:
            new_file_path = os.path.join(server_project_path  + "/src", file.replace("Asset", plugin_name))
            os.rename(file_path, new_file_path)


    # create a solution file for the plugin that includes the server and client projects
    print("Creating plugin solution file")
    subprocess.run(["dotnet", "new", "sln", "-n", plugin_name + "_Plugin_HardHatC2", "-o", plugin_project_path])
    print("Plugin solution file created at " + plugin_project_path + plugin_name + "_Plugin_HardHatC2.sln")
    print("Adding server project to plugin solution file")
    subprocess.run(["dotnet", "sln", plugin_project_path + plugin_name + "_Plugin_HardHatC2.sln", "add", plugin_project_path + plugin_name + "_ServerPlugin\\" + plugin_name + "_ServerPlugin.csproj"])
    print("Adding client project to plugin solution file")
    subprocess.run(["dotnet", "sln", plugin_project_path + plugin_name + "_Plugin_HardHatC2.sln", "add", plugin_project_path + plugin_name + "_ClientPlugin\\" + plugin_name + "_ClientPlugin.csproj"])
    print("Plugin solution file updated")



    print("Plugin project creation complete")



if __name__ == "__main__":
    main()