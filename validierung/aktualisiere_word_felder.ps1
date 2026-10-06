[CmdletBinding()]
param(
    [string]$DocxPfad,
    [string]$PdfPfad,
    [string]$PythonPfad,
    [switch]$OhneInhaltsverzeichnis
)

$ErrorActionPreference = 'Stop'
if (-not $DocxPfad) { $DocxPfad = Join-Path $PSScriptRoot '..\konzept\ki-it-sicherheitskonzept.docx' }
if (-not $PdfPfad) { $PdfPfad = Join-Path $PSScriptRoot '..\konzept\ki-it-sicherheitskonzept.pdf' }
$word = $null
$dokument = $null
$pdfTemp = $null
$projektpfad = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
if (-not $PythonPfad) {
    $projektPython = Join-Path $projektpfad '.arbeitsdaten\validierungsumgebung\Scripts\python.exe'
    $PythonPfad = if ([System.IO.File]::Exists($projektPython)) { $projektPython } else { 'python' }
}

function Pruefe-Projektpfad {
    param([Parameter(Mandatory)][string]$Pfad)
    $aufgeloest = [System.IO.Path]::GetFullPath($Pfad)
    if (-not $aufgeloest.StartsWith($projektpfad + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw 'Dokumente und Exporte müssen im Projektverzeichnis bleiben.'
    }
    return $aufgeloest
}

function Loese-ZielpfadAuf {
    param([Parameter(Mandatory)][string]$Pfad)

    $vollstaendig = Pruefe-Projektpfad -Pfad $Pfad
    $verzeichnis = [System.IO.Path]::GetDirectoryName($vollstaendig)
    if (-not [System.IO.Directory]::Exists($verzeichnis)) {
        [System.IO.Directory]::CreateDirectory($verzeichnis) | Out-Null
    }
    return $vollstaendig
}

function Aktualisiere-AlleFelder {
    param([Parameter(Mandatory)]$WordDokument)

    $WordDokument.Fields.Update() | Out-Null
    foreach ($abschnitt in @($WordDokument.Sections)) {
        foreach ($kopfzeile in @($abschnitt.Headers)) {
            $kopfzeile.Range.Fields.Update() | Out-Null
        }
        foreach ($fusszeile in @($abschnitt.Footers)) {
            $fusszeile.Range.Fields.Update() | Out-Null
        }
    }
}

function Formatiere-Inhaltsverzeichnis {
    param(
        [Parameter(Mandatory)]$WordAnwendung,
        [Parameter(Mandatory)]$WordDokument
    )

    # Die negativen Kennungen sind sprachunabhängige Word-Konstanten:
    # wdStyleTOC1 = -20 und wdStyleTOC2 = -21. Dadurch werden auch auf einer
    # deutschen Word-Installation die tatsächlich vom Feld verwendeten
    # integrierten Formatvorlagen angepasst.
    $vorgaben = @(
        @{ Kennung = -20; Groesse = 10.5; Fett = $true;  EinzugCm = 0.0; Davor = 1; Danach = 1 },
        @{ Kennung = -21; Groesse = 10.0; Fett = $false; EinzugCm = 0.6; Davor = 0; Danach = 0 }
    )
    foreach ($vorgabe in $vorgaben) {
        $stil = $WordDokument.Styles.Item($vorgabe.Kennung)
        $stil.AutomaticallyUpdate = $false
        $stil.Font.Name = 'Calibri'
        $stil.Font.Size = $vorgabe.Groesse
        $stil.Font.Bold = [int]$vorgabe.Fett * -1
        $stil.ParagraphFormat.Alignment = 0 # wdAlignParagraphLeft
        $stil.ParagraphFormat.LeftIndent = $WordAnwendung.CentimetersToPoints($vorgabe.EinzugCm)
        $stil.ParagraphFormat.FirstLineIndent = 0
        $stil.ParagraphFormat.SpaceBefore = $vorgabe.Davor
        $stil.ParagraphFormat.SpaceAfter = $vorgabe.Danach
        $stil.ParagraphFormat.LineSpacingRule = 0 # wdLineSpaceSingle
        $stil.ParagraphFormat.TabStops.ClearAll()
        $stil.ParagraphFormat.TabStops.Add(
            $WordAnwendung.CentimetersToPoints(16),
            2, # wdAlignTabRight
            1  # wdTabLeaderDots
        ) | Out-Null
    }
}

try {
    $docx = Pruefe-Projektpfad -Pfad $DocxPfad
    if (-not [System.IO.File]::Exists($docx)) {
        throw "DOCX-Masterdokument fehlt: $docx"
    }
    $pdf = Loese-ZielpfadAuf -Pfad $PdfPfad
    $pruefskript = Join-Path $PSScriptRoot 'erzeuge_dokumente.py'
    & $PythonPfad $pruefskript --pruefe-pdf-zielschutz $pdf
    if ($LASTEXITCODE -ne 0) {
        throw 'PDF-Export abgebrochen: das vorhandene Ziel ist befüllt, signiert oder geschützt.'
    }
    $pdfTemp = Loese-ZielpfadAuf -Pfad (Join-Path ([System.IO.Path]::GetDirectoryName($pdf)) ('.' + [System.IO.Path]::GetFileNameWithoutExtension($pdf) + '.' + [guid]::NewGuid().ToString('N') + '.tmp.pdf'))

    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0

    $dokument = $word.Documents.Open($docx, $false, $false)
    # Word darf den lokalen Kontonamen beim Speichern nicht als Bearbeiter eintragen.
    $dokument.RemovePersonalInformation = $true
    $erwarteteVerzeichnisse = if ($OhneInhaltsverzeichnis) { 0 } else { 1 }
    if ($dokument.TablesOfContents.Count -ne $erwarteteVerzeichnisse) {
        throw "Das Masterdokument muss $erwarteteVerzeichnisse Word-Inhaltsverzeichnis(se) enthalten."
    }

    # Dokumentweit geltende deutsche Silbentrennung. Word normalisiert beim
    # Speichern Teile des zugrunde liegenden OOXML; die COM-Eigenschaften sind
    # deshalb die maßgebliche Einstellung für die veröffentlichte Fassung.
    $dokument.AutoHyphenation = $true
    $dokument.ConsecutiveHyphensLimit = 2
    $dokument.HyphenationZone = $word.CentimetersToPoints(0.635)

    if (-not $OhneInhaltsverzeichnis) {
        $dokument.TablesOfContents.Item(1).Update()
        Formatiere-Inhaltsverzeichnis -WordAnwendung $word -WordDokument $dokument
    }
    $dokument.Repaginate()
    Aktualisiere-AlleFelder -WordDokument $dokument
    if (-not $OhneInhaltsverzeichnis) { $dokument.TablesOfContents.Item(1).UpdatePageNumbers() }
    $dokument.Repaginate()
    Aktualisiere-AlleFelder -WordDokument $dokument
    $dokument.Save()

    # 17 entspricht wdExportFormatPDF. Die PDF-Lesefassung wird ausschließlich
    # aus dem zuvor gespeicherten und aktualisierten DOCX-Master erzeugt.
    # Der Export behält Titel und Sachmetadaten des bereinigten Dokuments.
    # Diese Umschaltung wird nicht in das DOCX zurückgespeichert.
    $dokument.RemovePersonalInformation = $false
    $dokument.ExportAsFixedFormat($pdfTemp, 17, $false, 0, 0, 1, 1, 0, $true)
    & $PythonPfad $pruefskript --pruefe-pdf-zielschutz $pdf
    if ($LASTEXITCODE -ne 0) {
        throw 'PDF-Export abgebrochen: das Ziel wurde während des Exports befüllt, signiert oder geschützt.'
    }
    Move-Item -LiteralPath $pdfTemp -Destination $pdf -Force
    $pdfTemp = $null
    Write-Host "Word-Felder aktualisiert und DOCX gespeichert: $docx"
    Write-Host "PDF aus diesem DOCX erzeugt: $pdf"
}
finally {
    if ($null -ne $dokument) {
        $dokument.Close($false)
        [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($dokument)
    }
    if ($null -ne $word) {
        $word.Quit()
        [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($word)
    }
    if ($null -ne $pdfTemp -and [System.IO.File]::Exists($pdfTemp)) {
        Remove-Item -LiteralPath $pdfTemp -Force
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
