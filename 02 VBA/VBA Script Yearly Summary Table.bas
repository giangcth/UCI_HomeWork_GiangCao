Attribute VB_Name = "Module3"
Sub Data_summary():

Dim i As Long

Dim j As Long

Dim lastrow As Long

Dim Ticker As String

Dim open_value As Double

Dim close_value As Double

Dim Yearly_Change As Double

Dim Percent_Change As Double

Dim Total_Stock_Volumn As Double


lastrow = Cells(Rows.Count, 1).End(xlUp).row


' adding label for summary columns

Cells(1, 9).Value = "Ticker"

Cells(1, 10).Value = "Yearly_Change"

Cells(1, 11).Value = "Percent_Change"

Cells(1, 12).Value = "Total_Stock_Volumn"



  
' Adding columns in Summary Table section

    
    Total_Stock_Volumn = 0
    
    Dim Summary_Table_Row As Integer
    
    Summary_Table_Row = 2
    
    Dim ticker_row As Integer
    
    ticker_row = 0
    
               
    For i = 2 To lastrow
        
                          
             open_value = Cells(i - ticker_row, 3).Value
                
             close_value = Cells(i, 6).Value
             
            
            If Cells(i + 1, 1).Value <> Cells(i, 1).Value Then
        
                
                ticker_row = ticker_row + 1
                
                                
                Ticker = Cells(i, 1).Value
                                               
                Total_Stock_Volumn = Total_Stock_Volumn + Cells(i, 7).Value
                
                               
                                
                Yearly_Change = (close_value - open_value)
                
                                                           
                If open_value <> 0 Then
                
                Percent_Change = (Yearly_Change / open_value) * 100
                
                End If
                
                                
                
                Range("I" & Summary_Table_Row).Value = Ticker
                
                Range("L" & Summary_Table_Row).Value = Total_Stock_Volumn
                
                Range("J" & Summary_Table_Row).Value = Yearly_Change
                
                Range("K" & Summary_Table_Row).Value = (Str(Percent_Change) + "%")
                
                
                
                Summary_Table_Row = Summary_Table_Row + 1
                
                
                Total_Stock_Volumn = 0
                
                ticker_row = 0
                
                
                            
            Else
            
                       
                Total_Stock_Volumn = Total_Stock_Volumn + Cells(i, 7).Value
                
                ticker_row = ticker_row + 1
                
                                            
                                
                                
            End If
            
            
                       
    Next i
    
    
    
    Dim SummaryRow As Integer
    
    SummaryRow = Cells(Rows.Count, 9).End(xlUp).row
    
    
    For i = 2 To SummaryRow
    
        If Cells(i, 10).Value > 0 Then
            Cells(i, 10).Interior.ColorIndex = 4
            
        ElseIf Cells(i, 10).Value < 0 Then
            Cells(i, 10).Interior.ColorIndex = 3
            
        ElseIf Cells(i, 10).Value = 0 Then
            Cells(i, 10).Interior.ColorIndex = 6
            
        End If
        
            
    Next i
    

 'challenge questions
 
Cells(1, 16).Value = "Ticker"
Cells(1, 17).Value = "Percent Value"
Cells(2, 15).Value = "Greates % Increase"
Cells(3, 15).Value = "Greates % Decrease"
Cells(4, 15).Value = "Greates Total Volume"


Dim Max As Double

Dim Min As Double

Dim Volumn As Double



Max = 0

Min = 0

Volumn = 0




For i = 2 To SummaryRow

    If Cells(i, 11).Value > Max Then
    
    Max = Cells(i, 11).Value
    
    Cells(2, 16).Value = Cells(i, 9).Value
    Cells(2, 17).Value = Str(Cells(i, 11).Value * 100) + "%"
    
    
    ElseIf Cells(i, 11).Value < Min Then
    
    Min = Cells(i, 11).Value
    
    Cells(3, 16).Value = Cells(i, 9).Value
    Cells(3, 17).Value = Str(Cells(i, 11).Value * 100) + "%"
    

    End If
    
    
    If Cells(i, 12).Value > Volumn Then
    
    Volumn = Cells(i, 12).Value
    
    Cells(4, 16).Value = Cells(i, 9).Value
    Cells(4, 17).Value = Cells(i, 12).Value
    
    End If
    
    
Next i

 
     

End Sub

