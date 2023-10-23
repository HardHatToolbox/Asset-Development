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
    [Export(typeof(IExtImplant_TaskPostProcess))]
    [ExportMetadata("Name", "Asset")]
    [ExportMetadata("Description", "Task post processing for the Asset Implant")]
    public class Asset_TaskPostProcess : IExtImplant_TaskPostProcess
    {
        private readonly ExtImplant_TaskPostProcess_Base extImplant_TaskPostProcess_Base = new();

        public virtual bool DetermineIfTaskPostProc(ExtImplantTask_Base task)
        {
            return extImplant_TaskPostProcess_Base.DetermineIfTaskPostProc(task);
        }

        //if you want to do something after a task response comes back from the implant, you can do it here
        public virtual async Task PostProcessTask(IEnumerable<ExtImplantTaskResult_Base> results, ExtImplantTaskResult_Base result, ExtImplant_Base extImplant, ExtImplantTask_Base task)
        {
            await extImplant_TaskPostProcess_Base.PostProcessTask(results, result, extImplant, task);
        }
    }
}