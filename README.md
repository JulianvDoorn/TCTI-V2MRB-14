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

![Drie Servos en Arduino](https://raw.githubusercontent.com/JulianvDoorn/TCTI-V2MRB-14/master/HardwareLayout.png)
In het bovenstaande diagram staat beschreven hoe de Arduino Due is verbonden met de drie servomotoren en hoe de servomotoren aan de voeding is aangesloten.

Het staat niet gemodelleerd in het schema maar de Arduino krijgt zijn voeding van de PC doormiddel van een USB. Tevens wordt er met deze USB verbinding gecommuniceerd met de PID software. 

## Software dependencies

- Arduino Toolchain
- Python 3
- OpenCV (voor Python 3)
- Numpy
