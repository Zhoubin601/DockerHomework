from pathlib import Path
import sys
import win32com.client

path=Path(sys.argv[1]).resolve()
word=win32com.client.DispatchEx('Word.Application')
word.Visible=False
word.DisplayAlerts=0
document=None
try:
    document=word.Documents.Open(str(path),ReadOnly=False,AddToRecentFiles=False)
    for table in document.Tables:
        table.Rows(1).HeadingFormat=True
        table.Rows.AllowBreakAcrossPages=False
    document.Repaginate()
    for toc in document.TablesOfContents:
        toc.Update()
        toc.Range.Font.NameFarEast='宋体'
        toc.Range.Font.Color=0
    document.Fields.Update()
    for section in document.Sections:
        for footer in section.Footers:
            footer.Range.Fields.Update()
    document.Repaginate()
    document.Save()
    print('Word fields refreshed; native page count:',document.ComputeStatistics(2))
finally:
    if document is not None: document.Close(SaveChanges=False)
    word.Quit()
