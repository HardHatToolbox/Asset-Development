using System.ComponentModel.Composition;
using HardHatCore.HardHatC2Client.Utilities;
using static HardHatCore.HardHatC2Client.Utilities.CommandItem;
using static HardHatCore.HardHatC2Client.Utilities.CommandKey;


namespace Asset_ClientPlugin
{
    [Export(typeof(IImplantCommandValidation))]
    [ExportMetadata("Name", "Asset")]
    [ExportMetadata("Description", "This is the Asset command validation")]
    public class AssetCommandValidation : IImplantCommandValidation
    {
       private readonly ImplantCommandValidation_Base implantCommandValidation_Base = new();

        public bool ValidateCommand(string input, out Dictionary<string, string> args, out string error)
        {
            return implantCommandValidation_Base.ValidateCommand(input, out args, out error);
        }

        public List<string> GetPostExCommands()
        {
            return implantCommandValidation_Base.GetPostExCommands();
        }

        public List<string> GetOptionalModules()
        {
            return implantCommandValidation_Base.GetOptionalModules();
        }

        public Dictionary<string, string> GetModuleCommandPairs()
        {
            return implantCommandValidation_Base.GetModuleCommandPairs();
        }

        public List<CommandItem> DisplayHelp(Dictionary<string, string> input)
        {
            return implantCommandValidation_Base.DisplayHelp(input);
        }

        public List<string> GetOptionalCommandList()
        {
            return implantCommandValidation_Base.GetOptionalCommandList();
        }

        public List<string> GetRequiredCommandList()
        {
            return implantCommandValidation_Base.GetRequiredCommandList();
        }

        public List<string> GetContextChangingCommands()
        {
            return implantCommandValidation_Base.GetContextChangingCommands();
        }

        //this should be overridden with the command list for the implant
        //while you can change this so the list is obtained in a different way or that command keys are obtained in a different way, that will mean writing your own validation logic as well
        public List<CommandItem> CommandList { get; } = new List<CommandItem>()
        {
	        //new CommandItem()
            //{
            // Name = "CommandName",
            // Description = "details about the command",
            // Usage = "CommandName",
            // NeedsAdmin = false,
            // Opsec = OpsecStatus.NotSet,
            // MitreTechnique = "",
            // RequiresPreProc = false, //if true, there should be an override of the team servers ExtImplant_TaskPreProcess_Base class 
            // RequiresPostProc = false, //if true, there should be an override of the team servers ExtImplant_TaskPostProcess_Base class 
            // Keys = null,
            //},
			new CommandItem()
            {
                Name = "example",
                Description = "details about this command",
                Usage = "example /key value /key2 value2",
                //a boolean value that determines if the command requires High Integrity to run, if true, the command will not be sent to the implant if the implant is running as a standard user
                NeedsAdmin = false ,
                Opsec = OpsecStatus.NotSet,
                MitreTechnique = "optional mitre technique TXXXX value",
                //if true, there should be an override of the team servers ExtImplant_TaskPreProcess_Base class
                RequiresPreProc = false,
                //if true, there should be an override of the team servers ExtImplant_TaskPostProcess_Base class
                RequiresPostProc = false,
                //keys can be set to null if the command has no arguments, otherwise, the command arguments should be listed here
                Keys = new List<CommandKey>()
                {
                    //a key can be set to Required = false if the command argument is optional,
                    //if the key's existence is the only part that matters the NeedsValues can be set to false for example in whoami /groups the existence of the /groups key is all that matters, there is no value to use
                    new CommandKey() {Name = "/key", Description = "details on what the command argument is for" , Required = true, inputType = InputType.Text, PreDefinedValues = null, NeedsValues = true},
                    new CommandKey() {Name = "/key2", Description = "example of providing the managers as an input type, typically used in post ex commands like jump" , Required = true, inputType = InputType.Manager, PreDefinedValues = ManagerNames, NeedsValues = true},
                }
            },
        };



    }
}