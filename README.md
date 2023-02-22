# Lectio-mash



Lectio-mash er et program der er inspireret af Fase-mash fra filmen The Social Network bare udviklet til Lectio.
I filmen består programmet i skabe en hjemmeside der præsentere billeder af to piger, man trykker så på den flotteste pige og bliver præsenterete for to nye piger. 
Det samme gør lectio-mash, men denne gang med billeder fra din skole! (man kan skifte mellem billeder af drenge og piger)

--LÆS / introdukcer dig selv til filerne inden du kører dem.
--Husk på at det kan gå imod gdpr lovgivningen af udgive billeder af andre uden tiladelse 
--jeg tager intet ansvar for hvordan programmet bliver brugt, programmet i sig selv går ikke i mod GDPR loven


<h1 style ="color: #FF0000; "> VIGTIGT 
<h3>bevar filernes struktur</em></h3>
filerne "snakkersammen" og skal derfor vide hvor de ligger i forhold til hinnanden 
du kan sagtens rykke på begge filer bare bevar strukturen, evt lav genveje hvis det er et problem



<h2>Database scriptet</h2>
- denne fil skal kun køres en gang med mindre en ny databse skal etableres,



<h3>grunde til at kører det flere gange</h3>

problmer i navnefilen, noget der vil blive forklaret senere
eller lysten til at etablere en database med et andet logind

uanset hvorfor man vil køre programmet flere gange er det vigtigt at slette eller rykke den eksisterende database under \main stien 
den fil eksistere ikke hvis programmet ikke har været kørt før 


---

<h2>databaseskaber filen</h2>

lectio-mash bruger et logind (brugernavn & adgangskode) til at downloade alle elevers lectio-billder på det givende loginds skole
Brugernavnet og koden bliver ikke gemt efter programmet er lukket og bliver kun brugt til at ekstrahere cookies der er nødvendige for programmet


programmet tager "relativ" langtid at kører da lectios server bliver sure og midlertigt banlyser
programmet (din computer) fra lectios server hvis du sender "beskeder" til serveren for hurtigt
for at undgå det kan programmet kun maksimalt sende 10 beskeder i sekundet mene dette tal er lavere afhængig af computeren der kører programmet

for en skole med omkring 1200 elever tager det ca 8 minutter 
i programmets consol kan der ses direkte updatering om hvad programmet laver 


-----

<h4>håndtering af billder</h3>

billederne der bliver først downloaded ned til en fil, derefter bliver de så skrevet ind i en database som hjemmesiden (main.py) kan ekstrahere og ændre værdier i
Databasen har en indbygget elo(samme system og k-værdi som i skak) der ændre sig afhængig af hvem man er blevet sammenlignet på hjemesiden og deres elo
samt hvorvidt personen dømte en til at være mere attraktive end den anden. 





<h2>Problemer og løsninger</h2>

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


<h3>effektiviter det</h3>

største delen af ventetiden i koden er den tid computeren bruger på ikke at spørge lectio, (forklaret tidligere)
dette problem kunne nemt løses. Faktisk kunne programmet kører meget hurtigere og kræve marknt mindre computerkræft. 
hvis man i stedet for at lave alle elevid om til billede ider et af gangen gjor det pr klasse. Der opstår noget andre problemer men et er hurtigere og anderledes jeg har ikke gjort det fordi jeg først tænkte på det efter jeg havde lavet programmet og lad ik ændre på det.

<h2>main.py</h2>

--------

deter først gang jeg rigtigt har kodet html og css så det er blevet lidt en skrammel bunke, jeg gemmer information i html'en og læser den igen når den kommer tilbage. dette sytem er super usikkert og kan nemt misbruges jeg har lavet en "encodeing" dens formål er udelukkende at gøre det vanskligt for brugeren, en der kommer ind på hjemmesiden af forstå hvad der sker med tallen og hvordan de kunne manipuleres for at ændre ens rating i databasen. Hvis du selv har en bedre løsning end den jeg bruger kan du jo bare kun bruge 'etablere_database' scriptet 


<h3>Problemer</h3>

ligenu vises to billede tilfældigt, ideelt skulle to mennesker med samme elo matches mod hinnaden. 
jeg har en udgave der gør det så effiktivt som muligt men det kan man selv finde ud af hvorfor kunne være et problem.








