$ErrorActionPreference='Stop'
$inputPath=Join-Path $PSScriptRoot 'candidate-v8.docx'
$finalPath=Join-Path $PSScriptRoot 'word-final.docx'
$pdfPath=Join-Path $PSScriptRoot 'native-final.pdf'
if(Test-Path -LiteralPath $finalPath){throw 'Final working file already exists.'}
$wordApp=New-Object -ComObject Word.Application
$wordApp.Visible=$false
$wordApp.DisplayAlerts=0
$wordApp.AutomationSecurity=3
$reportDoc=$null
try {
    $reportDoc=$wordApp.Documents.Open($inputPath,$false,$false)
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
    $figurePages=@()
    foreach($shape in $reportDoc.InlineShapes){$figurePages += $shape.Range.Information(3)}
    $captionPages=@()
    foreach($paragraph in $reportDoc.Paragraphs){
        $captionText=$paragraph.Range.Text.Trim()
        if($captionText -match '^图(\d+|A\d+)'){$captionPages += [pscustomobject]@{text=$captionText;page=$paragraph.Range.Information(3)}}
    }
    $tocText=@()
    foreach($toc in $reportDoc.TablesOfContents){$tocText += $toc.Range.Text}
    $reportDoc.ExportAsFixedFormat($pdfPath,17)
    [pscustomobject]@{pages=$reportDoc.ComputeStatistics(2);tables=$reportDoc.Tables.Count;inlineShapes=$reportDoc.InlineShapes.Count;tablesOfContents=$reportDoc.TablesOfContents.Count;headings=$headingPages;figurePages=$figurePages;captionPages=$captionPages;tocText=$tocText} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'word-native-check.json') -Encoding utf8
    Write-Output ('Pages='+$reportDoc.ComputeStatistics(2)+'; Tables='+$reportDoc.Tables.Count+'; Figures='+$reportDoc.InlineShapes.Count)
} finally {
    if($reportDoc){$reportDoc.Saved=$true;$reportDoc.Close()}
    $wordApp.Quit()
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($wordApp)
}
