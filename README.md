# Tri-Servo Platform Practicum
De scope van dit practicum richt zich op het controleren van de positie van een bal in een 2D ruimte. Deze 2D ruimte stelt een plaat voor wat aan de hand van servomotoren kan worden gekanteld. Aan de hand van PID worden de graden berekend en kan er een erg precies systeem worden ontwikkeld.

Het lokaliseren van de bal op de platform zal worden gedaan met gebruik van een webcam. Deze webcam staat op een statief gemonteerd en is haaks op het  _tri-servo platform_  gericht. Dan kan er aan de hand van vision algoritmes de bal worden herkend.

Dit past goed bij de cursus  _Meten, regelen en besturen_, want alle drie de aspecten komen voor in dit practicum. (Meten: vision algoritme, regelen: PID berekening, besturen: servo motoren)

## Functionality
De functionaliteit van de hard- en software staan hieronder beschreven, deze zijn afgeleid uit de MoSCoW requirements in het PvA:

> Cijfers representeren een item uit de must, should and could have. De tientallen representeren de categorie (must, should of could). De eenheden vormen een feature. Voor een werkbaar product is elke feature naar minimaal 'must have' niveau worden gebracht.

-   **21 - Vlugge PID**  PID integratie met een vlugge afstelling, de bal komt snel dichtbij. De steady state error detection (integraal) zal uiteindelijk de laatste correctie doen.
-   **12 - Bal detectie**  Vision algoritme voor bal detectie.
-   **13 - Error bepaling**  Error bepaling op drie assen. Het platform kent drie motoren, dus voor elke motor moet er een error worden bepaald om PID te kunnen regelen.
-   **34 - Automatische beeldafkapping**  Automatische beeldafkapping van de webcam tijdens opstarten.
-   **35 - Automatische motor lokalisatie**  Automatische lokalisering van de motors tijdens opstarten.
-   **26 - Handmatige SetPoint**  Handmatig ingestelde SetPoint, de gebruiker kan op een venster klikken waar de SetPoint is.
-   **17 - Servo aansturing**  Het systeem kan aan de hand van actuators de bal in een richting kunnen bewegen.

## Required Hardware

- 'Tri-Servo Platform'
	- Drie krachtig genoege servomotoren
	- Lichte plaat met lokalisatiestickers (40x40 plexiglas, bijvoorbeeld, liefst ondoorzichtig d.m.v. tape of verf)
	- Elastiek waarmee de plaat in het midden mee wordt gehouden
	- Juiste voeding voor de servomotoren (Wij werkten met een 5V, 0.7A telefoonoplader)
> 5V kan door de Arduino worden geleverd, maar soms trokken de servos te veel stroom, waardoor de Arduino zich resette. Dit is vervelend wanneer je een bal probeert te balanceren.
- Arduino Due
- USB Webcam
	- Statief voor de webcam wat hoog genoeg is om de gehele Tri-Servo Platform in beeld te brengen

### Pin Layout Diagram

![Drie Servos en Arduino](https://raw.githubusercontent.com/JulianvDoorn/TCTI-V2MRB-14/master/Img/HardwareLayout.png)<br>
<sub>Pinlayout</sub>

In het bovenstaande diagram staat beschreven hoe de Arduino Due is verbonden met de drie servomotoren en hoe de servomotoren aan de voeding is aangesloten.

Het staat niet gemodelleerd in het schema maar de Arduino krijgt zijn voeding van de PC doormiddel van een USB. Tevens wordt er met deze USB verbinding gecommuniceerd met de PID software. Overigens moet de USB webcam ook aangesloten zijn aan de PC.

## Software dependencies

- Arduino IDE/Toolchain
- Python 3
- OpenCV (voor Python 3)
- Numpy

### Install and user Guide

Wanneer alle hardware gereed staat, kan de software worden geïnstalleerd. De software is doet in principe heel veel zelf wanneer de webcam op het bewegende platform staat gericht. Het is belangrijk dat alle stickers herkenbaar voor de webcam zijn.

#### Vision
![Platform met stickers](https://raw.githubusercontent.com/JulianvDoorn/TCTI-V2MRB-14/master/Img/PlatformPlate.jpg)<br>
<sup>Foto van de plaat, hoe de webcam het zou moeten zien</sup>

Dit is hoe onze plaat eruit ziet voor onze webcam. Het is van belang dat de stickers rond zijn en gekleurd in dezelfde kleuren als hierboven. De software filtert namelijk alle kleuren eruit behalve, bijvoorbeeld, rood. Wanneer dit is gedaan voert het stickerherkenning uit. 

De webcam moet verbonden zijn met de 1<sup>e</sup> (niet de 0<sup>e</sup>) virtuele webcam poort. Dit kan in main.py worden aangepast bij `cap = cv2.VideoCapture(1)`. Dit komt omdat de laptop waar het al op was ontwikkeld een webcam op de 0<sup>e</sup> webcam heeft.

#### Arduino
Voordat het allemaal werkt moet eerst nog de Arduino worden geflashed met de code dat de servomotoren aanstuurd aan de hand van seriele commando's. De sketch kan je vinden in het mapje `Arduino/`. Deze sketch kan je met de Arduino IDE uploaden naar je Arduino. Wanneer dit is gedaan heb je de Arduino IDE niet meer nodig.

### Class Diagram

![Class diagram](https://raw.githubusercontent.com/JulianvDoorn/TCTI-V2MRB-14/master/Img/ClassDiagram.png)<br>
<sup>Klassediagram van de Python software</sup>

| Element       | Description   |
| :-----------: |---------------|
| Vision Class | Dit is het metende gedeelde van het systeem. Het gebruik verschillende algoritmes en een instantie van Calibration om errors te berekenen die bruikbaar zijn voor een PID regelaar. |
| Calibration Class | Bevat subroutines om aan de hand van een video stream de motors te lokaliseren en een middelpunt te berekenen. Wanneer een instantie zich heeft gekalibreerd kan een instantie van Vision gebruik maken van de kalibratie. |
| FocusedVideoCapture Class | Dit is een wrapper class de VideoCapture uit OpenCV. Deze class runt nog een _crop_ operatie over de frame die uit VideoCapture.read() komt. Dit is bruikbaar voor het optimaliseren van de vision algoritmes.  |
| PID Class | Dit is het regelende component van dit systeem. Instances van PID kennen drie servo's en bevat een 'update' functie die de servo's update aan de hand van de ontvangen errors. |
| Servo Class | Dit is het regelende deel van het systeem. Het is gespecialiseerd voor het sturen van commando's naar de Arduino. Elke servo instance bestuurd maar een servo, maar de daadwerkelijke controller kent er maar liefst drie. Daarom moet er de seriële verbinding tussen instances worden gedeeld. Tenzij het geëxpliciteerd is dat verschillende servo's andere seriële poorten gebruiken. |
| MainLoop | In de daadwerkelijke software, is MainLoop niet een class. Maar voor het nut van een class diagram was het belangrijk om dit component de modelleren. Het nut van de MainLoop is om het PID gedeelte en het Vision gedeelte samen te voegen. |

### PID Loop

![PID Feedback Loop](https://raw.githubusercontent.com/JulianvDoorn/TCTI-V2MRB-14/master/Img/PIDLoop.png)<br>
<sup>Diagram van de PID feedback lus</sup>