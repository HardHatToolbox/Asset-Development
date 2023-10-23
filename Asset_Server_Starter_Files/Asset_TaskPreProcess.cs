using HardHatCore.ApiModels.Plugin_BaseClasses;
using System;
using System.Collections.Generic;
using System.ComponentModel.Composition;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using HardHatCore.TeamServer.Models.Extras;
using HardHatCore.TeamServer.Plugin_Interfaces;
using HardHatCore.TeamServer.Services;
using HardHatCore.TeamServer.Services.Handle_Implants;
using HardHatCore.TeamServer.Utilities;
using HardHatCore.TeamServer.Plugin_Interfaces.Ext_Implants;
using HardHatCore.TeamServer.Plugin_BaseClasses;

namespace Asset_ServerPlugin
{
    [Export(typeof(IExtImplant_TaskPreProcess))]
    [ExportMetadata("Name", "Asset")]
    [ExportMetadata("Description", "Task pre processing for the Asset Implant")]
    public class Asset_TaskPreProcess : IExtImplant_TaskPreProcess
    {
        private readonly ExtImplant_TaskPreProcess_Base extImplant_TaskPreProcess_Base = new();

        //by default task objects mark if they need to be preprocessed, if you want to change this behavior, you can do it here
        public virtual bool DetermineIfTaskPreProc(ExtImplantTask_Base task)
        {
            return extImplant_TaskPreProcess_Base.DetermineIfTaskPreProc(task);
        }

        //if you want to do something before a task is sent to the implant, you can do it here
        public virtual void PreProcessTask(ExtImplantTask_Base task, ExtImplant_Base implant)
        {
            extImplant_TaskPreProcess_Base.PreProcessTask(task, implant);
        }
    }
}