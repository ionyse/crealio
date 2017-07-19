/*
Le système de pop up est utilisé :
- CV Photo colonne droite
- Crealio, description d'un projet

*/

<!-- On charge la page et affiche le resultat -->
function showPopUpProject(type,nom,img,desc,taille,date,url,fichier)
{
	<!-- En fonction du type, on charge différente page ainsi que différent contenu. -->
	if(type == 'apercuImg')
	{
		//On change la class pour que la fenetre soit celle d'un aperçu image.
		document.getElementById("popUpProjet").className= "corpPopUpImg";

		texte="<p><a href='' onclick='closePopUpProject(); return false;'><img src='"+img;
		texte+="' alt='Cliquez pour Fermer'/></a><br/><a href='' onclick='closePopUpProject(); return false;'>Cliquez sur l'image pour fermer l'aperçu.</a></p>";   

		//On applique le contenu sur les div du popUp.
		document.getElementById("contenuTitrePopUp").innerHTML="<span style='font-size: 0.7em;'>Titre de l'image :</span> <strong>"+nom+"</strong>";
		document.getElementById("contenuCorpPopUp").innerHTML=texte;  
	}
	else if(type == 'project')
	{
		//On change la class pour que la fenetre soit celle d'un aperçu image.
		document.getElementById("popUpProjet").className= "corpPopUpProjet";

		texte="<div id='bodyPopUpProject'><div class='popUpProjectImage'><p><a href='' onclick='closePopUpProject(); return false;'><img src='"+img;
		texte+="' alt='Cliquer pour Fermer' class='imgPopUp'/></a></p>";
		if(taille == 'True')
		{
			texte+="<div class='boutonPopUp'>";
			if(url != '')
			{
				texte+="<div class='boutonLink'><p><a href='"+url;
				texte+="'>Liens</a></p></div>";
			}
			if(fichier != '')
 			{
				texte+="<div class='boutonDl'><p><a href='"+fichier;
				texte+="'>Télécharger le fichier</a></p></div>";
			}
			texte+="</div>";	
		}

		
		texte+="</div><div class='popUpProjectDetail'>";
		texte+="<p class='titrePopUpProject'><strong>"+nom+"</strong></p>";
		texte+="<p><span style='font-size: 0.9em;'>Date de creation : "+date+"</span></p>";
		texte+="<div id='popUpProjectDesc'></div>";
		if(taille == 'False')
		{
			texte+="<div class='boutonPopUp'>";
			if(url != '')
			{
				texte+="<div class='boutonLink' style='clear: both;'><p><a href='"+url;
				texte+="'>Liens</a></p></div>";
			}
			if(fichier != '')
 			{
				texte+="<div class='boutonDl' style='clear: both;'><p><a href='"+fichier;
				texte+="'>Télécharger le fichier</a></p></div>";
			}
			texte+="</div>";	
		}

		texte+="</div>";
		texte+="<div style='clear: both;'><p><a href='' onclick='closePopUpProject(); return false;'>Cliquez içi ou sur l'image pour fermer l'aperçu.</a></p></div></div>";   
		document.getElementById("contenuTitrePopUp").innerHTML="";
		document.getElementById("contenuCorpPopUp").innerHTML=texte;
		//Solution barbare pour afficher le texte et pour remplacer les div en texte afin d'avoir un affichage correct. 
		document.getElementById("popUpProjectDesc").innerHTML=document.getElementById(desc).innerHTML.replace('<div>','<p>').replace('</div>','</p>');	       
	}
	else if(type == 'conditions')
	{
		document.getElementById("popUpProjet").className= "corpPopUpCondConf";

		texte="<div id='conditionConfidentialite'></div><p><a href='' onclick='closePopUpProject(); return false;'>Cliquez içi pour fermer l'aperçu.</a></p>";   
		document.getElementById("contenuTitrePopUp").innerHTML="<p><strong>"+nom+"</strong></p>";
		document.getElementById("contenuCorpPopUp").innerHTML=texte;
		document.getElementById("conditionConfidentialite").innerHTML=document.getElementById(desc).innerHTML.replace('<div>','<p>').replace('</div>','</p>');	       
	}
	else if(type == 'confidentialité')
	{
		document.getElementById("popUpProjet").className= "corpPopUpCondConf";

		texte="<div id='conditionConfidentialite'></div><p><a href='' onclick='closePopUpProject(); return false;'>Cliquez içi pour fermer l'aperçu.</a></p>";   
		document.getElementById("contenuTitrePopUp").innerHTML="<p><strong>"+nom+"</strong></p>";
		document.getElementById("contenuCorpPopUp").innerHTML=texte;
		document.getElementById("conditionConfidentialite").innerHTML=document.getElementById(desc).innerHTML.replace('<div>','<p>').replace('</div>','</p>');
	}
	else
	{
		texte="<p>Le popUp est mal paramètré. Il faut contacter l'administrateur pour lui signaler le liens déféctueux.</p>";   
		document.getElementById("contenuTitrePopUp").innerHTML="<span style='font-size: 0.7em;'>Nom du Projet :</span> <strong> ERREUR INCONNU</strong>";
		document.getElementById("contenuCorpPopUp").innerHTML=texte;            
	}

	<!-- On affiche la page ainsi chargé. -->
	document.getElementById("popUpProjet").style.display = "block";

}

<!-- On retire la page apercu -->
function closePopUpProject()
{
	document.getElementById("popUpProjet").style.display = "none";
}