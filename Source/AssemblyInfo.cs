using System.Reflection;

[assembly: AssemblyTitle("VolumetricWingVapor")]
[assembly: AssemblyProduct("VolumetricWingVapor")]
[assembly: AssemblyCopyright("Copyright (c) 2026 PogKai")]
[assembly: AssemblyVersion("1.0.0.0")]
[assembly: AssemblyFileVersion("1.0.0.0")]

// KSP loads this after Wingtip Vortex, and not at all without it.
[assembly: KSPAssembly("VolumetricWingVapor", 1, 0)]
[assembly: KSPAssemblyDependency("WingtipVortex", 1, 5)]
