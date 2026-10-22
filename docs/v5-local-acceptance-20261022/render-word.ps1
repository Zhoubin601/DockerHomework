$ErrorActionPreference='Stop'
$workspaceRoot=[System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..'))
$inputPath=Join-Path $workspaceRoot 'output/v5/20261022-docker-lab-report-v5.docx'
$copyPath=Join-Path $PSScriptRoot 'report-review.docx'
Copy-Item -LiteralPath $inputPath -Destination $copyPath
$wordApp=New-Object -ComObject Word.Application
$wordApp.Visible=$false
$wordApp.DisplayAlerts=0
$wordApp.AutomationSecurity=3
$reportDoc=$null
try {
    $reportDoc=$wordApp.Documents.Open($copyPath,$false,$true)
    $reportDoc.Repaginate()
    $headingPages=@()
    foreach($paragraph in $reportDoc.Paragraphs){
        if($paragraph.OutlineLevel -le 2){
            $headingPages += [pscustomobject]@{heading=$paragraph.Range.Text.Trim();level=$paragraph.OutlineLevel;page=$paragraph.Range.Information(3)}
        }
    }
    $pdfPath=Join-Path $PSScriptRoot 'report-review.pdf'
    $reportDoc.ExportAsFixedFormat($pdfPath,17)
    [pscustomobject]@{pages=$reportDoc.ComputeStatistics(2);tables=$reportDoc.Tables.Count;images=$reportDoc.InlineShapes.Count;toc=$reportDoc.TablesOfContents.Count;headings=$headingPages} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'word-native.json') -Encoding utf8
    Write-Output ('Pages='+$reportDoc.ComputeStatistics(2)+'; Tables='+$reportDoc.Tables.Count+'; Figures='+$reportDoc.InlineShapes.Count)
} finally {
    if($reportDoc){$reportDoc.Close(0)}
    $wordApp.Quit(0)
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($wordApp)
}
