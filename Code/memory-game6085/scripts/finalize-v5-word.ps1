param([string]$PdfName='native-final.pdf')
$ErrorActionPreference='Stop'
$workspaceRoot=[System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../..'))
$reportPath=Join-Path $workspaceRoot 'docs/v5-report-work/20261022-docker-lab-report-v5.docx'
$pdfPath=Join-Path $workspaceRoot ('docs/v5-report-work/'+$PdfName)
$wordApp=New-Object -ComObject Word.Application
$wordApp.Visible=$false
$wordApp.DisplayAlerts=0
$wordApp.AutomationSecurity=3
$reportDoc=$null
try {
    $reportDoc=$wordApp.Documents.Open($reportPath,$false,$false)
    $reportDoc.Repaginate()
    [void]$reportDoc.Fields.Update()
    foreach($toc in $reportDoc.TablesOfContents){$toc.Update()}
    $reportDoc.Repaginate()
    foreach($toc in $reportDoc.TablesOfContents){$toc.UpdatePageNumbers()}
    $reportDoc.Save()
    $headingPages=@()
    foreach($paragraph in $reportDoc.Paragraphs){
        $level=$paragraph.OutlineLevel
        if($level -le 2){
            $headingPages += [pscustomobject]@{heading=$paragraph.Range.Text.Trim();level=$level;page=$paragraph.Range.Information(3)}
        }
    }
    $tocText=@()
    foreach($toc in $reportDoc.TablesOfContents){$tocText += $toc.Range.Text}
    $reportDoc.ExportAsFixedFormat($pdfPath,17)
    [pscustomobject]@{
        pages=$reportDoc.ComputeStatistics(2)
        tables=$reportDoc.Tables.Count
        inlineShapes=$reportDoc.InlineShapes.Count
        tablesOfContents=$reportDoc.TablesOfContents.Count
        headings=$headingPages
        tocText=$tocText
        pdf=$pdfPath
    } | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $workspaceRoot 'docs/v5-report-work/word-native-check.json') -Encoding utf8
    Write-Output ('Pages='+$reportDoc.ComputeStatistics(2)+'; Tables='+$reportDoc.Tables.Count+'; Figures='+$reportDoc.InlineShapes.Count)
    Write-Output $pdfPath
} finally {
    if($reportDoc){$reportDoc.Close(0)}
    $wordApp.Quit(0)
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($wordApp)
}
