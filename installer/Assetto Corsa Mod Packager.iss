; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Assetto Corsa Mod Packager"
#define MyAppVersion "0.5"
#define MyAppPublisher "Chez Theo"
#define MyAppURL "https://github.com/tmeedend/ac-mod-generator"
#define MyAppExeName "python.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{ED3DF8A1-5729-4949-B5F0-05E48FB6F139}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\AssettoCorsaModPackager
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=..\LICENSE
InfoBeforeFile=before-install.txt
InfoAfterFile=after-install.txt
; Remove the following line to run in administrative install mode (install for all users.)
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=commandline
OutputDir=installer\installer-bin
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Files]
Source: "..\deps\*"; DestDir: "{app}\deps\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\export-as-mod.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\actools-config.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\ModPackager.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\AC.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\actools\*.py"; DestDir: "{app}\actools\"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files


[Registry]             
Root: HKCU; Subkey: "Software\Classes\*\shell\Assetto Corsa Mod"; Flags: uninsdeletekeyifempty; ValueType: string; ValueName: "icon"; ValueData: "{app}\AC.ico"
Root: HKCU; Subkey: "Software\Classes\*\shell\Assetto Corsa Mod\command"; Flags: uninsdeletekeyifempty; ValueType: string; ValueName: ""; ValueData: "{app}\ModPackager.bat %1"  

Root: HKCU; Subkey: "Software\Classes\directory\shell\Assetto Corsa Mod"; Flags: uninsdeletekeyifempty; ValueType: string; ValueName: "icon"; ValueData: "{app}\AC.ico"
Root: HKCU; Subkey: "Software\Classes\directory\shell\Assetto Corsa Mod\command"; Flags: uninsdeletekeyifempty; ValueType: string; ValueName: ""; ValueData: "{app}\ModPackager.bat %1"
