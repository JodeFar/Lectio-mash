# Lectio-mash
Lectio-mash er et program der er inspireret af Fase-mash fra filmen The Social Network bare udviklet til Lectio.
Lectio-mash er et program der er inspireret af Fase-mash fra filmen The Social Network bare udviklet til Lectio.
I filmen består programmet i skabe en hjemmeside der præsentere billeder af to piger, man trykker så på den flotteste pige og bliver præsenterete for to nye piger. 
Det samme gør lectio-mash, men denne gang med billeder fra din skole! (man kan skifte mellem billeder af drenge og piger)

--LÆS / introdukcer dig selv til filerne inden du kører dem.



VIGTIGT: bevar filernes struktur. filerne "snakkersammen" og skal derfor vide hvor de ligger i forhold til hinnanden 
du kan sagtens rykke på begge filer bare bevar strukturen, evt lav genveje hvis det er et problem

-------Database scriptet------   
- denne fil skal kun køres en gang med mindre en ny databse skal etableres,

evt grunde til at kører det flere gange 
-------
[problmer i navnefilen, noget der vil blive forklaret senere]
[eller lysten til at etablere en database med et andet logind of ]
----

uanset hvorfor man vil køre programmet flere gange er det vigtigt at slette eller rykke den eksisterende database under \main stien 
den fil eksistere ikke hvis programmet ikke har været kørt før 



lectio-mash bruger et logind (brugernavn & adgangskode) til at downloade alle elevers lectio-billder på det givende loginds skole
Brugernavnet og koden bliver ikke gemt efter programmet er lukket og bliver kun brugt til at ekstrahere cookies der er nødvendige for programmet


programmet tager "relativ" langtid at kører da lectios server bliver sure og midlertigt banlyser
programmet (din computer) fra lectios server hvis du sender "beskeder" til serveren for hurtigt
for at undgå det kan programmet kun maksimalt sende 10 beskeder i sekundet mene dette tal er lavere afhængig af computeren der kører programmet

for en skole med omkring 1200 elever tager det ca 8 minutter 
i programmets consol kan der ses direkte updatering om hvad programmet laver 


-----


billederne der bliver først downloaded ned til en fil, derefter bliver de så skrevet ind i en database som hjemmesiden (main.py) kan ekstrahere og ændre værdier i
Databasen har en indbygget elo(samme system og k-værdi som i skak) der ændre sig afhængig af hvem man er blevet sammenlignet på hjemesiden og deres elo
samt hvorvidt personen dømte en til at være mere attraktive end den anden. 





Problemer og løsninger 

databasen forsøger automatisk at bestemme hvorvidt du er en pige eller dreng ud fra dit navn. 
Det virker ca 95% af tiden. Når det kører rigtigt og betyder også at du under drenge afdelingen kommer til at se en pige engang i mellem 
problemet kan løses på en række måder 


drengenavne filen jeg bruger er praktisktalt elendig jeg har selv fjenret en række helt nomale pigenavne som "Kaya" og "Andrea" 

løsning 1:
- hvis man oplever at der stadig er pigenavne i filen (hvilket der er) kan man åbne drengenavne filen 
- trykke CRTL & f slå "forskel mellem stort og bvogstav" til og søge efter pigenavnet man har fundet ud af ligger i filen 
- det kan man bare slette så sletter man databasen fra main.py filen og kører "etablere database" igen


løsning 2:
- manuelt ændre databasen (drenge er markert med et 'm' og piger ved værdien None)
- her skal man bruge et program til visualisere databasen fx 'DB-browser'  (databasen er en SQLite fil)
