; Script de Inno Setup personalizado para "Atrapa las Estrellitas"
[Setup]
AppName=Atrapa las Estrellitas
AppVersion=1.0
DefaultDirName={pf}\AtrapaLasEstrellitas
DefaultGroupName=Atrapa las Estrellitas
OutputDir=dist
OutputBaseFilename=AtrapaLasEstrellitas-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
DisableDirPage=no
SetupIconFile=Ico\ico.ico
WizardImageFile=src\Fondo.bmp
WizardSmallImageFile=Logo\Logo.bmp

[Files]
Source: "dist\AtrapaLasEstrellitas\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Atrapa las Estrellitas"; Filename: "{app}\AtrapaLasEstrellitas.exe"
Name: "{userdesktop}\Atrapa las Estrellitas"; Filename: "{app}\AtrapaLasEstrellitas.exe"

[Run]
Filename: "{app}\AtrapaLasEstrellitas.exe"; Description: "Iniciar Atrapa las Estrellitas"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Messages]
WelcomeLabel1=¡Bienvenido al instalador de Atrapa las Estrellitas!
WelcomeLabel2=Este asistente instalará el juego arcade más estelar en tu PC.
FinishedLabel=¡Instalación completada! Puedes iniciar el juego desde el menú inicio o el escritorio.

[CustomMessages]
AppWelcome=¡Gracias por elegir Atrapa las Estrellitas!
