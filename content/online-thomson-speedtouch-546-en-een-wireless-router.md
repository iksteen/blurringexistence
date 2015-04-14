Title: Online, Thomson SpeedTouch 546 en een wireless router
Date: 2011-03-10 21:00
Author: Ingmar Steen
Tags: technical

**Note**: This entry is in Dutch because it concerns an ADSL setup
that’s pretty specific to a Dutch internet provider. If you’re
interested in an English translation, feel free to leave a comment.

Hier in Zoetermeer hebben we een ADSL
verbinding van Online en hebben daarbij een Thomson SpeedTouch 546 modem
gekregen. Prima modem/router maar vanwege het configuratieprofiel dat
Online standaard levert ontbreken er een aantal instellingen: Er is geen
root of SuperUser account aanwezig, alleen een gebruikersaccount en een
TechSupport account.

Nou is het zo dat er achter de modem een Linksys WRT350N v2 router hangt
voor de draadloze verbinding. Dit leidt ertoe dat port forwards dubbel
moesten worden ingesteld. Nu zul je denken, dan stel je op de modem toch
gewoon de DMZ in. En ja, dat zou mogelijk zijn
ware het niet dat dit een van de opties is die niet bereikbaar is.

Er zijn diverse opties om dit probleem te omzeilen. Het is mogelijk de
Linksys alleen als switch te gebruiken door de modem in een van de LAN
poorten van de router te steken en DHCP op de router uit te schakelen.
Zonde van de routing functionaliteiten van de router, hadden we net zo
goed een accesspoint kunnen kopen. Een andere optie is het standaard
account aan te passen door de configuratie te downloaden, de rol van de
standaardgebruiker aan te passen en de aangepaste configuratie weer te
uploaden (dit is een populaire methode voor bijvoorbeeld de SpeedTouch
706). Dit kreeg ik echter niet voor elkaar.

Derde optie, en de optie waar ik voor gekozen heb is om de modem alleen
als bridge te laten fungeren en niet als router. Dit is erg makkelijk
aangezien Online ADSL levert middels ETHoA
(Ethernet over ATM) (aka RF1483 in bridged
modus of LLC). Het enige wat de router dan
hoeft te doen is via DHCP een IP adres
opvragen en alles werkt. Dit moet herkenbaar zijn als je ooit
kabelinternet hebt gehad. De meeste kabelmodems werken ook niet als
router.

Het instellen van deze modus is simpel: ga met je webbrowser naar
http://10.0.0.138 en kies in het SpeedTouch menu de optie
"Configuratie". Klik vervolgens op de "Instellingen" link en er
presenteert zich een wizard. Aan het begin van deze wizard kun je kiezen
tussen 3 profielen: bridged, Online ADSL en
routed. Kies hier voor bridged en doorloop de wizard. Kies als VC/MUX
8.35, dit was bij mij ook de standaardinstelling
(waarschijnlijk omdat dit al stond ingesteld).

Reboot vervolgens de router en controleer of deze een publiek IP adres
krijgt. Klaar is kees.

Mocht je weer bij de configuratie van de SpeedTouch willen komen moet je
een apparaat een vast IP adres geven in de 10.0.0.0/24 reeks en
rechtstreeks aansluiten op een van de LAN
poorten van de modem. Surf vervolgens weer naar http://10.0.0.138 en je
krijgt de configuratie te zien. Alternatief hiervoor: Reset de router
volledig met behulp van een pennetje / paperclip en het welbekende
verzonken resetknopje. Reboot hierna de router weer en de router zou
weer een IP adres uit de 10.0.0.0/24 moeten krijgen waarna je ook weer
toegang hebt tot de configuratiepagina.
