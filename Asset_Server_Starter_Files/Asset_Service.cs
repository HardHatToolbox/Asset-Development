using HardHatCore.TeamServer.Plugin_BaseClasses;
using HardHatCore.ApiModels.Plugin_Interfaces;
using HardHatCore.TeamServer.Utilities;
using HardHatCore.ApiModels.Shared;
using HardHatCore.TeamServer.Models;
using HardHatCore.TeamServer.Services;
using System.Diagnostics;
using System.ComponentModel.Composition; //make sure to add this and not the System.Composition package
using HardHatCore.TeamServer.Plugin_Interfaces.Ext_Implants;

namespace Asset_ServerPlugin
{
    [Export(typeof(IExtImplantService))]
    [ExportMetadata("Name", "Asset")]
    public class Asset_serviceBase : IExtImplantService
    {
        private readonly ExtImplantService_Base extImplantService_Base = new();


        public void AddExtImplant(ExtImplant_Base Implant)
        {
            extImplantService_Base.AddExtImplant(Implant);
        }

        public IEnumerable<ExtImplant_Base> GetExtImplants()
        {
            return extImplantService_Base.GetExtImplants();
        }

        public ExtImplant_Base GetExtImplant(string id)
        {
            return extImplantService_Base.GetExtImplant(id);
        }

        public void RemoveExtImplant(ExtImplant_Base Implant)
        {
            extImplantService_Base.RemoveExtImplant(Implant);
        }
        
        public bool AddExtImplantToDatabase(ExtImplant_Base implant)
        {
            return extImplantService_Base.AddExtImplantToDatabase(implant);
        }

        public Httpmanager GetImplantsManager(IExtImplantMetadata extImplantMetadata)
        {
            return extImplantService_Base.GetImplantsManager(extImplantMetadata);
        }

        public ExtImplant_Base InitImplantObj(IExtImplantMetadata implantMeta, ref HttpContext httpcontentxt, string pluginName)
        {
            return extImplantService_Base.InitImplantObj(implantMeta, ref httpcontentxt, pluginName);
        }

        public ExtImplant_Base InitImplantObj(IExtImplantMetadata implantMeta, string pluginName)
        {
            return extImplantService_Base.InitImplantObj(implantMeta, pluginName);
        }

        public void LogImplantFirstCheckin(ExtImplant_Base implant)
        {
            extImplantService_Base.LogImplantFirstCheckin(implant);
        }

        public void UpdateImplantDBInfo(ExtImplant_Base implant)
        {
            extImplantService_Base.UpdateImplantDBInfo(implant);
        }

        public void GenerateUniqueEncryptionKeys(string implantId)
        {
            extImplantService_Base.GenerateUniqueEncryptionKeys(implantId);
        }

        public byte[] HandleP2PDataDecryption(IExtImplant implant, byte[] encryptedData)
        {
            return extImplantService_Base.HandleP2PDataDecryption(implant, encryptedData);
        }

        //This has to be overridden because it is implant specific, this function should contain the logic to generate the implant  
        public  bool CreateExtImplant(IExtImplantCreateRequest request, out string result_message)
        {
            result_message = "";
            return true;
        }

        //should be overridden to implement the same encryption as the implant 
        public byte[] EncryptImplantTaskData(byte[] bytesToEnc, string encryptionKey)
        {
            
            return bytesToEnc;
        }

        //should be overridden to implement the same encryption as the implant 
		public byte[] DecryptImplantTaskData(byte[] bytesToDec, string encryptionKey)
        {
            
            return bytesToDec;
        }
    }
}