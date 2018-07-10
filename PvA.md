# PvA Tri-Servo Platform Practicum
De scope van dit practicum richt zich op het controleren van de positie van een bal in een 2D ruimte. Deze 2D ruimte stelt een plaat voor wat aan de hand van servomotoren kan worden gekanteld. Aan de hand van PID worden de graden berekend en kan er een erg precies systeem worden ontwikkeld.
Het lokaliseren van de bal op de platform zal worden gedaan met gebruik van een webcam. Deze webcam staat op een statief gemonteerd en is haaks op het _tri-servo platform_ gericht. Dan kan er aan de hand van vision algoritmes de bal worden herkend.
Dit past goed bij de cursus _Meten, regelen en besturen_, want alle drie de aspecten komen voor in dit practicum. (Meten: vision algoritme, regelen: PID berekening, besturen: servo motoren)

## MoSCoW
### Must have
- __11 - Werkbare PID__ PID integratie met werkbare afstelling waarbij de bal uiteindelijk wel op zijn plek komt
- __12 - Bal detectie__ Vision algoritme voor bal detectie.
- __13 - Error bepaling__ Error bepaling op drie assen. Het platform kent drie motoren, dus voor elke motor moet er een error worden bepaald om PID te kunnen regelen.
- __14 - Hardcoded beeldafkapping__ De focus frame van de webcam zit altijd op dezelfde plek. De focus frame zorgt ervoor dat de vision algoritmes optimaal presteren.
- __15 - Hardcoded motor lokalisatie__ Motor posities zitten altijd op dezelfde plek.
- __16 - Hardcoded SetPoint__ Het systeem wilt de bal altijd naar het midden toe brengen.
- __17 - Servo aansturing__ Het systeem moet aan de hand van actuators de bal in een richting kunnen bewegen.
### Should have
- __21 - Vlugge PID__ PID integratie met een vlugge afstelling, de bal komt snel dichtbij. De steady state error detection (integraal) zal uiteindelijk de laatste correctie doen.
- __24 - Handmatige beeldafkapping__ Handmatig ingestelde beeldafkapping van de webcam on de vision algoritmes optimaal te laten werken. Bij opstarten wordt het vlak door de gebruiker ingevoerd.
- __25 - Handmatige motor lokalisatie__ Handmatig ingestelde motor posities relatief aan het focuspunt van de webcam. Bij opstarten worden de punten door de gebruiker ingevoerd.
- __26 - Handmatige SetPoint__ Handmatig ingestelde SetPoint, de gebruiker kan op een venster klikken waar de SetPoint is.
### Could have
- __31 - Perfecte PID__ PID integratie met een onmiddellijke reactie en hoge precisie. De bal word meteen naar de setpoint gebracht en zal geen zichtbare steady state error hebben.
- __34 - Automatische beeldafkapping__ Automatische beeldafkapping van de webcam tijdens opstarten.
- __35 - Automatische motor lokalisatie__ Automatische lokalisering van de motors tijdens opstarten.

## Planning en communicatie
### Planning
Wij vinden dat wij het beste werken aan de hand van een leidraad. Normaliter expliciteren wij die niet op een formele wijze als dit, maar omdat er een schriftelijke PvA moet komen benoemen wij onze leidraad snel.

De volgende tussenproducten willen wij op chronologische wijze opleveren. De items zijn afgeleid van de requirements beschreven bij het kopje MoSCoW (van oud naar nieuw)

##### Must have:
- 14 - Hardcoded beeldafkapping
- 12 - Bal detectie
> Toelichting: als eerste moet er een werkende bal detectie komen. Dit is een cruciaal deel van het regelen van PID. Zonder dit element kan er niks komen dat zelfs op PID lijkt.

- 15 - Hardcoded motor lokalisatie
- 16 - Hardcoded SetPoint
- 13 - Error bepaling
> Toelichting: als tweede moet er een error kunnen worden bepaald. Dit moet dus aan de hand van motor posities en een setpoint. Dan kan er per motor een error worden berekend.

- 17 - Servo aansturing
> Toelichting: voordat de eerste PID kan worden geconfigureerd, moet er een manier zijn om de wereld te beïnvloeden. Dit gaat doormiddel van servomotoren.

- 11 - Werkbare PID
> Toelichting: wanneer er een error bepaling is en servos kunnen worden aangestuurd, kan er een eerste versie van PID kunnen worden geïmplementeerd. 
##### Should have:
- 25 - Handmatige motor lokalisatie
- 24 - Handmatige beeldafkapping
> Toelichting: omdat er een werkbare PID aansturing is, is dit niet meer het hoogste prioriteit. Er kan nu worden gekeken om het calibratieproces te verbeteren om een goede demo te leveren.
- 21 - Vlugge PID
- 26 - Handmatige SetPoint
##### Could have:
- 35 - Automatische motor lokalisatie
- 34 - Automatische beeldafkapping
> Toelichting: als de PID als voldoende wordt geacht, kan er worden gekeken om het calibratieproces te automatiseren. Als dit automatisch is kan er sneller worden getest worden met nieuwe PID waardes.
- 31 - Perfecte PID

### Communicatie
Wij zullen onderhands communiceren doormiddel van Telegram. Hiermee kunnen wij bestanden heen en weer sturen zonder gedoe en kunnen wij snel communiceren tijdens het werken op afstand.
Om met de docent te communiceren zullen wij onze school mails gebruiken en wanneer het uit komt zullen wij de docent persoonlijk opzoeken.

## Risico's
Om dit practicum zo optimaal mogelijk te laten verlopen hebben wij een bepaald aantal risico's in beeld gebracht. Deze risico's gaan in ons geval minder over technische problemen maar over de omstandigheden. Risico's als ziekteverzuim en andere onvoorspelbare kwesties zijn weggelaten.

#### R2D2
Kiet en Julian hebben beiden een verhoogde rol binnen R2D2. Daarom moet er rekening mee geworden dat dit practicum wellicht wordt afgeraffeld vanwege een tekort aan tijd en daarmee onvoldoende te scoren. Het is een optie om te wachten met het inleveren tot na R2D2. Dit zal wel betekenen dat de beoordeling volgens de herkansing gaat, maar het zal dan niet ten koste gaan van het eindcijfer.

Naast R2D2 achten wij dat er geen concrete risico's zijn omtrent dit practicum. 