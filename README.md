# Goose Creek Candles Customer Review Analytics

## Steps performed in this Project:

    1) Scrapped the Goosecreek Site to create dataset using Scrappy Framework. Automated scrapping and storing data in GCS using     
       docker and Cloud Run for automating the process. 
    2) Used Tearraform to create infrastructure in GCP for data cleaning (using Dataproc) and storing (GCS, BigQuery). Thereafter   
       created table for the cleaned dataset.
    3) Leveraged the BigQuery Table as a datasource for Looker Studio to create dashbord.
   
## Highlights of the Dashboard:

    1) Spring Candles Category is the most famous among all (highest sold) along with highets number of reviews.
    2) Old Time Lemonad Large 3 Wick Candle (lemon, pineapple, sparkling water & Sugar) is the most reviewed scent profile, Along           with highest number of 5 star ratings.
    3) During sale seasong the highest discount went up till 91% (this range had a mix of low rated candles and average rated ones)         with most of the articles have a 60% discount.

 You can check the sneak peek of the Dashboard below:
   
![image](https://github.com/MishraCo/GooseCandle_Review_Dashboard/assets/111904405/94c64f56-a2ef-4899-8cc4-d703ae5fa7e5)


Link to the Dashboard: https://lookerstudio.google.com/u/0/reporting/6d17c6cd-a64e-4861-a444-d129113dc0bb/page/tEnnC 
