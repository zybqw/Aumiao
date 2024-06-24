; 脚本由 Inno Setup 脚本向导 生成！
; 有关创建 Inno Setup 脚本文件的详细资料请查阅帮助文档！

#define MyAppName "Aumiao"
#define MyAppVersion "1.12.5"
#define MyAppPublisher "Aurzex"
#define MyAppURL "https://github.com/zybqw/Aumiao"
#define MyAppExeName "Aumiao.exe"

[Setup]
; 注: AppId的值为单独标识该应用程序。
; 不要为其他安装程序使用相同的AppId值。
; (若要生成新的 GUID，可在菜单中点击 "工具|生成 GUID"。)
AppId={{EBD53CA5-159B-4FCF-B4CF-7546CE1CE412}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName=D:/{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; 移除以下行，以在管理安装模式下运行（为所有用户安装）。
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=F:\
OutputBaseFilename=Aumiao Setup
SetupIconFile=E:\zybqw\zybqw_files\编程猫\luo.ico
Password=Aumiao
Encryption=yes
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "chinesesimp"; MessagesFile: "compiler:Default.isl"
Name: "english"; MessagesFile: "compiler:Languages\English.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "E:\zybqw\zybqw_files\编程猫\out\Aumiao.dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\zybqw\zybqw_files\编程猫\out\Aumiao.dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; 注意: 不要在任何共享系统文件上使用“Flags: ignoreversion”

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:ProgramOnTheWeb,{#MyAppName}}"; Filename: "{#MyAppURL}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

