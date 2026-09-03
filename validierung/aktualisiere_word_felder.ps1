[CmdletBinding()]
param(
    [string]$DocxPfad = (Join-Path $PSScriptRoot '..\konzept\ki-it-sicherheitskonzept.docx'),
    [string]$PdfPfad = (Join-Path $PSScriptRoot '..\konzept\ki-it-sicherheitskonzept.pdf')
)

$ErrorActionPreference = 'Stop'
$word = $null
$dokument = $null

function Loese-ZielpfadAuf {
    param([Parameter(Mandatory)][string]$Pfad)

    $vollstaendig = [System.IO.Path]::GetFullPath($Pfad)
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
        @{ Kennung = -20; Groesse = 10.5; Fett = $true;  EinzugCm = 0.0; Davor = 2; Danach = 3 },
        @{ Kennung = -21; Groesse = 10.0; Fett = $false; EinzugCm = 0.6; Davor = 0; Danach = 2 }
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
    $docx = [System.IO.Path]::GetFullPath($DocxPfad)
    if (-not [System.IO.File]::Exists($docx)) {
        throw "DOCX-Masterdokument fehlt: $docx"
    }
    $pdf = Loese-ZielpfadAuf -Pfad $PdfPfad

    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0

    $dokument = $word.Documents.Open($docx, $false, $false)
    if ($dokument.TablesOfContents.Count -ne 1) {
        throw "Das Masterdokument muss genau ein Word-Inhaltsverzeichnis enthalten."
    }

    # Dokumentweit geltende deutsche Silbentrennung. Word normalisiert beim
    # Speichern Teile des zugrunde liegenden OOXML; die COM-Eigenschaften sind
    # deshalb die maßgebliche Einstellung für die veröffentlichte Fassung.
    $dokument.AutoHyphenation = $true
    $dokument.ConsecutiveHyphensLimit = 2
    $dokument.HyphenationZone = $word.CentimetersToPoints(0.635)

    $dokument.TablesOfContents.Item(1).Update()
    Formatiere-Inhaltsverzeichnis -WordAnwendung $word -WordDokument $dokument
    $dokument.Repaginate()
    Aktualisiere-AlleFelder -WordDokument $dokument
    $dokument.TablesOfContents.Item(1).UpdatePageNumbers()
    $dokument.Repaginate()
    Aktualisiere-AlleFelder -WordDokument $dokument
    $dokument.Save()

    # 17 entspricht wdExportFormatPDF. Die PDF-Lesefassung wird ausschließlich
    # aus dem zuvor gespeicherten und aktualisierten DOCX-Master erzeugt.
    $dokument.ExportAsFixedFormat($pdf, 17)
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
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
