$churnJson = '{"gender":"Female","SeniorCitizen":0,"Partner":"Yes","Dependents":"No","tenure":1,"PhoneService":"No","MultipleLines":"No phone service","InternetService":"DSL","OnlineSecurity":"No","OnlineBackup":"Yes","DeviceProtection":"No","TechSupport":"No","StreamingTV":"No","StreamingMovies":"No","Contract":"Month-to-month","PaperlessBilling":"Yes","PaymentMethod":"Electronic check","MonthlyCharges":29.85,"TotalCharges":29.85}'
$c = Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method Post -Body $churnJson -ContentType "application/json"
Write-Output "CHURN_RESULT:"
Write-Output ($c | ConvertTo-Json)

$vgJson = '{"Platform":"Wii","Year":2006,"Genre":"Sports","Publisher":"Nintendo","NA_Sales":41.49,"EU_Sales":29.02,"JP_Sales":3.77,"Other_Sales":8.46}'
$v = Invoke-RestMethod -Uri "http://localhost:8001/predict" -Method Post -Body $vgJson -ContentType "application/json"
Write-Output "VG_RESULT:"
Write-Output ($v | ConvertTo-Json)

