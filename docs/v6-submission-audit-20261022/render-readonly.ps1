$ErrorActionPreference='Stop'
$reportPath=Join-Path $PSScriptRoot 'inspection-copy.docx'
$pdfPath=Join-Path $PSScriptRoot 'native-inspection.pdf'
$wordApp=New-Object -ComObject Word.Application
$wordApp.Visible=$false
$wordApp.DisplayAlerts=0
$wordApp.AutomationSecurity=3
$reportDoc=$null
try {
    $reportDoc=$wordApp.Documents.Open($reportPath,$false,$true)
    $reportDoc.Repaginate()
    $headingPages=@()
    foreach($paragraph in $reportDoc.Paragraphs){
        if($paragraph.OutlineLevel -le 2){
            $headingPages += [pscustomobject]@{heading=$paragraph.Range.Text.Trim();page=$paragraph.Range.Information(3)}
        }
    }
    $reportDoc.ExportAsFixedFormat($pdfPath,17)
    [pscustomobject]@{
        pages=$reportDoc.ComputeStatistics(2)
        tables=$reportDoc.Tables.Count
        inlineShapes=$reportDoc.InlineShapes.Count
        headings=$headingPages
        pdf=$pdfPath
    } | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'word-native-check.json') -Encoding utf8
    Write-Output ('Pages='+$reportDoc.ComputeStatistics(2)+'; Tables='+$reportDoc.Tables.Count+'; Figures='+$reportDoc.InlineShapes.Count)
} finally {
    if($reportDoc){$reportDoc.Close(0)}
    $wordApp.Quit(0)
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($wordApp)
}
