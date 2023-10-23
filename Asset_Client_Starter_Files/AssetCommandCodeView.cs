using System.ComponentModel.Composition;
using HardHatCore.HardHatC2Client.Plugin_BaseClasses;

namespace Asset_ClientPlugin
{
    //This powers the command view UI component in hardhat, if you want users to be able to view command source code and make modifications straight in the UI, you need to implement this
    [Export(typeof(CommandCodeView_Base))]
    [ExportMetadata("Name", "Asset")]
    [ExportMetadata("Description", "This is the asset command code view")]
    [ExportMetadata("CodeLang","{{REPLACE_ME}}")]
    //relative path to the command source code folder from the HardHat base directory
    [ExportMetadata("ImplantSrc", "..\\{{REPLACE_ME}}")]
    internal class AssetCommandCodeView : CommandCodeView_Base
    {
    }
}