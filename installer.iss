; HydroFlow Manager - Instalador para Windows
; Creado con Inno Setup
; Incluye instalación automática de LibreOffice para exportación a PDF

#define MyAppName "HydroFlow Manager"
#define MyAppVersion "1.04.1812"
#define MyAppPublisher "URBIDE"
#define MyAppURL "https://www.urbide.com/"
#define MyAppExeName "HidroFlowManager.exe"
#define MyAppIcon "source\logo.ico"

; Versión de LibreOffice a instalar
#define LibreOfficeVersion "24.2.0"
#define LibreOfficeURL "https://download.documentfoundation.org/libreoffice/stable/24.2.0/win/x86_64/LibreOffice_24.2.0_Win_x64.msi"
#define LibreOfficeInstaller "LibreOffice_Setup.msi"

[Setup]
; Información básica de la aplicación
AppId={{8A5E7F3D-9B2C-4E1A-A7D3-6F4B8C9D2E1F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=LICENSE
InfoBeforeFile=README.md
OutputDir=dist
OutputBaseFilename=HydroFlowManager_Setup_v{#MyAppVersion}
SetupIconFile={#MyAppIcon}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

; Configuración de interfaz
WizardImageFile=source\wizard_large.bmp
WizardSmallImageFile=source\wizard_small.bmp
DisableWelcomePage=no

; Directorio de salida del instalador
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode
Name: "installibreoffice"; Description: "Instalar LibreOffice (requerido para exportación a PDF)"; GroupDescription: "Componentes adicionales:"; Flags: checked

[Files]
; Ejecutable principal de HydroFlow
Source: "dist\HidroFlowManager.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTA: No use "Flags: ignoreversion" en archivos compartidos del sistema

; Archivos de recursos
Source: "source\*"; DestDir: "{app}\source"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "informes_guardados\*"; DestDir: "{app}\informes_guardados"; Flags: ignoreversion recursesubdirs createallsubdirs; AfterInstall: CreateInformesDir
Source: "output\*"; DestDir: "{app}\output"; Flags: ignoreversion recursesubdirs createallsubdirs

; Archivos de configuración y documentación
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: ".env.example"; DestDir: "{app}"; Flags: ignoreversion; DestName: ".env"

; Manuales de usuario
Source: "docs\Manual_Usuario_HydroFlow.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "docs\Manual_Informes_HydroFlow.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "docs\Guia_Tecnica_HydroFlow.md"; DestDir: "{app}\docs"; Flags: ignoreversion

[Dirs]
Name: "{app}\informes_guardados"; Permissions: users-full
Name: "{app}\output"; Permissions: users-full
Name: "{app}\source"; Permissions: users-full
Name: "{userappdata}\{#MyAppName}"; Permissions: users-full
Name: "{userappdata}\{#MyAppName}\configs"; Permissions: users-full
Name: "{userappdata}\{#MyAppName}\exports"; Permissions: users-full

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppIcon}"
Name: "{group}\Manual de Usuario"; Filename: "{app}\docs\Manual_Usuario_HydroFlow.md"; Comment: "Manual de usuario de HydroFlow Manager"
Name: "{group}\Manual de Informes"; Filename: "{app}\docs\Manual_Informes_HydroFlow.md"; Comment: "Manual del generador de informes"
Name: "{group}\Guía Técnica"; Filename: "{app}\docs\Guia_Tecnica_HydroFlow.md"; Comment: "Guía técnica para administradores"
Name: "{group}\Desinstalar {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\{#MyAppIcon}"
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon; IconFilename: "{app}\{#MyAppIcon}"

[Run]
; Instalar LibreOffice si el usuario lo seleccionó
Filename: "msiexec.exe"; Parameters: "/i ""{tmp}\{#LibreOfficeInstaller}"" /qn /norestart ADDLOCAL=ALL ALLUSERS=1 CREATEDESKTOPLINK=0 REGISTER_ALL_MSO_TYPES=0 UI_LANGS=es"; StatusMsg: "Instalando LibreOffice (esto puede tardar varios minutos)..."; Tasks: installibreoffice; Flags: waituntilterminated; Check: not LibreOfficeInstalled

; Ejecutar la aplicación al finalizar
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{userappdata}\{#MyAppName}"
Type: filesandordirs; Name: "{app}\informes_guardados"
Type: filesandordirs; Name: "{app}\output"

[Code]
var
  DownloadPage: TDownloadWizardPage;
  LibreOfficeNeeded: Boolean;

// Función para verificar si LibreOffice ya está instalado
function LibreOfficeInstalled: Boolean;
var
  LibreOfficePath: String;
begin
  Result := False;

  // Verificar en Program Files (instalación de 64 bits)
  if RegQueryStringValue(HKLM64, 'SOFTWARE\LibreOffice\LibreOffice', 'Path', LibreOfficePath) then
  begin
    Result := FileExists(LibreOfficePath + '\program\soffice.exe');
  end;

  // Verificar en Program Files (x86) (instalación de 32 bits)
  if not Result then
  begin
    if RegQueryStringValue(HKLM32, 'SOFTWARE\LibreOffice\LibreOffice', 'Path', LibreOfficePath) then
    begin
      Result := FileExists(LibreOfficePath + '\program\soffice.exe');
    end;
  end;

  // Verificar en el PATH del sistema
  if not Result then
  begin
    Result := (FindWindowByClassName('SALFRAME') <> 0) or
              FileExists(ExpandConstant('{pf}\LibreOffice\program\soffice.exe')) or
              FileExists(ExpandConstant('{pf32}\LibreOffice\program\soffice.exe'));
  end;
end;

// Función para obtener la versión de LibreOffice instalada
function GetLibreOfficeVersion: String;
var
  Version: String;
begin
  Result := '';

  if RegQueryStringValue(HKLM64, 'SOFTWARE\LibreOffice\LibreOffice', 'Version', Version) then
    Result := Version
  else if RegQueryStringValue(HKLM32, 'SOFTWARE\LibreOffice\LibreOffice', 'Version', Version) then
    Result := Version;
end;

// Inicializar la página de descarga
function OnDownloadProgress(const Url, FileName: String; const Progress, ProgressMax: Int64): Boolean;
begin
  if Progress = ProgressMax then
    Log(Format('Descarga completada. Archivo: %s', [FileName]));
  Result := True;
end;

procedure InitializeWizard;
begin
  // Crear la página de descarga
  DownloadPage := CreateDownloadPage(SetupMessage(msgWizardPreparing), SetupMessage(msgPreparingDesc), @OnDownloadProgress);

  LibreOfficeNeeded := not LibreOfficeInstalled;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
var
  VersionMsg: String;
begin
  Result := True;

  if CurPageID = wpSelectTasks then
  begin
    // Si el usuario seleccionó instalar LibreOffice pero ya está instalado
    if WizardIsTaskSelected('installibreoffice') and LibreOfficeInstalled then
    begin
      VersionMsg := GetLibreOfficeVersion;
      if VersionMsg <> '' then
        VersionMsg := ' (versión ' + VersionMsg + ')'
      else
        VersionMsg := '';

      if MsgBox('LibreOffice ya está instalado en su sistema' + VersionMsg + '.' + #13#10#13#10 +
                '¿Desea continuar sin instalar LibreOffice nuevamente?',
                mbConfirmation, MB_YESNO) = IDYES then
      begin
        // No descargar ni instalar LibreOffice
        LibreOfficeNeeded := False;
      end
      else
      begin
        Result := False;
      end;
    end;
  end
  else if CurPageID = wpReady then
  begin
    // Descargar LibreOffice si es necesario
    if WizardIsTaskSelected('installibreoffice') and LibreOfficeNeeded then
    begin
      DownloadPage.Clear;
      DownloadPage.Add('{#LibreOfficeURL}', '{#LibreOfficeInstaller}', '');
      DownloadPage.Show;
      try
        try
          DownloadPage.Download;
          Result := True;
        except
          if DownloadPage.AbortedByUser then
            Log('Descarga abortada por el usuario.')
          else
            SuppressibleMsgBox(AddPeriod(GetExceptionMessage), mbCriticalError, MB_OK, IDOK);
          Result := False;
        end;
      finally
        DownloadPage.Hide;
      end;
    end;
  end;
end;

// Crear directorio de informes guardados con permisos adecuados
procedure CreateInformesDir();
begin
  ForceDirectories(ExpandConstant('{app}\informes_guardados'));
  ForceDirectories(ExpandConstant('{userappdata}\{#MyAppName}\configs'));
  ForceDirectories(ExpandConstant('{userappdata}\{#MyAppName}\exports'));
end;

// Mensaje final personalizado
function UpdateReadyMemo(Space, NewLine, MemoUserInfoInfo, MemoDirInfo, MemoTypeInfo,
  MemoComponentsInfo, MemoGroupInfo, MemoTasksInfo: String): String;
var
  S: String;
begin
  S := '';

  S := S + MemoDirInfo + NewLine + NewLine;
  S := S + MemoGroupInfo + NewLine + NewLine;
  S := S + MemoTasksInfo + NewLine + NewLine;

  if WizardIsTaskSelected('installibreoffice') then
  begin
    if LibreOfficeInstalled then
      S := S + 'LibreOffice: Ya instalado (se omitirá la instalación)' + NewLine
    else
      S := S + 'LibreOffice: Se descargará e instalará automáticamente (~300 MB)' + NewLine;
  end
  else
  begin
    S := S + 'ADVERTENCIA: Sin LibreOffice, la exportación a PDF no estará disponible.' + NewLine;
    S := S + 'Puede instalar LibreOffice manualmente más tarde desde: https://www.libreoffice.org' + NewLine;
  end;

  Result := S;
end;

// Post-instalación: Verificar que todo está correcto
procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    Log('Instalación completada exitosamente.');

    // Verificar que LibreOffice se instaló correctamente si fue seleccionado
    if WizardIsTaskSelected('installibreoffice') and LibreOfficeNeeded then
    begin
      if LibreOfficeInstalled then
        Log('LibreOffice instalado correctamente.')
      else
        MsgBox('Advertencia: LibreOffice no se pudo instalar correctamente. ' + #13#10 +
               'La exportación a PDF puede no funcionar. ' + #13#10#13#10 +
               'Puede instalar LibreOffice manualmente desde: https://www.libreoffice.org',
               mbInformation, MB_OK);
    end;
  end;
end;
