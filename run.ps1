param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$CmdArgs
)

$ErrorActionPreference = "Stop"

if (Test-Path "venv\Scripts\python.exe") {
    & "venv\Scripts\python.exe" "scripts\run.py" @CmdArgs
} else {
    & python "scripts\run.py" @CmdArgs
}

exit $LASTEXITCODE
