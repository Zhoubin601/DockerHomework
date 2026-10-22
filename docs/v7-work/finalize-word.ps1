param([string]$PdfName='native-final.pdf')
$ErrorActionPreference='Stop'
$candidatePath=Join-Path $PSScriptRoot '20261022-docker-lab-report-v7.docx'
$reportPath=Join-Path $PSScriptRoot 'word-input.docx'
$finalPath=Join-Path $PSScriptRoot 'word-final.docx'
Copy-Item -LiteralPath $candidatePath -Destination $reportPath
$pdfPath=Join-Path $PSScriptRoot $PdfName
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
    $reportDoc.SaveAs2($finalPath,16)
    $headingPages=@()
    foreach($paragraph in $reportDoc.Paragraphs){
        if($paragraph.OutlineLevel -le 2){
            $headingPages += [pscustomobject]@{heading=$paragraph.Range.Text.Trim();level=$paragraph.OutlineLevel;page=$paragraph.Range.Information(3)}
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
    } | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'word-native-check.json') -Encoding utf8
    Write-Output ('Pages='+$reportDoc.ComputeStatistics(2)+'; Tables='+$reportDoc.Tables.Count+'; Figures='+$reportDoc.InlineShapes.Count)
} finally {
    if($reportDoc){$reportDoc.Saved=$true; $reportDoc.Close()}
    $wordApp.Quit()
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($wordApp)
}
