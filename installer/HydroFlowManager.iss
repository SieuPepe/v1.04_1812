; ============================================================================
; HydroFlow Manager v1.04 - Inno Setup Script
; ============================================================================
;
; Script de instalación profesional para HydroFlow Manager v1.04
; Genera un instalador .exe con todas las dependencias incluidas
;
; Requisitos:
;   - Inno Setup 6.0+ instalado (https://jrsoftware.org/isdl.php)
;   - HydroFlowManager.exe compilado en dist\
;   - HydroFlowManager_Config.exe compilado en dist\
;
; Uso:
;   Compilar con Inno Setup Compiler o ejecutar:
;   "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" HydroFlowManager.iss
;
; ============================================================================

#define MyAppName "HydroFlow Manager"
#define MyAppVersion "1.04"
#define MyAppPublisher "HydroFlow"
#define MyAppExeName "HydroFlowManager.exe"
#define MyAppConfigExeName "HydroFlowManager_Config.exe"

[Setup]
; Información básica de la aplicación
AppId={{8A5D2F3E-9B4C-4D6E-8F1A-2C3B4D5E6F7A}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes

; Archivo de salida
OutputDir=..\dist
OutputBaseFilename=HydroFlowManager_v{#MyAppVersion}_Setup
SetupIconFile=..\resources\images\logo.ico

; Compresión
Compression=lzma2/max
SolidCompression=yes

; Privilegios
PrivilegesRequired=admin

; Interfaz moderna
WizardStyle=modern
WizardSizePercent=120

; Idioma
ShowLanguageDialog=no

; Desinstalación
UninstallDisplayIcon={app}\{#MyAppExeName}

; Información de licencia y documentación
LicenseFile=..\LICENSE.txt
InfoBeforeFile=..\installer\LEER_ANTES_DE_INSTALAR.txt
InfoAfterFile=..\installer\LEER_DESPUES_DE_INSTALAR.txt

; Arquitectura
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "quicklaunchicon"; Description: "Crear icono en inicio rapido"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
; Ejecutable principal
Source: "..\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Asistente de configuración
Source: "..\dist\{#MyAppConfigExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Recursos (si existen)
#ifexist "..\resources"
Source: "..\resources\*"; DestDir: "{app}\resources"; Flags: ignoreversion recursesubdirs createallsubdirs
#endif

; Documentación
#ifexist "..\README.md"
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
#endif
#ifexist "..\INSTALACION.md"
Source: "..\INSTALACION.md"; DestDir: "{app}"; Flags: ignoreversion
#endif
#ifexist "..\LICENSE.txt"
Source: "..\LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
#endif

; Archivo .env.example para referencia
#ifexist "..\.env.example"
Source: "..\.env.example"; DestDir: "{app}"; Flags: ignoreversion
#endif

[Icons]
; Menú inicio
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Configurar {#MyAppName}"; Filename: "{app}\{#MyAppConfigExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

; Escritorio
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

; Inicio rápido
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
; Ejecutar asistente de configuración después de la instalación
Filename: "{app}\{#MyAppConfigExeName}"; Parameters: """{app}"""; Description: "Configurar conexión a base de datos"; Flags: postinstall nowait skipifsilent

; Opción para ejecutar la aplicación inmediatamente
Filename: "{app}\{#MyAppExeName}"; Description: "Ejecutar {#MyAppName}"; Flags: postinstall nowait skipifsilent unchecked

[UninstallDelete]
; Eliminar archivo .env al desinstalar (contiene credenciales)
Type: files; Name: "{app}\.env"

[Code]
// ============================================================================
// Código Pascal para validaciones y lógica personalizada
// ============================================================================

var
  MySQLCheckPage: TOutputMsgWizardPage;
  ConfigCheckPage: TInputQueryWizardPage;

// Verificar si MySQL está instalado y corriendo
function CheckMySQL: Boolean;
var
  ResultCode: Integer;
  MySQLPaths: array[0..2] of String;
  i: Integer;
  MySQLFound: Boolean;
begin
  Result := True;  // Por defecto continuar instalación
  MySQLFound := False;

  // Rutas comunes de MySQL
  MySQLPaths[0] := 'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe';
  MySQLPaths[1] := 'C:\xampp\mysql\bin\mysql.exe';
  MySQLPaths[2] := 'C:\wamp64\bin\mysql\mysql8.0.30\bin\mysql.exe';

  // Verificar si MySQL está en alguna ruta común
  for i := 0 to 2 do
  begin
    if FileExists(MySQLPaths[i]) then
    begin
      MySQLFound := True;
      Break;
    end;
  end;

  if not MySQLFound then
  begin
    // Intentar ejecutar mysql desde PATH
    if Exec('cmd.exe', '/c mysql --version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
    begin
      if ResultCode = 0 then
        MySQLFound := True;
    end;
  end;

  Result := MySQLFound;
end;

// Crear página de verificación de MySQL
procedure InitializeWizard;
begin
  MySQLCheckPage := CreateOutputMsgPage(wpWelcome,
    'Verificación de Requisitos Previos',
    'Verificando que MySQL/MariaDB esté instalado',
    'HydroFlow Manager requiere que MySQL o MariaDB esté instalado y corriendo antes de continuar con la instalación.' + #13#10 + #13#10 +
    'IMPORTANTE:' + #13#10 +
    '• MySQL/MariaDB debe estar instalado ANTES de continuar' + #13#10 +
    '• El servicio MySQL debe estar corriendo' + #13#10 +
    '• Debe tener las credenciales de acceso disponibles' + #13#10 +
    '• La base de datos HydroFlow debe estar creada e importada' + #13#10 + #13#10 +
    'El instalador verificará estos requisitos en la siguiente pantalla.');
end;

// Verificar antes de proceder
function NextButtonClick(CurPageID: Integer): Boolean;
var
  MySQLInstalled: Boolean;
  ErrorMsg: String;
begin
  Result := True;

  if CurPageID = MySQLCheckPage.ID then
  begin
    MySQLInstalled := CheckMySQL;

    if not MySQLInstalled then
    begin
      ErrorMsg := 'No se detectó MySQL/MariaDB en el sistema.' + #13#10 + #13#10 +
                  'HydroFlow Manager requiere MySQL/MariaDB para funcionar.' + #13#10 + #13#10 +
                  'Opciones:' + #13#10 +
                  '1. Instale MySQL/MariaDB antes de continuar' + #13#10 +
                  '2. Continúe la instalación (podrá configurar MySQL más tarde)' + #13#10 + #13#10 +
                  '¿Desea continuar de todos modos?';

      Result := MsgBox(ErrorMsg, mbConfirmation, MB_YESNO) = IDYES;
    end;
  end;
end;

// Mensaje después de la instalación
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // La configuración se ejecutará automáticamente por [Run] PostInstall
    // No es necesario hacer nada aquí
  end;
end;
