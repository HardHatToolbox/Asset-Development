using HardHatCore.HardHatC2Client.Components.ImplantCreation;
using HardHatCore.HardHatC2Client.Plugin_BaseClasses;
using HardHatCore.HardHatC2Client.Plugin_Interfaces;
using Asset_ClientPlugin.src;
using Microsoft.AspNetCore.Components;
using System.ComponentModel.Composition; //make sure to add this and not the System.Composition package


namespace Asset_ClientPlugin
{
    [Export(typeof(IimplantCreation))]
    //metadata that is used to config which build options are displayed in the UI
    [ImplantCreationBaseData(
            Name = "Asset",
            Description = "This is the Asset implant creation",
            //expected values are HTTP, HTTPS, SMB, TCP as those are the currently supported comm types by HardHat
            SupportedCommTypes = new string[] { "{{REPLACE_ME}}" },
            //Any value is accepted here, but should include OSs that the implant is compatible with and logic should be added to the Asset_Service.cs file to handle OS specific compilation
            SupportedOperatingSystems = new string[] { "{{REPLACE_ME}}" },
            //expected values are some of the following depending on what compile types your payload supports "exe", "serviceExe", "dll", "powershellCmd", "bin"
            SupportedOutputTypes = new string[] { "{{REPLACE_ME}}" },
            //expected values are true or false enables connection attempt in the build Menu
            SupportsConnectionAttempts = "{{REPLACE_ME}}" ,
            //expected values are true or false enables kill date in the build Menu
            SupportsKillDates = "{{REPLACE_ME}}" ,
            //expected values are true or false enables post ex support and Module Popups in the build Menu
            //should be true if implant has postEx spawn commands like Jump, Spawn, Inject, etc. 
            SupportsPostEx = "{{REPLACE_ME}}" 
    )]
    public class Asset_Creation_plugin : IimplantCreation
    {
        //just needs to be set with the name of the .Razor file that is used for the UI when creating the implant
        public Type GetComponentType()
        {
            return typeof(Asset_Creation_Component);
        }

        //does not have a module options UI element it needs to load so just returns an empty builder
        public RenderFragment GetModuleOptionsUI()
        {
            return builder => { };

            //if you want to add a module options UI element, uncomment the below and add your component in the typeof call
            //return builder =>
            //{
            //    builder.OpenComponent(0, typeof(ModuleOptionsComponent));
            //    builder.CloseComponent();
            //};
        }
    }
}