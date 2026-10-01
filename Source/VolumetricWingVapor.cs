using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using UnityEngine;
using VortexVapor;
using Debug = UnityEngine.Debug;

namespace VolumetricWingVapor
{
    // The player's choices, saved to GameData/<mod>/PluginData/settings.cfg.
    public static class Settings
    {
        public static bool On { get; private set; }
        // Scales how far the cloud stands off the wing (VaporVolume.CloudHeightChords).
        public static float Thickness { get; private set; }

        // Set by Set; the addon saves shortly after the last change.
        public static bool Dirty;
        public static float ChangedAt;

        static bool loaded;

        static Settings() { On = true; Thickness = 1f; }

        public static void Set(bool on, float thickness)
        {
            thickness = Mathf.Clamp(thickness, 0f, ModSettings.MaxIntensity);
            if (on == On && thickness == Thickness) return;
            On = on;
            Thickness = thickness;
            Dirty = true;
            ChangedAt = Time.unscaledTime;
        }

        public static void Reset() { Set(true, 1f); }

        public static void Load()
        {
            if (loaded) return;
            loaded = true;
            try
            {
                string path = FilePath();
                if (path == null || !File.Exists(path)) return;
                ConfigNode node = ConfigNode.Load(path);
                if (node == null) return;
                bool on;
                float thickness;
                if (bool.TryParse(node.GetValue("volumetric"), out on)) On = on;
                if (float.TryParse(node.GetValue("thickness"), NumberStyles.Float, CultureInfo.InvariantCulture, out thickness))
                    Thickness = Mathf.Clamp(thickness, 0f, ModSettings.MaxIntensity);
            }
            catch (Exception e) { Debug.Log("[VolumetricWingVapor] settings: could not read, using defaults: " + e.Message); }
        }

        public static void Save()
        {
            Dirty = false;
            try
            {
                string path = FilePath();
                if (path == null) return;
                Directory.CreateDirectory(Path.GetDirectoryName(path));
                var node = new ConfigNode("VolumetricWingVaporSettings");
                node.AddValue("volumetric", On.ToString());
                node.AddValue("thickness", Thickness.ToString("F2", CultureInfo.InvariantCulture));
                node.Save(path);
            }
            catch (Exception e) { Debug.Log("[VolumetricWingVapor] settings: could not save: " + e.Message); }
        }

        // Next to the Plugins folder.
        static string FilePath()
        {
            string plugins = Path.GetDirectoryName(typeof(Settings).Assembly.Location);
            string root = plugins != null ? Path.GetDirectoryName(plugins) : null;
            return root != null ? Path.Combine(Path.Combine(root, "PluginData"), "settings.cfg") : null;
        }
    }

    // Draws Wingtip Vortex's wing vapor as a cloud in place of its puffs, and adds this mod's
    // settings to Wingtip Vortex's window.
    [KSPAddon(KSPAddon.Startup.Flight, false)]
    public class VolumetricVaporAddon : MonoBehaviour, VaporRenderer.IDrawer
    {
        const float SaveDelay = 1f;   // s after the last change

        readonly VaporVolume volume = new VaporVolume();

        void Start()
        {
            Settings.Load();
            VaporRenderer.Drawer = this;
            ModSettings.VaporRows += Rows;
            ModSettings.Defaults += Settings.Reset;
            Debug.Log("[VolumetricWingVapor] v" + typeof(Settings).Assembly.GetName().Version.ToString(3) + " starting");
        }

        void OnDestroy()
        {
            if (ReferenceEquals(VaporRenderer.Drawer, this)) VaporRenderer.Drawer = null;
            ModSettings.VaporRows -= Rows;
            ModSettings.Defaults -= Settings.Reset;
            volume.Clear();
            if (Settings.Dirty) Settings.Save();
        }

        void Update()
        {
            // One write after a slider drag, not hundreds.
            if (Settings.Dirty && Time.unscaledTime - Settings.ChangedAt > SaveDelay) Settings.Save();
        }

        public bool Draw(List<VaporRenderer.Source> active, Vessel vessel, Vector3 down, Color tint, float scale, float dt)
        {
            if (!Settings.On || !VaporVolume.Available)
            {
                volume.Hide();
                return false;
            }
            volume.Update(active, vessel, down, tint, scale, Settings.Thickness, dt);
            return true;
        }

        public void Clear() { volume.Clear(); }

        // Under the wing vapor's rows in Wingtip Vortex's settings window.
        void Rows(bool vaporOn)
        {
            bool usable = VaporVolume.Available;
            float thickness = ModSettingsWindow.IntensityRow("Thickness", Settings.Thickness, vaporOn && Settings.On && usable);
            bool on = Settings.On;
            if (usable) on = GUILayout.Toggle(on, " Volumetric cloud (Waterfall)");
            else GUILayout.Label("Volumetric cloud needs Waterfall installed.");
            Settings.Set(on, thickness);
        }
    }
}
