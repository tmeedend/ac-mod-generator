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
DisableDirPage=no
OutputDir=installer\installer-bin
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Files]
Source: "..\deps\*"; DestDir: "{app}\deps\"; Flags: ignoreversion recursesubdirs createallsubdirs  
Source: "..\examples\*"; DestDir: "{app}\examples\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\export-as-mod.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\configuration.ini"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\ModPackager.bat"; DestDir: "{app}"; Flags: ignoreversion ; AfterInstall: WriteBatFile()
Source: "..\AC.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\actools\*.py"; DestDir: "{app}\actools\"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files


[Registry]             
Root: HKCU; Subkey: "Software\Classes\*\shell\Assetto Corsa Mod"; Flags: uninsdeletekeyifempty; ValueType: string; ValueName: "icon"; ValueData: "{app}\AC.ico"
Root: HKCU; Subkey: "Software\Classes\*\shell\Assetto Corsa Mod\command"; Flags: uninsdeletekeyifempty; ValueType: string; ValueName: ""; ValueData: "{app}\ModPackager.bat ""%1"""  

Root: HKCU; Subkey: "Software\Classes\directory\shell\Assetto Corsa Mod"; Flags: uninsdeletekeyifempty; ValueType: string; ValueName: "icon"; ValueData: "{app}\AC.ico"
Root: HKCU; Subkey: "Software\Classes\directory\shell\Assetto Corsa Mod\command"; Flags: uninsdeletekeyifempty; ValueType: string; ValueName: ""; ValueData: "{app}\ModPackager.bat ""%1"""

[INI]
Filename: {app}\configuration.ini; Section: SETTINGS; Key: ASSETTOCORSA_PATH; String: {code:GetACPath}
Filename: {app}\configuration.ini; Section: SETTINGS; Key: 7ZIP_EXEC; String: {app}\deps\7zip\7z.exe
Filename: {app}\configuration.ini; Section: SETTINGS; Key: QUICKBMS_EXE; String: {app}\deps\quickbms.exe


[code]
var
ACDirPage : TInputDirWizardPage; 
InstallationPath: string;

function GetInstallationPath(): string;
begin
  { Detected path is cached, as this gets called multiple times }
  if InstallationPath = '' then
  begin
    if RegQueryStringValue(
         HKLM64, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 244210',
         'InstallLocation', InstallationPath) then
    begin
      Log('Detected Steam installation: ' + InstallationPath);
    end
      else
    begin
      InstallationPath := 'C:\Program Files (x86)\Steam\steamapps\common\assettocorsa';
      Log('No installation detected, using the default path: ' + InstallationPath);
    end;
  end;
  Result := InstallationPath;
end;


function BoolToStr(Value: Boolean): String; 
begin
  if Value then
    Result := 'Yes'
  else
    Result := 'No';
end;

procedure InitializeWizard;
begin
ACDirPage  := CreateInputDirPage(wpSelectDir,
  'Select Assetto Corsa directtory', 'This information is used to be able to generate 7zip archives from your installed Assetto Corsa mods. It''s not required if you only use this tool to generate mods from downloaded mods.', 'Your assettocorsa directory should be in the folder steamapps\common of your Steam installation.', True, '');   
  ACDirPage.Add('Select assettocorsa directory:');
  ACDirPage.Values[0] := GetInstallationPath();
end;

function GetACPath(Param: String): string;
begin
 result :=  ACDirPage.Values[0];
end;

procedure WriteBatFile();
var
  lines : TArrayOfString;
  Res : Boolean;
begin
  SetArrayLength(lines, 3);      
  lines[0] := '@echo off';              
  lines[1] := 'set ACMPPATH=' + ExpandConstant('{app}');
  lines[2] := 'set PYTHONPATH=' + ExpandConstant('{app}') + '\deps\python\';
  Res := SaveStringsToFile(ExpandConstant('{app}') + '\env.bat',lines,true);
end;