TO EXECUTE THE CODE WITH PYTHON3 :

python3 seam_carving.py  <r/c> <scale> <image_input> <image_output>

<r/c>	: est de spécifier si vous voulez que le redimensionnement soit fait sur quel axe

<scale> : pour spécifier l'échelle de l'image que vous voulez. 
par exemple : si l'image est 780x640 et que j'ai choisi c et l'échelle est 0.5 alors
l'image de sortie sera 780x320 

<image_input> : est l'image d'entrée doit inclure le type d'image donc par exemple : SeamBefore.png
<image_output> : le nom de l'image de sortie, elle sortira au format png


THE IMAGES USED TO TEST :

SeamBefore.png  <598 x 521>
SeamBefore2.png <391 x 257>
SeamBefore3.png <297 x 395>
SeamBefore4.png <1920 x 1079> celui-ci prend environ 45mins à réduire avec une échelle de 0.8

les autres ne prennent pas plus de 8-10 mins pour l'échelle 0.5

IMAGES ALREADY REDIMENSIONED:

SeamAfter1.png   axis r scale 0.5 SeamBefore.png   <5mins 
SeamAfter2.png	 axis c scale 0.5 SeamBefore.png   <5mins

SeamAfter3.png	 axis r scale 0.5 SeamBefore2.png  <5mins
SeamAfter4.png	 axis c scale 0.5 SeamBefore2.png  <5mins

SeamAfter5.png	 axis r scale 0.5 SeamBefore3.png  <5mins
SeamAfter6.png	 axis c scale 0.5 SeamBefore3.png  <5mins

SeamAfter7.png	 axis r scale 0.8 SeamBefore4.jpg  8mins
SeamAfter8.png	 axis c scale 0.8 SeamBefore4.jpg  15mins