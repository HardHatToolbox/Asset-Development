# Asset Development
 A repo to aid in Asset development for HardHat C2

## Guide Steps 

### Getting Ready
1. Download the main HardHat C2 project `git clone https://github.com/DragoQCC/HardHatC2.git `
2. Download the plugin dev repo from the HardHat Toolbox `git clone https://github.com/HardHatToolbox/Asset-Development.git `
3. Ensure python3 is installed for your OS: `https://www.python.org/downloads/ `

### Getting Started With Asset Creation 
- Currently, HardHat supports plugins for Assets which are implants that can be written in any language. To get a working Asset, some client and server code is required. To help streamline this process a Python script has been provided to generate a set of C# projects that require very little modification. 
- Note: The path to the plugin folder does not need to exist and should end with the name of the Asset; for example if I was creating the Rivet asset, it could be `C:\HardHat_Assets\Rivet\`
1. Navigate to the plugin dev repo & execute `python3 .\AssetDevStart.py -HH PATH_TO_HARDHAT_FOLDER -PF PATH_TO_NEW_PLUGINFOLDER -PN AssetName `
   	- ex. `python3 .\AssetDevStart.py -HH C:\HardHat\ -PF C:\HardHat_Assets\Rivet\ -PN Rivet`
	- This will generate a few project folders & a solution file with all of the correct dependencies and references already created
	- The `Name_Asset` is an empty folder where the source code of the Asset should go. This can be in any language so long as it can communicate with HardHat via JSON 
	- the `Name_ClientPlugin` & `Name_ServerPlugin` folders are for the C# code to be used to add implementation details about your Asset to HardHatCore (Client + Server)
	- It is normal to see some errors from the dotnet command when it builds all the projects in the HardHat repo because the Engineer is not .net core and will fail 
1. Start to fill in the required implementation details in the client and server project files  
2. Create your Asset source code :)

#### What are the different premade files?
- Within the Client & Server folders, you will find a `/src` folder 
- Client
	- `Asset_Creation_Component.razor` -> Requires a step change function implementation is provided to handle any custom steps that are added during the build process
	- `Asset_Creation_Plugin.cs ` -> Requires the Exported metadata be updated  
	- `AssetCommandCodeView.cs ` -> Requires the expected relative path from the base HardHat folder to the Assets commands folder `ex. ../Assets/Rivet/Commands` Powers the code view tab in the Client side toolbox page
	- `AssetCommandValidation.cs ` -> Requires the list of Asset commands and overloads to the Validation function if the command does not follow the HardHatCore default
- Server 
	- `Asset_HandleComms.cs ` -> Requires an implementation of the `HandlePostRequest` if any encryption is added
	- `Asset_Service.cs ` -> Requires implementation of the compilation logic for the Asset; this may include ensuring the system has the required programs that are invoked such as Cargo for Rust Assets
		  if you wish to use the same AES encryption as the Engineer, modify the body of the function to be `extImplantService_Base.EncryptImplantTaskData(byte[] bytesToEnc, string encryptionKey)` for your plugins encryption and similarly for decryption function  
	- `Asset_TaskPostProcess.cs ` -> By default, requires no modifications until you want to add logic to handle specific task responses 
	- `Asset_TaskPreProcess.cs `   -> By default, requires no modifications until you want to add logic to handle tasking before it is sent to the Asset  
- All of the premade files come with a readonly copy of a base implementation of the class, which is the version the Engineer Asset uses, and for most things, the plugins are already set to utilize this base implementation but can be swapped out as required

### Ensuring your Asset is HardHat compatible
- Other than the Client and server code, you also have the main source code of your Asset. While it can be written in any language, it does need to follow some rules to communicate with HardHat 
1. Any desired Tasking encryption needs to match the encryption you provide in `Asset_Service.cs`
2. The object sent to the team server when building your Asset is going to contain user-selected options such as sleep time as strings, It is recommended to place placeholders like `"{{REPLACE_SLEEP_TIME}}" ` in your source code and do a string replacement in the build function but this is up to you on how to integrate the users choices into the code
3. The asset will need to expect a byte array as the response from HardHat during communication it should do the following 
	1. Decrypt the byte array using the `Message Path Key` provided by HardHat if encryption is supported 
	2. Deserialize into a List of the Assets version of a `C2TaskMessage`
	3. If Asset supports P2P comms then check each message's MessagePath to see if the task is for the current Asset  or a child Asset 
	4. Decrypt the byte array in the C2TaskMessage.TaskData using the `Task Encryption key` if encryption is supported 
	5. Deserialize the task data array into a List of the Assets version of the `ExtImplantTask_Base` class 
	6. Handle the task 
4. When communicating it is expected the Asset with send its Metadata in a header like `Authorization bearer Base64_String` 
	1. The metadata should be a base64 string from a byte array containing Asset_Name_Length + Asset_Name + Serialized Metadata object 
	2. Asset Name should be obtained during the build process from ` Encryption.EncryptImplantName(request.implantType);` this is a XORd version of the Asset name, during check-in the team server can decode this and then, based on the name, call the correct plugin to handle decryption and post-tasking processing as needed 
5. When sending back a task response it should be a serialized byte array of the Assets version of the `TaskResponse` object
6. As documented in the Rivet example and in the below section, the classes that require serialization need to return properly formatted JSON


#### Required Json Examples 
The following are the handful of JSON schemas that the Asset needs to include to properly talk with HardHat. While the Class itself can be named whatever you want the name & type of the Properties needs to match for serialization and deserialization to be successful. 
- Metadata 
```json
{
  "Id": "", //string
  "Hostname": "", //string
  "Address": "", //string
  "Username": "", //string
  "ProcessName": "", //string
  "ProcessId": 0, //int
  "Integrity": "", //string
  "Arch": "", //string
  "ManagerName": "", //string
  "Sleep": 0 //int
}
```

- Tasks, examples include the EngineerTask & RustyTask examples both of which can ingest JSON formatted like this 
```json
{
  "Id": "", //string
  "Command": "", //string
  "Arguments": null, //Dictionary<string,string>
  "File": "", //base64 encoded string that was originally a byte[]
  "IsBlocking": false //bool 
}
```

- C2 Messages, contains the path which is a collection of  GUIDs to show the path of Assets the message should take, and the task data which is a byte[] of the task 
```json
{
  "PathMessage": null, // List<string>
  "TaskData": null //base64 encoded string that was originally a byte[]
}
```

- Task Results 
```json
{
  "Id": "", //string
  "Command": "", //string
  "Result": "", //base64 encoded string that was originally a byte[]
  "IsHidden": false, // bool
  "ImplantId": "", //string
  "Status": 0, //Status Type
  "ResponseType": 0 // Response type 
}

enum TaskStatus
{
    Pending = 0,
    Tasked = 1,
    Running = 2,
    Complete = 3,
    FailedWithWarnings = 4,
    CompleteWithErrors = 5,
    Failed = 6,
    Cancelled = 7,
    NONE
}

enum TaskResponseType
{
    None = 0,
    String = 1,
    FileSystemItem = 2,
    ProcessItem = 3,
    HelpMenuItem = 4,
    TokenStoreItem = 5,
    DataChunk = 6,
    EditFile = 7
}
```

- Task result types like `String`, `FileSystemItem`, `ProcessItem` etc. all have backing classes the result byte array will get deserialized into 
- String -> MessageData
```json
{
  "Message": "", //string
}
```
- FileSystemItem
```json
{
  "Name": "", //string
  "Length": 0, //int
  "Owner": "", //string
  "ChildItemCount": 0, //int
  "CreationTimeUtc": "0001-01-01T00:00:00", //DateTime
  "LastAccessTimeUtc": "0001-01-01T00:00:00", //DateTime
  "LastWriteTimeUtc": "0001-01-01T00:00:00", //DateTime
  "ACLs": [] //List<ACL>
}
// ACL
{
  "IdentityRef": "", //string
  "AccessControlType": "", //string
  "FileSystemRights": "", //string
  "IsInherited": false //bool
}

```
- ProcessItem
```json
{
  "ProcessName": "", //string
  "ProcessPath": "", //string
  "Owner": "", //string
  "ProcessId": 0, //int
  "ProcessParentId": 0, //int
  "SessionId": 0, //int
  "Arch": "", //string
}
```
- TokenStoreItem
```json
{
  "Index": 0, //int
  "Username": "", //string
  "PID": 0, //int
  "SID": "", //string
  "IsCurrent": false //bool
}
```
- DataChunk
```json
{
  "Type": 0, //if a 1 its a part if 2 its the last part and the object can be put back together
  "Position": 0,
  "Length": 0,
  "Data": "", //base64 encoded string that was originally a byte[]
  "RealResponseType": 0 //TaskResponseType 
}
```
- EditFile 
```json
{
  "FileName": "", //string
  "Content": "", //string
  "CanEdit": false //bool
}
```

#### Example? 
- Check out the  [Rivet](https://github.com/HardHatToolbox/Rivet). project for an example of not only working & fully commented C# example code but also a working demo of an Asset written in Rust 

## Publishing Your Asset 
- The goal of HardHat is to provide a powerful, easy-to-use C2 framework, and hopefully, when you develop an Asset for HardHat, you aim to provide it to the community to learn and utilize together. 
- In light of that, reach out to join the HardHat Toolbox org on GitHub by sending a request to Drago-QCC on Discord, the Bloodhound gang slack, or Twitter with your GitHub username.


