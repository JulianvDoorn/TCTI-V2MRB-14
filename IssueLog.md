# Issue log
In dit practicum waren er verschillende issues tegengekomen. Problem met bijvoorbeeld dat de bal niet wordt herkend. Of dat de calibratie fout is gelopen
waardoor de software een fout beeld heeft van de realiteit. Kortom, er zijn verschillende problemen gevonden die in de loop van dit practicum zijn op gelost.
In dit document staat er beschreven welke problemen er waren en welke oplossing is gevonden.

Van de volgende opsomming kan er van uit worden gegaan dat de issues in chronologische volgorde zijn geconstateerd en opgelost.

## Resolved issues
### Issue
Er kan geen bal worden herkend op de platform. Het systeem kan dus geen error berekenen.
#### Solution
Doormiddel van een preprocessing filter krijgt een afbeelding een hoog contrast. Wanneer er thresholding op deze afbeelding wordt gedaan springen alle kleuren
eruit en is het makkelijk te identificeren welke kleur waar zit. Maar omdat alleen zwarte elementen in de afbeelding interessant zijn, wordt er een kleuren
filter toegepast. Als een kleur niet dicht genoeg bij zwart zit, wordt de pixel uitgezet, als een kleur erg op zwart lijkt, wordt de pixel aangezet. Op die
manier onstaat er een mask dat over alle zwarte pixels heen gaat. Deze mask is minder gevoelig voor dingen als schaduw en andere laagfrequente gradienten. Op
deze mask kan er blobdetectie worden uitgevoerd. Wanneer er maar een blob in het plaatje zichtbaar is, gaat de software ervan uit dat die blob de bal is.

### Issue
De software kan de gekleurde lokalisatiestickers niet accuraat vinden aan de hand met een kleuren filter en gemiddelde positie van pixels met een specifieke 
kleur. Overigens beinvloeden de stickers elkaar, wanneer bijvoorbeeld een klein beetje groen als blauw wordt gezien. 
#### Solution
Wanneer de gemiddelde positie van bijvoorbeeld een blauwe pixel is bepaald. Kan er een Hough transformatie worden uitgevoerd. Een Hough transformatie
identificeerd alle cirkels op een plaatje, maar bied geen context over deze cirkel. Een mooie oplossing was dus om onze eerste insteek te combineren
met een Hough transformatie. Ons nieuwe algoritme bepaald dus de gemiddelde positie van bijvoorbeeld alle blauwe pixels, vervolgens koppelt hij een
Hough cirkel aan een blob pixels. De blobs bieden dus context aan de preciezere Hough cirkels.

### Issue
Het verschil berekenen tussen twee punten aan de hand van aftrekken en dan pythagoras toepassen geeft geen negatieve waardes terug. Dit is nodig
voor wanneer de bal buiten de drie motor stickers valt, dat moet de PID namelijk ook corrigeren.
#### Solution
In plaats van af te trekken met punten, moeten de setpoint en ballpoint worden geprojecteerd op de as van de servomotor. Aan de hand van deze projectie
kan er ook worden berekend of de bal boven of onder een motor zit. Tevens is deze techniek een stuk beter voor het PID systeem, omdat de error nu meer
de daadwerkelijke acties van de idividuele servomotoren representeerd.

### Issue
Het PID systeem bewoog de plaat op en neer maar hield de plaat nog wel strict horizontaal. Meestal was het gedrag capped out door de servo guard wat ervoor
zorgde dat de servos niks stuk maakten, waardoor het leek alsof het systeem niks meer deed.
#### Solution
De PID class gebruikte voor de opslag van servo specifieke variabelen 'self'. Terwijl PID alle drie de servos onder de controlerende PID class vallen. Alleen
de laatste servo binnen het algoritme deed dus wat hij hoorde te doen, maar de rest deed hetzelfde. Het was opgelost om servo specifieke variabelen onder de
daadwerkelijke servo instanties te brengen, zodat ze niet onterecht worden overschreven.

### Issue
Er moet een hele hoge Kp waarde zijn om de bal in bewegen te laten komen. Dit is op het eerste gezicht niet heel erg, maar dit bracht wel het hele
systeem uit balans omdat de Ki en Kd waardes dan ook anders moesten.
#### Solution
Het probleem had niks met de software te maken. Het zat hem in de hardware van het systeem. Met name de plexiglas en het elastiek dat eronder zat.
het elastiek trok te hard aan de plexiglas waardoor het in een kom werdt gebogen. Het effect is dat er een hoge Kp moet worden ingesteld om de bal uit deze kom
te kunnen laten komen. De oplossing was dus simpelweg het elastiek losser laten zitten. Maar wel strak genoeg om de plaat in het midden te houden.